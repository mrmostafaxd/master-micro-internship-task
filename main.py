import sys
from PySide2.QtCore import QSize
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout
from custom_widgets import CustomCanvas, CustomLabel, CustomLineEdit, CustomPushButton
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
import constants as cons


class MainWindow(QMainWindow):
    """
    The main application window for the Function Plotter app.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Function Plotter")
        self.setMinimumSize(QSize(cons.APP_MIN_WIDTH, cons.APP_MIN_HEIGHT))

        self.set_icon(cons.APP_ICON_LOCATION, cons.APP_ICON_SIZE)

        ################ Widgets ################
        # for function
        function_label = CustomLabel(
            "Function f(x):", cons.APP_NORMAL_FONT_SIZE)
        self.function_input = CustomLineEdit(cons.APP_NORMAL_FONT_SIZE)
        self.func_error_label = CustomLabel(
            "", cons.APP_ERROR_FONT_SIZE, cons.APP_ERROR_FONT_COLOR)

        # for minimum x value
        min_val_label = CustomLabel(
            "Minimum x value:", cons.APP_NORMAL_FONT_SIZE)
        self.min_val_input = CustomLineEdit(
            font_size=cons.APP_NORMAL_FONT_SIZE, float_only=True)
        self.min_error_label = CustomLabel(
            "", cons.APP_ERROR_FONT_SIZE, cons.APP_ERROR_FONT_COLOR)

        # for maximum x value
        max_val_label = CustomLabel(
            "Maximum x value:", cons.APP_NORMAL_FONT_SIZE)
        self.max_val_input = CustomLineEdit(
            font_size=cons.APP_NORMAL_FONT_SIZE, float_only=True)
        self.max_error_label = CustomLabel(
            "", cons.APP_ERROR_FONT_SIZE, cons.APP_ERROR_FONT_COLOR)

        # for plot button
        self.plot_button = CustomPushButton(
            "Plot", cons.APP_NORMAL_FONT_SIZE+4)
        self.plot_button.clicked.connect(self.plot)

        # for the Matplotlib Canvas
        self.canvas = CustomCanvas(
            width=cons.PLOT_CANVAS_FIGURE_WIDTH,
            height=cons.PLOT_CANVAS_FIGURE_HEIGHT,
            dpi=cons.PLOT_CANVAS_DPI
        )
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setDisabled(True)

        ################ Layout ################
        layout_main = QHBoxLayout()

        # set the layout that contains user controls
        layout_left = QVBoxLayout()
        left_widget = QWidget()

        # set the layout that contains matplotlib canvas
        layout_right = QVBoxLayout()
        right_widget = QWidget()

        layout_left.addWidget(function_label)
        layout_left.addWidget(self.function_input)
        layout_left.addWidget(self.func_error_label)
        layout_left.addWidget(min_val_label)
        layout_left.addWidget(self.min_val_input)
        layout_left.addWidget(self.min_error_label)
        layout_left.addWidget(max_val_label)
        layout_left.addWidget(self.max_val_input)
        layout_left.addWidget(self.max_error_label)
        layout_left.addWidget(self.plot_button)

        # to prevent the widgets from moving away from one another horizontally
        layout_left.addStretch(10)

        # create the container widgets that will contain the layouts
        layout_right.addWidget(self.canvas)
        layout_right.addWidget(self.toolbar)

        left_widget.setLayout(layout_left)
        # give enough breathing room for the controls
        left_widget.setMinimumWidth(450)

        right_widget.setLayout(layout_right)

        layout_main.addWidget(left_widget)
        layout_main.addWidget(right_widget)

        # make window scaling affects the graph more than the controls
        layout_main.setStretch(0, 1)
        layout_main.setStretch(1, 3)

        container = QWidget()
        container.setLayout(layout_main)

        self.setCentralWidget(container)

    def set_icon(self, icon_location, icon_size=48):
        """
        Sets the application icon.

        Parameters
        ----------
        icon_location : str
            The path to the icon file.
        icon_size : int
            The size of the icon.
        """

        # need to resize the icon first to prevent errors
        pixmap = QPixmap(icon_location)
        pixmap = pixmap.scaled(icon_size, icon_size)
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)

    def plot(self, s=None):
        """
        Clear the current plot and plot the validated function.

        Parameters
        ----------
        s: None
            An unused parameter to make the method 
            a slot for the clicked signal
        """

        self.canvas.default_config()

        # if the validation failed, disable Matplotlib toolbar and return
        x_y = self.validate_function()
        if not x_y:
            self.toolbar.setDisabled(True)
            return

        x, y, function_str = x_y
        # to fix the problem when the input function is a constant
        if not isinstance(y, np.ndarray) and not isinstance(y, list):
            y = [y] * len(x)

        # plot the function and enable Matplotlib toolbar
        self.canvas.replot_function(x, y, function_str)
        self.toolbar.setDisabled(False)

    def validate_function(self):
        """
        Validates the function input and the minimum and maximum x values before plotting the function.

        Returns
        -------
        A tuple containing an array of x values between the minimum and maximum x values, 
        the evaluated function string if the validation is successful, and the evaluated function 
        as a string to be a title in the graph , or None otherwise.
        """

        self.reset_errors()
        is_valid = True
        function_str = self.function_input.text()

        # check if the function input is empty
        if not function_str.strip():
            self.func_error_label.setText(cons.FUNC_VALUE_EMPTY_ERROR)
            is_valid = False

        # validate the minimum and maximum X values before usage
        min_max = self.validate_and_return_min_max()
        if not min_max:
            is_valid = False

        if not is_valid:
            return None

        min_value, max_value = min_max

        x = np.linspace(min_value, max_value, 1000)

        # validate the evaluation value of the function
        try:
            # convert the power operator to python compatible operator
            function_str_modified = function_str.replace("^", "**")
            return (x, eval(function_str_modified), function_str)
        except Exception as e:
            self.func_error_label.setText(cons.FUNC_VALUE_INCORRECT_ERROR)
            return None

    def validate_and_return_min_max(self):
        """
        Validates the minimum and maximum x values entered by the user.

        Returns
        -------
        A tuple of the valid minimum and maximum x values.
        """

        is_values_valid = True
        min_value = self.min_val_input.text()
        max_value = self.max_val_input.text()

        # validate the minimum x value
        if not min_value:
            is_values_valid = False
            self.min_error_label.setText(cons.MIN_VALUE_EMPTY_ERROR)
        else:
            try:
                # convert the power operator to python compatible operator
                min_value = min_value.replace("^", "**")
                min_value = float(eval(min_value))
            except Exception as e:
                is_values_valid = False
                self.min_error_label.setText(cons.MIN_VALUE_INCORRECT_ERROR)

        # validate the maximum x value
        if not max_value:
            is_values_valid = False
            self.max_error_label.setText(cons.MAX_VALUE_EMPTY_ERROR)
        else:
            try:
                # convert the power operator to python compatible operator
                max_value = max_value.replace("^", "**")
                max_value = float(eval(max_value))
            except Exception as e:
                is_values_valid = False
                self.max_error_label.setText(cons.MAX_VALUE_INCORRECT_ERROR)

        # validate the range between minimum x value and the maximum x value
        if is_values_valid and (max_value == min_value or max_value < min_value):
            self.min_error_label.setText(cons.MIN_MAX_ERROR)
            self.max_error_label.setText(cons.MIN_MAX_ERROR)
            is_values_valid = False

        return (min_value, max_value) if is_values_valid else None

    def reset_errors(self):
        """
        Reset the labels signifying the different error resulting from user input
        """
        self.func_error_label.setText("")
        self.min_error_label.setText("")
        self.max_error_label.setText("")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()
