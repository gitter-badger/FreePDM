"""
    :copyright: Copyright 2022 by the FreePDM team
    :license:   MIT License.
"""

import os
from pathlib import Path
import sys

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2.QtGui import QPixmap 
from PySide2.QtWidgets import QApplication, QDialog
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader

sys.path.append(os.fspath(Path(__file__).resolve().parents[1] / 'skeleton'))

from itemdatamodel import ItemDataModel


class EditItem(QDialog):
    def __init__(self, file):
        super(EditItem, self).__init__()
        self.file = file
        print("File is ", self.file)
        self.idm = ItemDataModel(self.file)

        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parents[1] / "gui/EditItem.ui")
        print(path)
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        # Some change below based on https://pythonprogramming.net/basic-gui-pyqt-tutorial/
        # self.ui.setWindowIcon(QtGui.QIcon(os.fspath(Path(__file__).resolve().parents[1] / "ui/logos/O_logo-32x32.png")))  # Probably done in ui file OSX don't show icon

        self.ui.setWindowTitle("Edit Item")  # Done in ui file

        self.ui.nameEdit.setReadOnly(True)
        self.ui.userNameEdit.setReadOnly(True)
        self.ui.dateEdit.setReadOnly(True)
        self.ui.weightEdit.setReadOnly(True)
        self.ui.unitEdit.setReadOnly(True)
        self.ui.saveButton.clicked.connect(self.save_button)
        self.ui.okButton.clicked.connect(self.push_ok_button)
        # self.ui.done(self.done)

        # When file is read-only don't activate the Ok button
        # Unfortunately this doesn't work for mine OS (Xbuntu)
        # if os.access(self.file, os.R_OK) == True:
            # self.ui.saveButton.setEnabled(False)

        self.ui.nameEdit.setText(self.idm.document_properties["Label"])
        self.ui.dateEdit.setText(self.idm.document_properties["CreationDate"])
        if 'Unit' in self.idm.document_properties:
            self.ui.unitEdit.setText(self.idm.document_properties['Unit'])
        if "thumbnail" in self.idm.document_properties:
            pixmap = QtGui.QPixmap(self.idm.thumbnail)
            self.ui.lbl.setPixmap(pixmap.scaled(256, 256))

    def save_button(self):
        self.ui.hide()
    
    def push_ok_button(self):
        self.ui.hide()

    # def done(self):
    #     self.ui.hide()



def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    # Opening a FCStd file with the command line
    if len(sys.argv) == 2:
        fcfile = sys.argv[1]
    else:
        fcfile = ''
    mainwindow = EditItem(fcfile)
    mainwindow.ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    mainw = main()
