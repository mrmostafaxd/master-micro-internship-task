from PySide2.QtWidgets import QLabel, QLineEdit, QPushButton, QWidget
from PySide2.QtCore import QRegExp
from PySide2.QtGui import QFont, QDoubleValidator, QRegExpValidator
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
import matplotlib
matplotlib.use('Qt5Agg')


class CustomCanvas(FigureCanvas):
    """
    A custom canvas widget for displaying a Matplotlib plot.
    """

    def __init__(self, width=5, height=4, dpi=100):
        """
        Initializes the CustomCanvas object.

        Parameters
        ----------
        width : float
            The width of the plot in inches.
        height : float
            The height of the plot in inches.
        dpi : float
            The resolution of the plot in dots per inch.
        """

        self.axes = None

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)

        self.default_config()

    def replot_function(self, x, y, function_str):
        """Clear the current plot and re-plot the function with the given x and y values.

        Parameters:
        ----------
        x : np.ndarray
            The x values of the function to plot
        y : np.ndarray
            The y values of the function to plot
        function_str : str 
            f(x) as a string
        """

        self.default_config()
        self.axes.set_title(f"f(x) = {function_str}")

        self.axes.plot(x, y)

        # to automatically adjust the plot so that it stays inside the figure area
        self.fig.tight_layout()

        self.draw()

    def default_config(self):
        """
        Clear the plot and set the default configuration for the plot.
        """

        # clear the graph
        if self.axes:
            self.axes.cla()
        self.fig.clf()

        # reconfigure the graph and the label
        self.axes = self.fig.add_subplot(111)
        self.axes.grid()
        self.axes.set_xlabel("X")
        self.axes.set_ylabel('f(X)')

        # to automatically adjust the plot so that it stays inside the figure area
        self.fig.tight_layout()

        self.draw()


class CustomLabel(QLabel):
    """
    A custom label widget with font size and color options.
    """

    def __init__(self, text, font_size=None, font_color=None):
        """
        Initializes the CustomLabel object.

        Parameters
        ----------
        text: str
            The text to display on the label
        font_size : int 
            The size of the font used for the label
        font_color : str 
            The color of the font used for the label
        """

        super().__init__(text)

        if font_size:
            self.set_font_size(font_size)

        if font_color:
            self.set_font_color(font_color)

    def set_font_size(self, font_size):
        """
        Sets the font size of the label.

        Parameters
        ----------
        font_size : int 
            The size of the font
        """
        font: QFont = self.font()
        font.setPointSize(font_size)
        self.setFont(font)

    def set_font_color(self, font_color):
        """
        Sets the font color of the label.

        Parameters
        ----------
        font_color : str
            The color of the font
        """
        self.setStyleSheet(f"color: {font_color}")


class CustomPushButton(QPushButton):
    """
    A custom push button widget with font size option.
    """

    def __init__(self, text, font_size=None):
        """
        Initializes the CustomPushButton object.

        Parameters
        ----------
        text : str
            The text to display on the button
        font_size : int
            The size of the font used for the button
        """
        super().__init__(text)

        if font_size:
            self.set_font_size(font_size)

    def set_font_size(self, font_size):
        """
        Sets the font size of the button.

        Parameters
        ----------
        font_size : int
            The size of the font
        """
        font: QFont = self.font()
        font.setPointSize(font_size)
        self.setFont(font)


class CustomLineEdit(QLineEdit):
    """
    A custom line edit widget with font size and input type options.
    """

    def __init__(self, font_size=None, float_only=False):
        """
        Initializes the CustomLineEdit object.

        Parameters
        ----------
        font_size : int
            The size of the font used for the line edit
        float_only: bool
            A boolean value indicating whether to limit the input type to floats only
        """
        super().__init__()

        if font_size:
            self.set_font_size(font_size)

        if float_only:
            # To stop the user from inputting non-float value
            self.setValidator(QDoubleValidator())

            # To replace the default power operator from "e" to "^"
            validator = QRegExpValidator(
                QRegExp("[-+]?[0-9]*\\.?[0-9]+([\\^][-+]?[0-9]+)?"))
            notation = validator.regExp().pattern()
            notation = notation.replace("e", "^")
            validator.setRegExp(QRegExp(notation))
            self.setValidator(validator)

    def set_font_size(self, font_size):
        """
        Sets the font size of the line edit.

        Parameters
        ----------
        font_size : int
            The size of the font
        """
        font: QFont = self.font()
        font.setPointSize(font_size)
        self.setFont(font)
