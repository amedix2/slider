"""

made by amedix and twitmix

"""
import sys
from pathlib import Path
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,\
    QGraphicsDropShadowEffect, QMainWindow, QLabel, QFileDialog, QMessageBox

import config


class redactor_start(QMainWindow):
    def __init__(self, *a):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.color_btn = config.colors.light_grey

        self.setGeometry(560, 240, 400, 300)
        self.setWindowTitle('choose')
        self.setStyleSheet(f'background-color: #ffffff; border-radius: 15')

    def open_file(self):
        pass


class redactor_main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.color_btn = config.colors.light_grey

        self.setGeometry(560, 240, 800, 600)
        self.setWindowTitle('Slider Redactor')
        self.setStyleSheet(f'background-color: #ffffff; border-radius: 15')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w1 = redactor_main()
    w1.show()
    w2 = redactor_start()
    w2.show()
    sys.exit(app.exec())