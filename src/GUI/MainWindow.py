"""
    :copyright: Copyright 2022 by the FreePDM team
    :license:   MIT License.
"""

import os
from pathlib import Path
import sys

from PySide2.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader

sys.path.append(os.fspath(Path(__file__).resolve().parents[1] / 'Skeleton'))

from directorymodel import DirectoryModel


class MainWindow(QMainWindow):
    def __init__(self):
        self.dir = os.path.expanduser('~')
        if len(sys.argv) == 2:
            self.dir = sys.argv[1]
        print("self.dir =", self.dir)

        super(MainWindow, self).__init__()
        self.load_ui()
        self.load_data()
    
    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parents[1] / "GUI/MainWindow.ui")
        print(path)
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        self.ui.setGeometry(50, 40, 800, 600)
        # Some change below based on https://pythonprogramming.net/basic-gui-pyqt-tutorial/
        self.ui.setWindowTitle("FreePDM")  # Done in ui file
        # self.ui.setWindowIcon(QtGui.QIcon(os.fspath(Path(__file__).resolve().parents[1] / "ui/logos/O_logo-32x32.png")))  # Probably done in ui file OSX don't show icon
        self.ui.show()
        ui_file.close()

    def load_data(self):
        dm = DirectoryModel(self.dir)
        row = 0
        self.ui.tableWidget.setRowCount(dm.size())
        for item in dm.dirList:
            self.ui.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(item["dirOrFile"]))
            self.ui.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(item["filename"]))
            self.ui.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(item["size"]))
            row=row+1


def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    widget = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    mainw = main()