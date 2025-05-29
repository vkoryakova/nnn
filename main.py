from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from add_window import AddWindow
from custom import Custom
from database import QwrSql
from orders import OrdersWindow
from partners import Ui_MainWindow
import sys
from edit_window import EditWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.listWidget.doubleClicked.connect(self.edit)
        self.ui.pushButton_add.clicked.connect(self.add_partner)
        self.ui.pushButton_delete.clicked.connect(self.delete_partner)
        self.ui.pushButton_orders.clicked.connect(self.orders)

        self.load_partners()

    def orders(self):
        current_item = self.ui.listWidget.currentItem()
        partner_id = current_item.data(Qt.ItemDataRole.UserRole)
        self.orders_w = OrdersWindow(partner_id)
        self.orders_w.show()
        self.close()

    def delete_partner(self):
        try:
            current_item = self.ui.listWidget.currentItem()
            partner_id = current_item.data(Qt.ItemDataRole.UserRole)
            if not partner_id:
                QMessageBox.critical(self, "Ошибка", "Выберите кого хотите удалить")
            with QwrSql() as db:
                db.delete_partner(partner_id)
                QMessageBox.information(self, "Успех", "Партнер успешно удален")
                self.load_partners()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"{e}")


    def add_partner(self):

        self.add_w = AddWindow()
        self.add_w.show()
        self.close()

    def edit(self):
        current_item = self.ui.listWidget.currentItem()
        partner_id = current_item.data(Qt.ItemDataRole.UserRole)
        self.edit_w  =EditWindow(partner_id)
        self.edit_w.show()
        self.close()
    def load_partners(self):
        with QwrSql() as db:
            partners = db.load_partners()
            self.ui.listWidget.clear()
            for i in partners:
                info = (f"{i[2]} | {i[1]}               {i[6]}%\n"
                        f"{i[3]}\n"
                        f"inn: {i[4]}\n"
                        f"rating: {i[5]}\n")
                id_partner = i[0]

                custom = Custom(info)
                list_item = QListWidgetItem(self.ui.listWidget)
                list_item.setSizeHint(custom.sizeHint())
                list_item.setData(Qt.ItemDataRole.UserRole, id_partner)
                self.ui.listWidget.addItem(list_item)
                self.ui.listWidget.setItemWidget(list_item, custom)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


