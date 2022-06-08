import sys
from PyQt5.QtWidgets import *

app = QApplication(sys.argv)
mainDialog = QFileDialog()
fname = mainDialog.getOpenFileName(mainDialog,'Open file',
                                   'c:\\',"document file files (*.pdf)")
print(fname[0])
# mainDialog.show ()
app.exec_()
