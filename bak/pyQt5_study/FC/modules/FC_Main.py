# -*- coding: utf-8 -*-

import sys

import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

CalUi = '../_uiFiles/calculator.ui'


class MainDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(CalUi, self)

        self.num_pushButton_1.clicked.connect(self.NumClicked)

    def NumClicked(self):
        print('나 클릭됐다~~')

app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()
app.exec_()
