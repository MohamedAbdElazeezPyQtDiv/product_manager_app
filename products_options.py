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

#         # main options layout
#         self.mainOptionsLayout = QVBoxLayout()
#         self.setLayout(self.mainOptionsLayout)

#         # label
#         self.productLabel = QLabel('Options')
#         self.mainOptionsLayout.addWidget(self.productLabel, 15, Qt.AlignHCenter)

#         # options layout
#         self.optionsLayout = QHBoxLayout()
#         self.optionsLayout.setSpacing(30)
#         self.mainOptionsLayout.addLayout(self.optionsLayout, 85)

#         # options
#         self.sellProduct = QToolButton()
#         self.sellProduct.setText('Sell')
#         self.sellProduct.setIcon(QIcon("icons/options/sell_product.png"))
#         self.sellProduct.setIconSize(QSize(48, 48))
#         self.sellProduct.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

#         self.addProduct = QToolButton()
#         self.addProduct.setText('Add')
#         self.addProduct.setIcon(QIcon("icons/options/add_product.png"))
#         self.addProduct.setIconSize(QSize(48, 48))
#         self.addProduct.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

#         self.editProduct = QToolButton()
#         self.editProduct.setText('Edit')
#         self.editProduct.setIcon(QIcon("icons/options/edit_product.png"))
#         self.editProduct.setIconSize(QSize(48, 48))
#         self.editProduct.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

#         self.removeProduct = QToolButton()
#         self.removeProduct.setText('Remove')
#         self.removeProduct.setIcon(QIcon("icons/options/remove_product.png"))
#         self.removeProduct.setIconSize(QSize(48, 48))
#         self.removeProduct.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

#         self.optionsLayout.addStretch()
#         self.optionsLayout.addWidget(self.addProduct)
#         self.optionsLayout.addWidget(self.sellProduct)
#         self.optionsLayout.addWidget(self.editProduct)
#         self.optionsLayout.addWidget(self.removeProduct)
#         self.optionsLayout.addStretch()

#     def set_label(self, text):
#         self.productLabel.setText(text)


def main():
    application = QApplication(sys.argv)
    app = ProductsOptions()
    app.show()
    sys.exit(application.exec())


if __name__ == '__main__':
    main()
