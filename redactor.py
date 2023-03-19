"""

made by amedix and twitmix

"""
import sys
from pathlib import Path
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, \
    QGraphicsDropShadowEffect, QMainWindow, QFileDialog, QMessageBox, QLineEdit, QTextEdit

import config


class redactor_main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.index = 0
        self.data = [['', '']]

        self.color_btn = config.colors.light_grey

        self.setGeometry(560, 240, 800, 600)
        self.setWindowTitle('Slider Redactor')
        self.setStyleSheet(f'background-color: {config.colors.super_light_grey}; border-radius: 15')

        self.btn_file_open = QPushButton('Открыть файл', self)
        self.btn_file_open.setFont(QFont("Times", 15, QFont.Bold))
        self.btn_file_open.resize(240, 50)
        self.btn_file_open.move(280, 20)
        self.btn_file_open.setStyleSheet(f'background-color: {config.colors.light_grey}; border-radius: 15')
        self.btn_file_open.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=15, xOffset=7, yOffset=7))

        self.saveFile = QPushButton('Сохранить файл', self)
        self.saveFile.setFont(QFont("Times", 15, QFont.Bold))
        self.saveFile.resize(240, 50)
        self.saveFile.move(540, 20)
        self.saveFile.setStyleSheet(f'background-color: {config.colors.light_grey}; border-radius: 15')
        self.saveFile.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=15, xOffset=7, yOffset=7))

        self.fileName = QLineEdit(self)
        self.fileName.move(20, 20)
        self.fileName.resize(240, 50)
        self.fileName.setStyleSheet(f'background-color: {config.colors.light_grey}; border-radius: 15')
        self.fileName.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=15, xOffset=7, yOffset=7))
        self.fileName.setPlaceholderText("Введите название файла")
        self.fileName.setFont(QFont("Times", 10, QFont.Bold))
        self.fileName.setAlignment(Qt.AlignCenter)

        self.slideName = QLineEdit(self)
        self.slideName.move(20, 90)
        self.slideName.resize(760, 50)
        self.slideName.setStyleSheet(f'background-color: {config.colors.light_grey}; border-radius: 15')
        self.slideName.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=15, xOffset=7, yOffset=7))
        self.slideName.setPlaceholderText("Введите название или номер слайда")
        self.slideName.setFont(QFont("Times", 15, QFont.Bold))
        self.slideName.setAlignment(Qt.AlignCenter)

        self.slideText = QTextEdit(self)
        self.slideText.move(20, 160)
        self.slideText.resize(760, 350)
        self.slideText.setStyleSheet(f'background-color: {config.colors.light_grey}; border-radius: 15')
        self.slideText.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=15, xOffset=7, yOffset=7))
        self.slideText.setPlaceholderText("Введите текст слайда")
        self.slideText.setFont(QFont("Times", 15, QFont.Bold))
        self.slideText.setAlignment(Qt.AlignTop)

        self.nextSlide = QPushButton('Следующий слайд', self)
        self.nextSlide.setFont(QFont("Times", 15, QFont.Bold))
        self.nextSlide.resize(240, 50)
        self.nextSlide.move(540, 530)
        self.nextSlide.setStyleSheet(f'background-color: {config.colors.light_grey}; border-radius: 15')
        self.nextSlide.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=15, xOffset=7, yOffset=7))

        self.prevSlide = QPushButton('Предыдущий слайд', self)
        self.prevSlide.setFont(QFont("Times", 15, QFont.Bold))
        self.prevSlide.resize(270, 50)
        self.prevSlide.move(20, 530)
        self.prevSlide.setStyleSheet(f'background-color: {config.colors.light_grey}; border-radius: 15')
        self.prevSlide.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=15, xOffset=7, yOffset=7))

        self.btn_file_open.clicked.connect(self.open_file)
        self.nextSlide.clicked.connect(self.next)

    def open_file(self):
        self.path = QFileDialog.getOpenFileName(directory='my_docs', filter='*.sli')[0]
        print(self.path)
        if self.path != '':
            if len(open(self.path, 'r').read()) > 102400:
                self.path = ''
                print('long')
                QMessageBox.critical(self, 'too large file', 'Ваш файл превышает размер 100кб')
            config.app_settings.set_path(self.path)
            print(config.app_settings.name)

    def next(self):
        print(1)
        print(self.slideName.text(), self.slideText.text())
        self.data[self.index][0], self.data[self.index][1] = self.slideName.text(), self.slideText.text()
        print(2)
        self.index += 1
        self.data.append(['', ''])
        self.slideName.setPlaceholderText("Введите название или номер слайда")
        self.slideText.setPlaceholderText("Введите текст слайда")
        print(self.data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w1 = redactor_main()
    w1.show()
    sys.exit(app.exec())
