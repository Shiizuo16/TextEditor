from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5 import uic
import sys

class EditorGUI(QMainWindow):

    def __init__(self):
        self.current_file = None
        super(EditorGUI, self).__init__()
        uic.loadUi("src\\editor.ui", self)
        self.show()

        self.setWindowTitle('Text Editor by Yash')      # Window title

        # Editor buttons - Font
        self.action12.triggered.connect(lambda: self.change_size(12))
        self.action18.triggered.connect(lambda: self.change_size(18))
        self.action24.triggered.connect(lambda: self.change_size(24))
        # File buttons
        self.actionNew.triggered.connect(self.new_file)
        self.actionOpen_2.triggered.connect(self.open_file)
        self.actionSave.triggered.connect(self.save_file)
        self.actionSave_As.triggered.connect(self.save_file_as)
        self.actionClose.triggered.connect(self.closeEvent)

    def change_size(self, size):
        self.plainTextEdit.setFont(QFont("Arial", size))

    def open_file(self):
        options = QFileDialog.Options()
        filename = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;Python Files (*.py);;All files (*)", options=options)[0]
        if filename != "":
            with open(filename, "r") as file:
                self.plainTextEdit.setPlainText(file.read())
            self.current_file = filename

    def save_file(self):
        if self.current_file is None:
            print('file does not exist')
            self.save_file_as()
        else:
            print('file exists')
            with open(self.current_file, 'w') as file:
                print('file opened')
                stuff = self.plainTextEdit.toPlainText()
                print(stuff)
                file.write(stuff)
                print('file written')
        print('file saved')

    def save_file_as(self):
        options = QFileDialog.Options()
        filename = QFileDialog.getSaveFileName(self, "Save File", "Files\\file", "Text Files (*.txt);;Python Files (*.py);;All files (*)", options=options)[0]
        if filename != "":
            with open(filename, "w") as file:
                stuff = self.plainTextEdit.toPlainText()
                print(stuff)
                file.write(stuff)
            self.current_file = filename

    def new_file(self):
        dialog = QMessageBox()
        dialog.setText("Do you want to save your work?")
        dialog.addButton(QPushButton("Yes"), QMessageBox.YesRole)  # 0
        dialog.addButton(QPushButton("No"), QMessageBox.NoRole)  # 1
        dialog.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)  # 2

        answer = dialog.exec_()

        if answer == 0:
            self.save_file()
            self.plainTextEdit.setPlainText("")
            self.current_file = None
        elif answer == 1:
            self.plainTextEdit.setPlainText("")
            self.current_file = None

    def closeEvent(self, event):
        if self.plainTextEdit.toPlainText() == "":
            sys.exit()
        dialog = QMessageBox()
        dialog.setText("Do you want to save your work?")
        dialog.addButton(QPushButton("Yes"), QMessageBox.YesRole)           # 0
        dialog.addButton(QPushButton("No"), QMessageBox.NoRole)             # 1
        dialog.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)     # 2

        answer = dialog.exec_()

        if answer == 0:
            self.save_file()
            event.accept()
        elif answer == 1:
            sys.exit()
        elif answer == 2:
            event.ignore()


def main():
    app = QApplication([])
    window = EditorGUI()
    app.exec_()

if __name__ == '__main__':
    main()