import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic

main_form = uic.loadUiType("./ui/main_view.ui")[0]

class UiTest(QMainWindow, main_form):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)

        self.sub_view = None

        self.test_data = "UiTest data"

        self.button1.clicked.connect(self.button1Clicked)
        self.pushButton_2.clicked.connect(self.button2Clicked)


    def button1Clicked(self):
        print("========== call button1Clicked")

    def button2Clicked(self):
        print("========== call button2Clicked")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    view = UiTest()
    view.show()

    sys.exit(app.exec_())