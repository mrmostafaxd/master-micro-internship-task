import pytest
from PySide2.QtTest import QTest
from PySide2.QtCore import Qt
import numpy as np

import main
import constants as cons


def input_values_and_click(qtbot, window, func_input=None, min_input=None, max_input=None, can_click=True):
    """
    Simulates user input in the input fields and optionally clicks the plot button.

    Parameters
    ----------
    - qtbot: Pytest fixture to handle Qt event loop integration for GUI testing.
    - window: The MainWindow instance.
    - func_input (optional): The input for the function field. 
    - min_input (optional): The input for the minimum X value field. 
    - max_input (optional): The input for the maximum X value field. 
    - can_click (optional): Indicates whether to simulate clicking the plot button. 
    """

    # Function input field
    if func_input is not None:
        QTest.keyClicks(window.function_input, func_input)

    # Minimum X value input field
    if min_input is not None:
        QTest.keyClicks(window.min_val_input, min_input)

    # Maximum X value input field
    if max_input is not None:
        QTest.keyClicks(window.max_val_input, max_input)

    # Plot button
    if can_click:
        qtbot.mouseClick(window.plot_button, Qt.LeftButton)


@pytest.fixture
def main_window(qtbot):
    """
    Fixture to create and return an instance of the MainWindow class.

    Parameters
    ----------
    - qtbot: Pytest fixture to handle Qt event loop integration for GUI testing.

    Returns
    -------
    - MainWindow instance: An instance of the MainWindow class.
    """
    window = main.MainWindow()
    window.show()

    qtbot.addWidget(window)

    return window


@pytest.fixture
def main_window_after_valid_input(qtbot, main_window):
    """
    Fixture to set up the MainWindow instance after valid input is entered.

    Parameters
    ----------
    - qtbot: Pytest fixture to handle Qt event loop integration for GUI testing.
    - main_window: The main_window fixture that provides the MainWindow instance.

    Returns
    -------
    - Tuple: A tuple containing the MainWindow instance, input values, and plotted x and y values.
      - main_window: The MainWindow instance.
      - func_test_val: The input function value.
      - min_test_val: The input minimum x value.
      - max_test_val: The input maximum x value.
      - x: The array of x values used for plotting.
      - y: The array of corresponding y values calculated from the input function.
    """
    func_test_val = "x^2+2"
    func_test_val_modified = func_test_val.replace("^", "**")
    min_test_val = "-10"
    max_test_val = "10"

    # the values that will test the validity of the graph
    x = np.linspace(float(min_test_val), float(max_test_val), 1000)
    y = eval(func_test_val_modified)

    input_values_and_click(
        qtbot, main_window, func_test_val, min_test_val, max_test_val)

    return (main_window, func_test_val, min_test_val, max_test_val, x, y)


###################################
######## Empty Input Tests ########
###################################

def test_main_window_visible_when_opened(main_window):
    """
    Test that the main window is visible when opened.

    Parameters
    ----------
    - main_window: The main_window fixture that provides the MainWindow instance.
    """

    # Assert that the main window is visible
    assert main_window.isVisible()


def test_default_widget_values(main_window):
    """
    Test that the default values of the input fields and error labels are empty,
    no lines are drawn on the canvas, and the Matplotlib toolbar icons are disabled.

    Parameters
    ----------
    - main_window: The main_window fixture that provides the MainWindow instance.
    """

    # Assert that the function input and its corresponding error label are empty
    assert main_window.function_input.text() == ""
    assert main_window.func_error_label.text() == ""

    # Assert that the maximum X value input and its corresponding error label are empty
    assert main_window.min_val_input.text() == ""
    assert main_window.min_error_label.text() == ""

    # Assert that the minimum X value input and its corresponding error label are empty
    assert main_window.max_val_input.text() == ""
    assert main_window.max_error_label.text() == ""

    # Assert that no graph is plotted
    assert len(main_window.canvas.axes.lines) == 0

    # Assert that the Matplotlib toolbar icons are disabled
    assert main_window.toolbar.isEnabled() == False


def test_clicking_plot_button_without_any_input(qtbot, main_window):
    """
    Test the behavior of clicking the plot button without providing any input.

    Parameters
    ----------
    - qtbot: Pytest fixture to handle Qt event loop integration for GUI testing.
    - main_window: The main_window fixture that provides the MainWindow instance.
    """

    # Simulates clicking the plot button without entering any values
    input_values_and_click(qtbot, main_window)

    # Assert that the appropriate error messages are displayed for each input field
    assert main_window.func_error_label.text() == cons.FUNC_VALUE_EMPTY_ERROR
    assert main_window.min_error_label.text() == cons.MIN_VALUE_EMPTY_ERROR
    assert main_window.max_error_label.text() == cons.MAX_VALUE_EMPTY_ERROR

    # Assert that no graph is plotted
    assert len(main_window.canvas.axes.lines) == 0

    # Assert that the Matplotlib toolbar icons are disabled
    assert main_window.toolbar.isEnabled() == False


###################################
######## Valid Input Tests ########
###################################

def test_valid_input_shows_the_correct_graph_and_enables_toolbar(main_window_after_valid_input):
    """
    Test that providing valid input results in the correct graph being drawn on the canvas
    and enables the Matplotlib toolbar icons.

    Parameters
    ----------
    - main_window_after_valid_input: A fixture providing the MainWindow instance and relevant input values.
    """

    # Retrieve the MainWindow instance and relevant input values from the fixture
    mw, func_test_val, min_test_val, max_test_val, x, y = main_window_after_valid_input

    # Assert that the canvas draws a single graph
    assert len(mw.canvas.axes.lines) == 1

    # Assert that the graph title matches the provided function input
    assert mw.canvas.axes.get_title() == f"f(x) = {func_test_val}"

    # Assert that the graph drawn on the canvas has the correct x and y values
    assert np.array_equal(mw.canvas.axes.lines[0].get_xdata(), x)
    assert np.array_equal(mw.canvas.axes.lines[0].get_ydata(), y)

    # Assert that the Matplotlib toolbar icons are enabled
    assert mw.toolbar.isEnabled() == True


def test_valid_input_shows_no_error(main_window_after_valid_input):
    """
    Test that providing valid input results in no error messages displayed on the MainWindow.

    Parameters
    ----------
    - main_window_after_valid_input: A fixture providing the MainWindow instance and relevant input values.
    """

    # Retrieve the MainWindow instance from the fixture
    mw = main_window_after_valid_input[0]

    # Asserts that no error messages are displayed for the function input,
    #  minimum X value input, and maximum X value input
    assert mw.func_error_label.text() == ""
    assert mw.min_error_label.text() == ""
    assert mw.max_error_label.text() == ""


######################################
######## Function Input Tests ########
######################################

@pytest.mark.parametrize("func_test_val, expected_error", [
    ("", cons.FUNC_VALUE_EMPTY_ERROR),
    ("z^2+2", cons.FUNC_VALUE_INCORRECT_ERROR),
    ("asdwrewfewf", cons.FUNC_VALUE_INCORRECT_ERROR)
])
def test_function_input_errors_and_no_graph(qtbot, main_window, func_test_val, expected_error):
    """
    Test the behavior of the function input field with valid minimum and maximum X values
    for different error cases.

    Parameters
    ----------
    - qtbot: Pytest fixture to handle Qt event loop integration for GUI testing.
    - main_window: The main_window fixture that provides the MainWindow instance.
    - func_test_val: The function input value to test.
    - expected_error: The expected error message for the specific input case.
    """
    # Set the function input field with the provided test value and click the plot button
    input_values_and_click(qtbot, main_window, func_test_val, "-10", "10")

    # Assert that the appropriate error message is displayed for the function input field
    assert main_window.func_error_label.text() == expected_error

    # Assert that no graph is plotted
    assert len(main_window.canvas.axes.lines) == 0

    # Assert that the Matplotlib toolbar icons are disabled
    assert main_window.toolbar.isEnabled() == False


###################################################
######## Minimum and Maximum X Input Tests ########
###################################################

@pytest.mark.parametrize("user_input_min_max_test_val, apparent_min_max_test_val, field_type", [
    ("xacsfasfasf", "", "min"),
    ("12", "12",  "min"),
    ("-12.2", "-12.2", "min"),
    ("-dsafvasfas", "-", "min"),
    ("13^2", "13^2", "min"),
    ("wdwdw^wwfwf", "", "min"),
    ("13^2^3", "13^23", "min"),
    ("xacsfasfasf", "", "max"),
    ("12", "12",  "max"),
    ("-12.2", "-12.2", "max"),
    ("-dsafvasfas", "-", "max"),
    ("13^2", "13^2", "max"),
    ("wdwdw^wwfwf", "", "max"),
    ("13^2^3", "13^23", "max"),
])
def test_min_max_val_input_field(qtbot, main_window, user_input_min_max_test_val, apparent_min_max_test_val, field_type):
    """
    Test the behavior of the minimum X and maximum X value input fields
    by entering different types of values.

    Parameters
    ----------
    - qtbot: Pytest fixture to handle Qt event loop integration for GUI testing.
    - main_window: The main_window fixture that provides the MainWindow instance.
    - user_input_min_max_test_val: The user input value to test.
    - apparent_min_max_test_val: The expected value to be displayed in the input field.
    - field_type: The type of the input field (either 'min' or 'max').
    """

    # Set the input field with the provided user input value
    #  then asserts that the value displayed in the input field matches
    #  the expected apparent value.
    if field_type == "min":
        input_values_and_click(
            qtbot, main_window, min_input=user_input_min_max_test_val)
        assert main_window.min_val_input.text() == apparent_min_max_test_val
    elif field_type == "max":
        input_values_and_click(
            qtbot, main_window, max_input=user_input_min_max_test_val)
        assert main_window.max_val_input.text() == apparent_min_max_test_val
    else:
        assert False


@pytest.mark.parametrize("min_test_val, max_test_val, expected_error, field_type", [
    ("", "10", cons.MIN_VALUE_EMPTY_ERROR, "min"),
    ("+", "10", cons.MIN_VALUE_INCORRECT_ERROR, "min"),
    ("-", "10", cons.MIN_VALUE_INCORRECT_ERROR, "min"),
    ("-10", "", cons.MAX_VALUE_EMPTY_ERROR, "max"),
    ("-10", "+", cons.MAX_VALUE_INCORRECT_ERROR, "max"),
    ("-10", "-", cons.MAX_VALUE_INCORRECT_ERROR, "max")
])
def test_min_max_val_input_errors_and_no_graph(qtbot, main_window, min_test_val, max_test_val, expected_error, field_type):
    """
    Test the behavior of the minimum X and maximum X value input fields by entering invalid and empty values.

    Parameters
    ----------
    - qtbot: Pytest fixture to handle Qt event loop integration for GUI testing.
    - main_window: The main_window fixture that provides the MainWindow instance.
    - min_test_val: The value to be set in the minimum X value input field.
    - max_test_val: The value to be set in the maximum X value input field.
    - expected_error: The expected error message to be displayed.
    - field_type: The type of the input field (either 'min' or 'max').
    """

    # Set the input fields with the provided minimum and maximum X values
    # then click on the plot button
    input_values_and_click(qtbot, main_window, "x^2",
                           min_test_val, max_test_val)

    # Assert that the expected error message is displayed in the corresponding error label
    if field_type == "min":
        assert main_window.min_error_label.text() == expected_error
    elif field_type == "max":
        assert main_window.max_error_label.text() == expected_error
    else:
        assert False

    # Assert that no graph is plotted
    assert len(main_window.canvas.axes.lines) == 0

    # Assert that the Matplotlib toolbar icons are disabled
    assert main_window.toolbar.isEnabled() == False


@pytest.mark.parametrize("min_test_val, max_test_val", [
    ("10", "-10"),
    ("5", "5")
])
def test_invalid_min_max_range_and_no_graph(qtbot, main_window, min_test_val, max_test_val):
    """
        Test if minimum X value greater than or equal maximum X value give error to the user.

    Parameters
    ----------
    - qtbot: Pytest fixture to handle Qt event loop integration for GUI testing.
    - main_window: The main_window fixture that provides the MainWindow instance.
    - min_test_val: The value to be set in the minimum X value input field.
    - max_test_val: The value to be set in the maximum X value input field.
    """
    # Set the input fields with the provided minimum and maximum X values
    #  then click on the plot button
    input_values_and_click(qtbot, main_window, "x^2",
                           min_test_val, max_test_val)

    # Assert that the expected error message is displayed in the corresponding error label
    assert main_window.min_error_label.text() == cons.MIN_MAX_ERROR
    assert main_window.max_error_label.text() == cons.MIN_MAX_ERROR

    # Assert that no graph is plotted
    assert len(main_window.canvas.axes.lines) == 0

    # Assert that the Matplotlib toolbar icons are disabled
    assert main_window.toolbar.isEnabled() == False
