from PyQt6.QtWidgets import *
from gui import *
import csv
import os


class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        """
        Initializes the Logic class. Sets up the UI and
        connects the buttons to methods
        :param

        """
        super().__init__()
        self.setupUi(self)

        self.score_labels_entries: list[tuple[QLabel, QLineEdit]] = [
            (self.score_one_label, self.score_one_entry),
            (self.score_two_label, self.score_two_entry),
            (self.score_three_label, self.score_three_entry),
            (self.score_four_label, self.score_four_entry)
        ]

        self.message_box.setText('Click SUBMIT after entering name and number of attempts')
        self.message_box.setStyleSheet("color: red")
        self.submit_button.clicked.connect(lambda: self.submit())
        self.calculate_button.clicked.connect(lambda: self.calculate())
        self.calculate_button.setVisible(False)
        self.clear_button.setVisible(False)
        self.clear_button.clicked.connect(lambda: self.clear())

        for label, entry in self.score_labels_entries:
            label.setVisible(False)
            entry.setVisible(False)

    def submit(self) -> None:
        """
        Handles the submit button
        Validates student name and number of attempts
        :param student_name: Students name
        :param attempts: Holds number of attempts
        """
        self.message_box.setText('Please fill your scores and click CALCULATE')
        self.message_box.setStyleSheet("color: red")

        try:
            student_name: str = self.student_name_entry.text()
            if student_name == '':
                raise ValueError('Name field cannot be blank!')
        except ValueError as e:
            self.message_box.setText(str(e))
            self.message_box.setStyleSheet("color: red")
            return

        try:
            attempts: int = int(self.attempts_field.text())
            if attempts < 1 or attempts > 4:
                raise TypeError('Number of attempts must be between 1 and 4')
        except ValueError:
            self.message_box.setText('Number of attempts must be a whole number')
            self.message_box.setStyleSheet("color: red")
            return
        except TypeError as e:
            self.message_box.setText(str(e))
            self.message_box.setStyleSheet("color: red")
            return

        for i in range(attempts):
            label, entry = self.score_labels_entries[i]
            label.setVisible(True)
            entry.setVisible(True)
        self.calculate_button.setVisible(True)
        self.submit_button.setVisible(False)

    def calculate(self) -> None:
        """
        Handles the calculate button
        Validates scores, determines highest and lowest and letter grade
        Data is written to a csv file that is created if none exist
        :param scores: list to set initial score to 0
        :param highest_score: Highest score entered
        :param lowest_score: Lowest score entered
        :param letter_grade: Grade based on score
        """
        scores: list[float] = [0, 0, 0, 0]

        try:
            attempts: int = int(self.attempts_field.text())
            for i in range(attempts):
                _, entry = self.score_labels_entries[i]
                score: float = float(entry.text())
                if score < 0 or score > 100:
                    raise TypeError("Value must be between 0 and 100")
                scores[i] = score

        except ValueError:
            self.message_box.setText('Score must be a whole number')
            self.message_box.setStyleSheet("color: red")
            return
        except TypeError as e:
            self.message_box.setText(str(e))
            self.message_box.setStyleSheet("color: red")
            return

        highest_score: float = max(scores)
        lowest_score: float = min(scores)
        self.high_score.setText(f'{highest_score}')
        self.low_score.setText(f'{lowest_score}')

        if highest_score >= 90:
            self.letter_grade.setText('A!')
            letter_grade: str = 'A'
        elif 80 <= highest_score < 90:
            self.letter_grade.setText('B!')
            letter_grade: str = 'B'
        elif 70 <= highest_score < 80:
            self.letter_grade.setText('C!')
            letter_grade: str = 'C'
        elif 60 <= highest_score < 70:
            self.letter_grade.setText('D!')
            letter_grade: str = 'D'
        else:
            self.letter_grade.setText('F!')
            letter_grade: str = 'F'

        student_total: list[str] = [
            self.student_name_entry.text(),
            str(scores[0]),
            str(scores[1]),
            str(scores[2]),
            str(scores[3]),
            str(highest_score),
            letter_grade
        ]

        with open('grades.csv', 'a', newline='') as grades_output:
            writer = csv.writer(grades_output)
            if os.stat('grades.csv').st_size == 0:
                writer.writerow(
                    ['Name', 'Score 1', 'Score 2', 'Score 3', 'Score 4', 'Final Score', 'Letter Grade'])
            writer.writerow(student_total)

        self.message_box.setText(
            'Grades calculated and entered into grades.csv! Press CLEAR to enter new student data!')
        self.message_box.setStyleSheet("color: Green")
        self.clear_button.setVisible(True)

    def clear(self) -> None:
        """
             Handles the clear button click event.
             Clears all fields and sets everything back to initial state
             """
        attempts: int = int(self.attempts_field.text())
        for i in range(attempts):
            label, entry = self.score_labels_entries[i]
            entry.clear()
            label.setVisible(False)
            entry.setVisible(False)

        self.letter_grade.clear()
        self.high_score.clear()
        self.low_score.clear()
        self.attempts_field.clear()
        self.student_name_entry.clear()
        self.calculate_button.setVisible(False)
        self.submit_button.setVisible(True)
        self.message_box.setText('Click SUBMIT after entering name and number of attempts')
        self.message_box.setStyleSheet("color: red")
