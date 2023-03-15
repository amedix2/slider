"""

made by amedix and twitmix

"""
import config
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,\
    QGraphicsDropShadowEffect, QMainWindow, QLabel, QFileDialog


class redactor_start(QWidget):
    def __init__(self, *a):
        super().__init__()
        self.initUI()

    def initUI(self):
        pass


class redactor_main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.color_btn = config.colors.light_grey

        self.setGeometry(560, 200, 800, 600)
        self.setWindowTitle('reda')
        self.setStyleSheet(f'background-color: #ffffff; border-radius: 15')
