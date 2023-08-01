"""
Final TS Project
Calculator
"""
import PySide6.QtCore

# Imports
import re
from PySide6 import QtCore, QtWidgets, QtGui
import random
import sys


# Gui
class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        """
        function:
        defines variables and sets up gui
        """
        super().__init__()
        # Layout
        self.step = None
        self.layout = QtWidgets.QVBoxLayout(self)

        # Input box
        self.calculator_input = QtWidgets.QLineEdit()
        self.layout.addWidget(self.calculator_input)
        self.calculator_input.placeholderText()
        self.calculator_input.setPlaceholderText("Enter an equation you would like solved")

        # layout
        self.text = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.text)
        self.layout.setSpacing(1)
        self.layout.setContentsMargins(10, 10, 10, 10)

        # Buttons
        self.answer_button = QtWidgets.QPushButton("Answer")
        self.layout.addWidget(self.answer_button)
        self.answer_button.setContentsMargins(0, -10, -10, 0)
        self.answer_button.clicked.connect(self.answer_getter)

        # Dropdown for process
        self.process_label = QtWidgets.QLabel("Process")
        self.layout.addWidget(self.process_label)
        self.process_label.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.process_dropdown = QtWidgets.QComboBox()
        self.layout.addWidget(self.process_dropdown)

    @QtCore.Slot()
    def answer_getter(self):
        """
        function:
        Does the math and displays the answer
        :return: 
        none
        """
        # Clears the process for new process
        self.process_dropdown.clear()
        equation = self.calculator_input.text()
        answer = main(equation)
        self.text.setText(str(answer))
        self.calculator_input.setText("")
        self.process_dropdown.addItems(process)

    def math_process(self):
        """
        function:
        Puts the process to solve the equation into a dropdown tab
        :return: 
        none
        """
        # Sets up the process and add it to the window
        for i in range(len(process)):
            self.step = QtWidgets.QLabel(process[i], alignment=QtCore.Qt.AlignCenter)
            self.layout.addWidget(self.step)


# Functions
def calc_add(numbers):
    """
    function:
    adds
    :parameter
    numbers: list
    :return
    new_num
    """

    new_num = numbers[0] + numbers[1]
    return new_num


def calc_sub(numbers):
    """
    function:
    subtracts
    :parameter
    numbers: list
    :return
    new_num
    """
    new_num = numbers[0] - numbers[1]
    return new_num


def calc_mult(numbers):
    """
    function:
    multiplies
    :parameter
    numbers: list
    :return
    new_num
    """
    new_num = numbers[0] * numbers[1]
    return new_num


def calc_div(numbers):
    """
    function:
    divides
    :parameter
    numbers: list
    :return
    new_num
    """
    if numbers[1] == 0:
        return "Cannot divide by zero"
    new_num = numbers[0] / numbers[1]
    return new_num


def find_equation(operator, *numbers):
    """
    function:
    finds the correct equation
    :parameter
    operator: str
    numbers: floats
    :return
    new_num
    """
    if operator == "*":
        new_num = calc_mult(numbers)
    elif operator == "/":
        new_num = calc_div(numbers)
    elif operator == "- ":
        new_num = calc_sub(numbers)
    elif operator == "+":
        new_num = calc_add(numbers)

    return new_num, numbers


def new_index(new_num, num_replaced, index):
    """
    function:
    The main function that takes the users input and calculates it
    :parameter
    new_num: float
    num_replaced: list
    index: int
    :return
    none
    """
    for i in num_replaced:
        numbers_list.remove(i)
    numbers_list.insert(index, new_num)


def solve(index):
    """
    function:
    uses the other 2 functions to solve the equation
    :param index: int
    :return:
    """
    try:
        new_num, num_replaced = find_equation(operators[index], numbers_list[index], numbers_list[index + 1])
    except IndexError:
        return "Invalid equation"
    if isinstance(new_num, str):
        return new_num
    process.append(f"{num_replaced[0]} {operators[index]} {num_replaced[1]} = \n{new_num}")
    new_index(new_num, num_replaced, index)
    operators.remove(operators[index])


# Variables
def main(equation):
    """
    function:
    The main function that takes the users input and calculates it
    :return
    answer
    """
    # Globals
    global operators
    global numbers_list
    global process

    numbers_list = []
    operators = []
    process = []

    # List setup and user input
    operators_tuple = ("*", "/", "-", "+", "- ")
    equation = re.split("(\*|- |/|\+|\s|-(?<!\d)[,.]|[,.](?!\d))", equation)

    for i in equation:
        try:
            i = float(i)
            numbers_list.append(i)
        except:
            # Negative check
            if len(i) > 2:
                for j in range(len(i)):
                    if i[j].isdigit():
                        j = float(i[j])
                        numbers_list.append(j)
                    elif i[j] == "-" and i[j + 1] == "-":
                        operators.append("- ")
                        j = float(i[j + 1] + i[j + 2])
                        numbers_list.append(j)
                        break
                    elif i[j] == "-":
                        operators.append("- ")

            if i in operators_tuple:
                operators.append(i)
            else:
                equation.remove(i)
    # Check for any string variables
    if not operators:
        return "Invalid equation"
    for i in operators:
        if i not in operators_tuple:
            return "Invalid equation"

    # Main equation run
    j = 0
    error = None
    while j < len(operators):
        if not error is None:
            return error
        elif operators[j] == "*":
            error = solve(j)
            j = 0
        elif operators[j] == "/":
            error = solve(j)
            j = 0
        elif "*" in operators or "/" in operators:
            j += 1
        elif "+" == operators[j] or "- " == operators[j]:
            error = solve(j)
            j = 0
        else:
            j += 1

    return numbers_list[0]


# Global lists
process = []
numbers_list = []
operators = []

while __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = MyWidget()
    window.resize(500, 200)
    window.show()

    # answer = main()
    # print(f"The answer is {answer}")
    sys.exit(app.exec())
