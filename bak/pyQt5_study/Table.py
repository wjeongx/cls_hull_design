from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import random

class MyTable(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.table = QTableWidget(parent)
        self._mainwin = parent

        
        self.__make_layout()
        self.__make_table()

    def __make_table(self):
        # self.table.setSelectionBehavior(QTableView.SelectRows)  # multiple row 선택 가능
        # self.table.setSelectionMode(QAbstractItemView.SingleSelection)        

        # row, column 갯수 설정해야만 tablewidget 사용할수있다.
        self.table.setColumnCount(5)
        self.table.setRowCount(3)

        # column header 명 설정. 
        self.table.setHorizontalHeaderLabels(["코드", "종목명"]) 
        self.table.horizontalHeaderItem(0).setToolTip("코드...")          # header tooltip 
        self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignRight) # header 정렬 방식 
        header_item = QTableWidgetItem("추가") 
        header_item.setBackground(Qt.red) # 헤더 배경색 설정 --> app.setStyle() 설정해야만 작동한다. 
        self.table.setHorizontalHeaderItem(2, header_item) # cell 에 data 입력하기 
        self.table.setItem(0, 0, QTableWidgetItem("000020")) 
        self.table.setItem(0, 1, QTableWidgetItem("삼성전자")) 
        self.table.setItem(1, 0, QTableWidgetItem("000030")) 
        self.table.setItem(1, 1, QTableWidgetItem("현대차")) 
        self.table.setItem(2, 0, QTableWidgetItem("000080")) 
        item = QTableWidgetItem("기아차") 
        self.table.setItem(2, 1, item) 
        
        # self.table.resizeColumnsToContents() 
        # self.table.resizeRowsToContents() 
        
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers) # edit 금지 모드 
        
        # self.table.setCurrentCell(1, 1) # current cell 위치 지정하기 
        self.table.setColumnWidth(2, 50) 
        ckbox = QCheckBox() 
        self.table.setCellWidget(0, 2, ckbox) 
        ckbox2 = QCheckBox('me') 
        self.table.setCellWidget(1, 2, ckbox2) 
        mycom = QComboBox() 
        mycom.addItems(["aa", "dd", "kk"]) 
        mycom.addItem("cc") 
        mycom.addItem("bb") 
        self.table.setCellWidget(2, 2, mycom) 
        item_widget = QPushButton("test") 
        self.table.setCellWidget(1, 3, item_widget) 
        self.table.cellClicked.connect(self.__mycell_clicked) 
        mycom.currentTextChanged.connect(self.__mycom_text_changed)

    def __mycell_clicked(self, row, col):
        cell = self.table.item(row, col)
        print(cell)

        if cell is not None:
            txt = "clicked cell = ({0},{1}) ==>{2}<==".format(row, col, cell.text())
        else:
            txt = "clicked cell = ({0},{1}) ==>None type<==".format(row, col)

        msg = QMessageBox.information(self, 'clicked cell...', txt)
        print(txt)
        self._mainwin.statusbar.showMessage(txt)
        return

    def __mycom_text_changed(self, txt):
        msg = QMessageBox.information(self, 'combobox changed...', txt)
        return

    def __make_layout(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.table)

        grid = QGridLayout()
        vbox.addLayout(grid)
        # grid.setSpacing(20)

        btn1 = QPushButton("전체내용 삭제")
        grid.addWidget(btn1, 0, 0)
        btn2 = QPushButton("table삭제")
        grid.addWidget(btn2, 0, 1)
        btn3 = QPushButton("selection mode")
        grid.addWidget(btn3, 0, 2)
        btn4 = QPushButton("column 추가")
        grid.addWidget(btn4, 0, 3)

        btn5 = QPushButton("column 삽입")
        grid.addWidget(btn5, 1, 0)
        btn6 = QPushButton("column 삭제")
        grid.addWidget(btn6, 1, 1)
        btn7 = QPushButton("row 추가")
        grid.addWidget(btn7, 1, 2)
        btn8 = QPushButton("row 삽입")
        grid.addWidget(btn8, 1, 3)

        btn9 = QPushButton("row 삭제")
        grid.addWidget(btn9, 2, 0)
        btn10 = QPushButton("row 단위선택")
        grid.addWidget(btn10, 2, 1)
        btn11 = QPushButton("grid line 숨기기")
        grid.addWidget(btn11, 2, 2)
        btn12 = QPushButton("alternate color")
        grid.addWidget(btn12, 2, 3)

        btn13 = QPushButton("randorm row 선택")
        grid.addWidget(btn13, 3, 0)
        btn14 = QPushButton("edit")
        grid.addWidget(btn14, 3, 1)
        btn15 = QPushButton("hide row헤더")
        grid.addWidget(btn15, 3, 2)
        btn16 = QPushButton("hide column헤더")
        grid.addWidget(btn16, 3, 3)

        btn17 = QPushButton("selected cells")
        grid.addWidget(btn17, 4, 0)
        btn18 = QPushButton("selected ranges")
        grid.addWidget(btn18, 4, 1)
        btn19 = QPushButton("current cell 내용")
        grid.addWidget(btn19, 4, 2)
        btn20 = QPushButton("(0,0) cell 내용")
        grid.addWidget(btn20, 4, 3)

        btn21 = QPushButton("span")
        grid.addWidget(btn21, 5, 0)
        btn22 = QPushButton("바탕화면 바꾸기")
        grid.addWidget(btn22, 5, 1)
        btn23 = QPushButton("cell 배경 바꾸기")
        grid.addWidget(btn23, 5, 2)
        btn24 = QPushButton("선택시 색 변경 ")
        grid.addWidget(btn24, 5, 3)

        btn25 = QPushButton("헤더배경색 변경")
        grid.addWidget(btn25, 6, 0)
        btn26 = QPushButton("(1,2) checkbox 값")
        grid.addWidget(btn26, 6, 1)
        btn27 = QPushButton("정렬 설정하기")
        grid.addWidget(btn27, 6, 2)
        btn28 = QPushButton("column, row 숨기기")
        grid.addWidget(btn28, 6, 3)

        self.setLayout(vbox)

        self.setGeometry(200, 200, 400, 500)
        self.setWindowTitle("tablewidget example")
'''
        btn1.clicked.connect(self.__btn1_clicked)
        btn2.clicked.connect(self.__btn2_clicked)
        btn3.clicked.connect(self.__btn3_clicked)
        btn4.clicked.connect(self.__btn4_clicked)
        btn5.clicked.connect(self.__btn5_clicked)
        btn6.clicked.connect(self.__btn6_clicked)
        btn7.clicked.connect(self.__btn7_clicked)
        btn8.clicked.connect(self.__btn8_clicked)
        btn9.clicked.connect(self.__btn9_clicked)
        btn10.clicked.connect(self.__btn10_clicked)
        btn11.clicked.connect(self.__btn11_clicked)
        btn12.clicked.connect(self.__btn12_clicked)
        btn13.clicked.connect(self.__btn13_clicked)
        btn14.clicked.connect(self.__btn14_clicked)
        btn15.clicked.connect(self.__btn15_clicked)
        btn16.clicked.connect(self.__btn16_clicked)
        btn17.clicked.connect(self.__btn17_clicked)
        btn18.clicked.connect(self.__btn18_clicked)
        btn19.clicked.connect(self.__btn19_clicked)
        btn20.clicked.connect(self.__btn20_clicked)
        btn21.clicked.connect(self.__btn21_clicked)
        btn22.clicked.connect(self.__btn22_clicked)
        btn23.clicked.connect(self.__btn23_clicked)
        btn24.clicked.connect(self.__btn24_clicked)
        btn25.clicked.connect(self.__btn25_clicked)
        btn26.clicked.connect(self.__btn26_clicked)
        btn27.clicked.connect(self.__btn27_clicked)
        btn28.clicked.connect(self.__btn28_clicked)
'''

class MyMain(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        table = MyTable(self)
        # table.setStyle(QStyleFactory.create('Fusion'))
        self.setCentralWidget(table)

        self.statusbar = self.statusBar()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))  # --> 없으면, 헤더색 변경 안됨.

    # w = MyTable()
    w = MyMain()
    w.show()
    sys.exit(app.exec())
 
