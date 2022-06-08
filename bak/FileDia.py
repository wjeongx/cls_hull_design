import sys
from PyQt5.QtWidgets import *


app = QApplication(sys.argv)
mainDialog = QDialog()
fname = QFileDialog.getOpenFileName(mainDialog, 'Open file', 
   'c:\\',"input files (*.pdf *.gif)")
print(fname)
app.exec_()

