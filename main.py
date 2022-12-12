from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtCore import Qt
from PyQt5 import uic
import sys

class EditorGUI(QMainWindow):

    def __init__(self):
        self.current_file = None
        self.stuff = str()
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
        # Shortcuts
        self.shortcut_open = QShortcut(QKeySequence('ctrl+o'), self)
        self.shortcut_open.activated.connect(self.open_file)
        self.shortcut_new = QShortcut(QKeySequence('ctrl+n'), self)
        self.shortcut_new.activated.connect(self.new_file)
        self.shortcut_save = QShortcut(QKeySequence('ctrl+s'), self)
        self.shortcut_save.activated.connect(self.save_file)
        self.shortcut_save_as = QShortcut(QKeySequence('ctrl+shift+s'), self)
        self.shortcut_save_as.activated.connect(self.save_file_as)

    def change_size(self, size):
        self.plainTextEdit.setFont(QFont("Arial", size))

    def check_stuff(self):
        return True if self.plainTextEdit.toPlainText() == self.stuff else False

    def open_file(self):
        if not self.check_stuff():
            # Save file dialog box
            dialog = QMessageBox()
            dialog.setText("Do you want to save your work?")
            dialog.addButton(QPushButton("Yes"), QMessageBox.YesRole)  # 0
            dialog.addButton(QPushButton("No"), QMessageBox.NoRole)  # 1
            dialog.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)  # 2

            answer = dialog.exec_()

            if answer == 0:
                self.save_file()
            elif answer == 2:
                return 0

        options = QFileDialog.Options()
        filename = QFileDialog.getOpenFileName(self, "Open File", "Files\\", "Text Files (*.txt);;Python Files (*.py);;All files (*)", options=options)[0]
        if filename != "":
            with open(filename, "r") as file:
                stuff = file.read()
                self.plainTextEdit.setPlainText(stuff)
                self.current_file = filename
                self.stuff = stuff

    def save_file(self):
        if self.current_file is None:
            self.save_file_as()
        else:
            with open(self.current_file, 'w') as file:
                stuff = self.plainTextEdit.toPlainText()
                file.write(stuff)
                self.stuff = stuff

    def save_file_as(self):
        options = QFileDialog.Options()
        filename = QFileDialog.getSaveFileName(self, "Save File", "Files\\file", "Text Files (*.txt);;Python Files (*.py);;All files (*)", options=options)[0]
        if filename != "":
            with open(filename, "w") as file:
                stuff = self.plainTextEdit.toPlainText()
                file.write(stuff)
                self.current_file = filename
                self.stuff = stuff

    def new_file(self):
        # If the file is empty or no change has been made --> don't save
        if self.plainTextEdit.toPlainText() == "" or self.check_stuff():
            self.plainTextEdit.setPlainText("")
            self.current_file = None
            self.stuff = str()
            return 0


        # Save file dialog box
        dialog = QMessageBox()
        dialog.setText("Do you want to save your work?")
        dialog.addButton(QPushButton("Yes"), QMessageBox.YesRole)  # 0
        dialog.addButton(QPushButton("No"), QMessageBox.NoRole)  # 1
        dialog.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)  # 2

        answer = dialog.exec_()

        if answer == 0:
            self.save_file()
        elif answer == 2:
            return 0
        self.plainTextEdit.setPlainText("")
        self.current_file = None
        self.stuff = str()

    def closeEvent(self, event):
        if self.plainTextEdit.toPlainText() == "": # If file is empty, just exit
            sys.exit()
        elif self.check_stuff(): # If no change has been made, just exit
            sys.exit()

        # Save File dialog box
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