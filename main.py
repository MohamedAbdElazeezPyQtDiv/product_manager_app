import sys
from win32api import GetSystemMetrics
from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon, QAction, QFont
from PySide6.QtCore import Qt, QSize
import styleSheet
import db_manager


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Product Manager V 1.0')
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(.05 * GetSystemMetrics(0), 50, 1350, 750)
        self.setFixedSize(self.size())
        self.setStyleSheet(styleSheet.styles())
        self.appDatabase = db_manager.DbManager(database='database.sqlite3')

        # -- central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # -- layouts
        self.mainLayout = QHBoxLayout()
        self.central_widget.setLayout(self.mainLayout)

        # -- toolbar
        self.tb = QToolBar('tool bar')
        self.tb.setFixedHeight(50)
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addToolBar(self.tb)
        # toolbar actions
        self.addProduct = QAction(QIcon('icons/add.png'), 'Add product')
        self.addMember = QAction(QIcon('icons/add_member.png'), 'Add member')
        self.sellProduct = QAction(QIcon('icons/sell.png'), 'Sell product')
        self.tb.addActions([self.addProduct, self.addMember, self.sellProduct])
        self.tb.addSeparator()

        # -- tab widget
        self.tabWidget = QTabWidget()
        self.mainLayout.addWidget(self.tabWidget)
        # tab widget tabs
        self.productsTab, self.membersTab, self.statisticsTab = QWidget(), QWidget(), QWidget()
        self.tabWidget.addTab(self.productsTab, 'Products')
        self.tabWidget.addTab(self.membersTab, 'Customers')
        self.tabWidget.addTab(self.statisticsTab, 'Statistics')

        # ################### PRODUCTS ################# #

        # products tab layout
        self.productsLayout = QHBoxLayout()
        self.productsTab.setLayout(self.productsLayout)

        # Products table
        self.productsTable = QTableWidget()
        self.productsLayout.addWidget(self.productsTable, stretch=70)
        self.refresh_table(table_widget=self.productsTable, refresh_with='all data', database_table_name='Products')
        self.productsTable.setHorizontalHeaderLabels(self.appDatabase.columns_names('Products'))
        self.productsTable.setColumnWidth(1, 200)
        self.productsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.productsTable.setCurrentCell(0, 1)
        # products tab main right layout
        self.productsMainRightLayout = QGridLayout()
        self.productsLayout.addLayout(self.productsMainRightLayout, stretch=30)
        self.productsMainRightLayout.setRowStretch(0, 5)
        self.productsMainRightLayout.setRowStretch(1, 15)
        self.productsMainRightLayout.setRowStretch(2, 10)
        self.productsMainRightLayout.setRowStretch(3, 30)
        self.productsMainRightLayout.setRowStretch(4, 25)
        self.productsMainRightLayout.setRowStretch(5, 15)
        self.productsMainRightLayout.setAlignment(Qt.AlignTop)
        self.productsMainRightLayout.setVerticalSpacing(1)

        # products tab right layouts
        self.searchLineEdit = QLineEdit()
        self.searchLineEdit.setPlaceholderText('Enter product name to search')
        self.productsMainRightLayout.addWidget(self.searchLineEdit, 0, 0, Qt.AlignVCenter)

        self.searchButton = QPushButton('search')
        self.searchButton.clicked.connect(self.search_product)
        self.productsMainRightLayout.addWidget(self.searchButton, 0, 1, Qt.AlignVCenter)

        self.filterGroupBox = QGroupBox('Filter')
        self.productsMainRightLayout.addWidget(self.filterGroupBox, 1, 0, 1, 1, Qt.AlignVCenter)
        self.filterLayout = QVBoxLayout()
        self.filterGroupBox.setLayout(self.filterLayout)
        self.filter1 = QRadioButton('Available')
        self.filter2 = QRadioButton('Un Available')
        self.filter3 = QRadioButton('All')
        self.filterLayout.addWidget(self.filter1)
        self.filterLayout.addWidget(self.filter2)
        self.filterLayout.addWidget(self.filter3)
        self.filterButton = QPushButton('filter')
        self.filterButton.clicked.connect(self.filter)
        self.productsMainRightLayout.addWidget(self.filterButton, 1, 1, Qt.AlignVCenter)

        # options label
        self.productLabel = QLabel('Options')
        self.productsMainRightLayout.addWidget(self.productLabel, 2, 0, 1, 3, Qt.AlignHCenter)
        self.productsTable.currentCellChanged.connect(
                lambda: self.productLabel.setText(f"Product: {self.productsTable.currentItem().text()}")
                if self.productsTable.currentColumn() == 1 else self.productLabel.setText('options'))
        self.productLabel.setFont(QFont('times', 14, 5))

        # options layout
        self.optionsLayout = QHBoxLayout()
        self.optionsLayout.setSpacing(30)
        self.productsMainRightLayout.addLayout(self.optionsLayout, 3, 0, 1, 3)

        # options
        self.sellProduct = QToolButton()
        self.sellProduct.setText('Sell')
        self.sellProduct.setIcon(QIcon("icons/options/sell_product.png"))
        self.sellProduct.setIconSize(QSize(48, 48))
        self.sellProduct.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.sellProductGroupbox = QGroupBox('sell')
        # sell signal
        self.sellProduct.clicked.connect(lambda: self.product_option(option='sell'))

        self.addProduct = QToolButton()
        self.addProduct.setText('Add')
        self.addProduct.setIcon(QIcon("icons/options/add_product.png"))
        self.addProduct.setIconSize(QSize(48, 48))
        self.addProduct.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.editProduct = QToolButton()
        self.editProduct.setText('Edit')
        self.editProduct.setIcon(QIcon("icons/options/edit_product.png"))
        self.editProduct.setIconSize(QSize(48, 48))
        self.editProduct.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.editProductGroupbox = QGroupBox('Edit')
        # edit signal
        self.editProduct.clicked.connect(lambda: self.product_option(option='edit'))

        self.removeProduct = QToolButton()
        self.removeProduct.setText('Remove')
        self.removeProduct.setIcon(QIcon("icons/options/remove_product.png"))
        self.removeProduct.setIconSize(QSize(48, 48))
        self.removeProduct.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.removeProduct.clicked.connect(lambda: self.product_option('remove'))

        self.optionsLayout.addStretch()
        self.optionsLayout.addWidget(self.addProduct)
        self.optionsLayout.addWidget(self.sellProduct)
        self.optionsLayout.addWidget(self.editProduct)
        self.optionsLayout.addWidget(self.removeProduct)
        self.optionsLayout.addStretch()

        # - edit product group box
        # layout
        self.productsMainRightLayout.addWidget(self.editProductGroupbox, 4, 0, 1, 3)
        self.editProductGroupboxLayout = QFormLayout()
        self.editProductGroupbox.setLayout(self.editProductGroupboxLayout)
        self.editProductGroupbox.close()
        # widgets
        self.editProductName = QLineEdit()
        self.editProductGroupboxLayout.addRow('Product: ', self.editProductName)
        self.editProductName.setPlaceholderText('Product name')

        self.editProductStock = QLineEdit()
        self.editProductGroupboxLayout.addRow('In stock: ', self.editProductStock)
        self.editProductStock.setPlaceholderText('in stock')

        self.editProductPrice = QLineEdit()
        self.editProductGroupboxLayout.addRow('Price: ', self.editProductPrice)
        self.editProductPrice.setPlaceholderText('Product price')

        self.editProductAvailability = QComboBox()
        self.editProductGroupboxLayout.addRow('Availability: ', self.editProductAvailability)
        self.editProductAvailability.addItems(['Available', 'Un Available'])

        self.editProductSaveButton = QPushButton('Save')
        self.editProductGroupboxLayout.addWidget(self.editProductSaveButton)
        # signals
        self.editProductSaveButton.clicked.connect(lambda: self.product_option(option='save edit'))
        self.productsTable.currentCellChanged.connect(lambda: self.product_option(
                'edit') if self.editProductGroupbox.isVisible() else self.editProductGroupbox.close())

        # -sell product group box
        # layout
        self.productsMainRightLayout.addWidget(self.sellProductGroupbox, 4, 0, 1, 3)
        self.sellProductGroupboxLayout = QFormLayout()
        self.sellProductGroupbox.setLayout(self.sellProductGroupboxLayout)
        self.sellProductGroupbox.close()
        # widgets
        self.sellProductLineEdit = QLineEdit()
        self.sellProductGroupboxLayout.addRow('Quantity', self.sellProductLineEdit)
        self.sellProductLineEdit.setPlaceholderText('Product quantity')
        self.sellProductCheckBox = QCheckBox(self)
        self.sellProductGroupboxLayout.addWidget(self.sellProductCheckBox)
        self.sellProductCheckBox.setText('sell to saved member')
        self.sellProductCombBox = QComboBox(self)
        self.sellProductGroupboxLayout.addWidget(self.sellProductCombBox)
        self.sellProductCombBox.addItems([i[0] for i in self.appDatabase.get_member_details()])
        self.sellProductCombBox.setDisabled(True)
        self.sellProductButton = QPushButton('Sell')
        self.sellProductGroupboxLayout.addWidget(self.sellProductButton)
        # signals
        self.sellProductCheckBox.clicked.connect(lambda:
                                                 self.sellProductCombBox.setEnabled(True)
                                                 if self.sellProductCheckBox.isChecked()
                                                 else self.sellProductCombBox.setDisabled(True))
        self.sellProductButton.clicked.connect(lambda: self.product_option(option='submit sell'))
        self.sellProduct.clicked.connect(lambda: self.product_option('sell'))

        # ####################### Customers ##################### #

        # Customers tab layout
        self.membersLayout = QHBoxLayout()
        # Products tab table
        self.membersTab.setLayout(self.membersLayout)

        self.membersTable = QTableWidget()
        self.membersLayout.addWidget(self.membersTable, stretch=70)
        self.membersTable.setColumnWidth(1, 200)
        self.membersTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.refresh_table(table_widget=self.membersTable,
                           database_table_name='Customers',
                           refresh_with='all data')
        self.membersTable.setHorizontalHeaderLabels(self.appDatabase.columns_names('Customers'))
        self.membersTable.setCurrentCell(0, 1)

        # ####################### Statistics ##################### #
        self.statisticsTabLayout = QFormLayout()
        self.statisticsTab.setLayout(self.statisticsTabLayout)
        self.refresh_statistics()

    def refresh_table(self, table_widget: QTableWidget, database_table_name, refresh_with='all data'):
        table_widget.setColumnCount(self.appDatabase.count(database_table_name, count='columns'))
        table_widget.setRowCount(self.appDatabase.count(database_table_name, count='rows'))

        if refresh_with == 'all data':
            self.show_table_data(table_widget=table_widget, data=self.appDatabase.all_data(database_table_name),
                                 rows_num=self.appDatabase.count(database_table_name, count='rows'),
                                 columns_num=self.appDatabase.count(database_table_name, count='columns'))
        else:
            pass

    def show_table_data(self, table_widget: QTableWidget, data: list, rows_num: int, columns_num: int) -> None:
        table_widget.clearContents()
        for r in range(rows_num):
            for c in range(columns_num):
                table_widget.setItem(r, c, QTableWidgetItem(str(data[r][c])))

    def search_product(self):
        if self.searchLineEdit.text() != '':
            print(self.searchLineEdit.text())
            search_result = self.appDatabase.search(self.searchLineEdit.text())
            self.show_table_data(table_widget=self.productsTable,
                                 data=search_result,
                                 rows_num=len(search_result),
                                 columns_num=self.appDatabase.count('products', 'columns'))
        else:
            pass

    def filter(self):
        data_to_show = self.appDatabase.all_data('Products')
        if self.filter1.isChecked():
            data_to_show = self.appDatabase.filter('Products', filter='available')
        elif self.filter2.isChecked():
            data_to_show = self.appDatabase.filter('Products', filter='un available')
        elif self.filter3.isChecked():
            pass
        self.show_table_data(table_widget=self.productsTable,
                             data=data_to_show,
                             rows_num=len(data_to_show),
                             columns_num=self.appDatabase.count('products', 'columns'))

    def product_option(self, option='add'):
        if self.productsTable.currentColumn() == 1:
            self.productLabel.setText(self.productsTable.currentItem().text())
        current_product_id = self.productsTable.item(self.productsTable.currentRow(), 0).text()
        if option == 'add':
            pass
        elif option == 'sell':
            self.editProductGroupbox.close()
            self.sellProductGroupbox.show()
        elif option == 'submit sell':
            self.appDatabase.sell_product(current_product_id, int(self.sellProductLineEdit.text()))
            if self.sellProductCheckBox.isChecked():
                self.sellProductCombBox.setEnabled(True)
                self.appDatabase.add_product_to_member(member_id=self.appDatabase.get_member_details(data_type='id',
                                                                                                     member_name=self.sellProductCombBox.currentText()),
                                                       product_id=current_product_id,
                                                       quantity=int(self.sellProductLineEdit.text()))
            self.refresh_table(table_widget=self.productsTable, database_table_name='Products')
            self.refresh_table(table_widget=self.membersTable, database_table_name='Customers')

        elif option == 'edit':
            self.sellProductGroupbox.close()
            self.editProductGroupbox.show()
            self.editProductName.setText(self.appDatabase.product_details(current_product_id, 'name'))
            self.editProductStock.setText(str(self.appDatabase.product_details(current_product_id, 'stock')))
            self.editProductPrice.setText(str(self.appDatabase.product_details(current_product_id, 'price')))
            self.editProductAvailability.setCurrentText(
                    'Available' if self.appDatabase.product_is_available(current_product_id) else 'Un Available')
        elif option == 'save edit':
            msg = QMessageBox.warning(self, 'Save', "Are you sure to save?'",
                                      QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)
            if msg == QMessageBox.Yes:
                self.appDatabase.add_product(statue='edit',
                                             product_id=current_product_id,
                                             product_name=self.editProductName.text(),
                                             stock=int(self.editProductStock.text()),
                                             manufacture=self.appDatabase.product_details(current_product_id,
                                                                                          'manufacture'),
                                             price=int(self.editProductPrice.text()),
                                             availability=self.editProductAvailability.currentText())
            self.editProductGroupbox.close()
            self.refresh_table(table_widget=self.productsTable, database_table_name='Products')

        elif option == 'remove':
            self.sellProductGroupbox.close()
            self.editProductGroupbox.close()
            msg = QMessageBox.warning(self, 'Remove',
                                      f"Are you sure to remove '{self.productsTable.currentItem().text()} ?'",
                                      QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)
            current_row = self.productsTable.currentRow()
            current_column = self.productsTable.currentColumn()
            if msg == QMessageBox.Yes:
                self.appDatabase.remove_product(current_product_id)
                self.refresh_table(table_widget=self.productsTable, database_table_name='Products')
                self.productsTable.setCurrentCell(current_row, current_column)
        self.refresh_statistics()

    def refresh_statistics(self):
        for i in range(len(self.appDatabase.statistics().items())):
            self.statisticsTabLayout.removeRow(0)
        for key, value in self.appDatabase.statistics().items():
            self.statisticsTabLayout.addRow(key, QLabel(f'{value}'))

    def closeEvent(self, event) -> None:
        self.appDatabase.commit()
        self.appDatabase.close()
        print('database closed')


def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())
    print("hellow")
    


if __name__ == '__main__':
    main()
