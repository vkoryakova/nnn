from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from custom import Custom
from database import QwrSql
from calc import Ui_MainWindow

class OrdersWindow(QMainWindow):
    def __init__(self, partner_id):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.partner_id = partner_id
        self.ui.pushButton_back.clicked.connect(self.back)
        self.ui.pushButton_calcukate.clicked.connect(self.calc)

        self.load_orders()
    def calc(self):
        current_item = self.ui.listWidget.currentItem()
        order_id = current_item.data(Qt.ItemDataRole.UserRole)

        with QwrSql() as db:
            index_material = db.load_percent_material(order_id)
            space = db.calc_space(order_id)
            space_float = float(space)
            amount = db.load_amount(order_id)
            adjusted_material_per_item = space_float * (1 + float(index_material) / 100)
            total_raw = adjusted_material_per_item * int(amount)
            print(int(total_raw))

    def back(self):
        from main import MainWindow
        self.m = MainWindow()
        self.m.show()
        self.close()

    def load_orders(self):
        with QwrSql() as db:
            partners = db.load_orders(self.partner_id)
            self.ui.listWidget.clear()
            for i in partners:
                info = (f"{i[1]} - {i[2]}\n"
                        f"{i[3]}")
                id_order = i[0]

                custom = Custom(info)
                list_item = QListWidgetItem(self.ui.listWidget)
                list_item.setSizeHint(custom.sizeHint())
                list_item.setData(Qt.ItemDataRole.UserRole, id_order)
                self.ui.listWidget.addItem(list_item)
                self.ui.listWidget.setItemWidget(list_item, custom)
