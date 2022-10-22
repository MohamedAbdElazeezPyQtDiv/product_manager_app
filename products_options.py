import sys
from win32api import GetSystemMetrics
from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt, QSize


class ProductsOptions(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Options')
        self.setGeometry(.25 * GetSystemMetrics(0), 150, 480, 480)
        self.show()

    def set_label(self, text):
        self.productLabel.setText(text)


def main():
    application = QApplication(sys.argv)
    app = ProductsOptions()
    app.show()
    sys.exit(application.exec())


if __name__ == '__main__':
    main()
