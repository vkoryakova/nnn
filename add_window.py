from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from custom import Custom
from database import QwrSql
from add import Ui_MainWindow

class AddWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.load_types()
        self.ui.pushButton_back.clicked.connect(self.back)
        self.ui.pushButton_save.clicked.connect(self.save_add)

    def back(self):
        from main import MainWindow
        self.m = MainWindow()
        self.m.show()
        self.close()

    def save_add(self):
        type_p = self.ui.comboBox_type.currentData()
        name = self.ui.lineEdit_name.text()
        director = self.ui.lineEdit_director.text()
        inn = self.ui.lineEdit_inn.text()
        rating = self.ui.lineEdit_rating.text()
        discount = self.ui.lineEdit_discount.text()

        try:
            with QwrSql() as db:
                db.add_partner(type_p, name, director, inn, rating, discount)
                QMessageBox.information(self, "Успех", "Партнер успешно добавлен")
                from main import MainWindow
                self.m = MainWindow()
                self.m.show()
                self.close()
        except ValueError as e:
            QMessageBox.warning(self, "Предупреждение", f"Неверный тип данных: {e}")
        except Exception as e:  # Assuming DatabaseError is defined
            QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось обновить данные: {e}")



    def load_types(self):
        with QwrSql() as db:
            types = db.load_types()
            for id, name in types:
                self.ui.comboBox_type.addItem(name, id)
