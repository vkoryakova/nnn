from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from custom import Custom
from database import QwrSql
from edit import Ui_MainWindow

class EditWindow(QMainWindow):
    def __init__(self, partner_id):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.partner_id = partner_id
        self.load_types()
        self.load_partner()
        self.ui.pushButton_back.clicked.connect(self.back)
        self.ui.pushButton_save.clicked.connect(self.save_edit)

    def back(self):
        from main import MainWindow
        self.m = MainWindow()
        self.m.show()
        self.close()

    def save_edit(self):
        type_p = self.ui.comboBox_type.currentData()
        name = self.ui.lineEdit_name.text()
        director = self.ui.lineEdit_director.text()
        inn = self.ui.lineEdit_inn.text()
        rating = self.ui.lineEdit_rating.text()
        discount = self.ui.lineEdit_discount.text()

        try:
            with QwrSql() as db:
                db.update_partner(self.partner_id, type_p, name, director, inn, rating, discount)
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
        pass

    def load_partner(self):
        try:
            with QwrSql() as db:
                partner = db.load_partner(self.partner_id)

                for i in partner:
                    self.ui.lineEdit_name.setText(i[0])
                    self.ui.lineEdit_director.setText(i[1])
                    self.ui.lineEdit_inn.setText(str(i[2]))
                    self.ui.lineEdit_rating.setText(str(i[3]))
                    self.ui.lineEdit_discount.setText(str(i[4]))
                    self.ui.comboBox_type.setCurrentText(i[5])
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"{e}")