from PyQt6.QtWidgets import *

class Custom(QWidget):
    def __init__(self, text):
        super().__init__()
        layout = QVBoxLayout()
        label_text = QLabel(text)
        layout.addWidget(label_text)
        self.setLayout(layout)