"""

made by amedix and twitmix

"""
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, \
    QGraphicsDropShadowEffect, QMainWindow, QFileDialog, QMessageBox, QLineEdit, QPlainTextEdit

import config


class redactor_main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.slides_left = QLabel(self)
        self.slides_right = QLabel(self)
        self.prevSlide = QPushButton('Предыдущий слайд', self)
        self.btn_del = QPushButton('Удалить слайд', self)
        self.nextSlide = QPushButton('Следующий слайд', self)
        self.slideText = QPlainTextEdit(self)
        self.slideName = QLabel(self)
        self.fileName = QLineEdit(self)
        self.saveFile = QPushButton('Сохранить файл', self)
        self.btn_file_open = QPushButton('Открыть файл', self)
        self.color_btn = config.colors.light_grey
        self.data = ['']
        self.index = 0
        self.path = ''
        self.initUI()

    def initUI(self):

        self.setGeometry(560, 240, 800, 600)
        self.setWindowTitle('Slider Redactor')
        self.setStyleSheet(f'background-color: {config.colors.color_main}; border-radius: 15')

        self.btn_file_open.setFont(QFont("Times", 15, QFont.Bold))
        self.btn_file_open.resize(240, 50)
        self.btn_file_open.move(280, 20)
        self.btn_file_open.setStyleSheet(f'background-color: {config.colors.color_supp}; border-radius: 15')
        self.btn_file_open.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=3, xOffset=4, yOffset=4))

        self.saveFile.setFont(QFont("Times", 15, QFont.Bold))
        self.saveFile.resize(240, 50)
        self.saveFile.move(540, 20)
        self.saveFile.setStyleSheet(f'background-color: {config.colors.color_supp}; border-radius: 15')
        self.saveFile.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=3, xOffset=4, yOffset=4))

        self.fileName.move(20, 20)
        self.fileName.resize(240, 50)
        self.fileName.setStyleSheet(f'background-color: {config.colors.color_supp}; border-radius: 15')
        self.fileName.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=3, xOffset=4, yOffset=4))
        self.fileName.setPlaceholderText("Введите название файла")
        self.fileName.setFont(QFont("Times", 12, QFont.Bold))
        self.fileName.setAlignment(Qt.AlignCenter)

        self.slideName.move(280, 90)
        self.slideName.resize(240, 50)
        self.slideName.setStyleSheet(f'background-color: {config.colors.color_supp}; border-radius: 15')
        self.slideName.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=3, xOffset=4, yOffset=4))
        self.slideName.setText("Слайд 0")
        self.slideName.setFont(QFont("Times", 15, QFont.Bold))
        self.slideName.setAlignment(Qt.AlignCenter)

        self.slideText.move(20, 160)
        self.slideText.resize(760, 350)
        self.slideText.setStyleSheet(f'background-color: {config.colors.color_supp}; border-radius: 15')
        self.slideText.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=3, xOffset=4, yOffset=4))
        self.slideText.setPlaceholderText(" Введите текст слайда")
        self.slideText.setFont(QFont("Times", 15, QFont.Bold))

        self.nextSlide.setFont(QFont("Times", 15, QFont.Bold))
        self.nextSlide.resize(240, 50)
        self.nextSlide.move(540, 530)
        self.nextSlide.setStyleSheet(f'background-color: {config.colors.color_supp}; border-radius: 15')
        self.nextSlide.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=3, xOffset=4, yOffset=4))

        self.btn_del.setFont(QFont("Times", 15, QFont.Bold))
        self.btn_del.resize(240, 50)
        self.btn_del.move(280, 530)
        self.btn_del.setStyleSheet(f'background-color: {config.colors.color_supp}; border-radius: 15')
        self.btn_del.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=3, xOffset=4, yOffset=4))

        self.prevSlide.setFont(QFont("Times", 15, QFont.Bold))
        self.prevSlide.resize(240, 50)
        self.prevSlide.move(20, 530)
        self.prevSlide.setStyleSheet(f'background-color: {config.colors.color_supp}; border-radius: 15')
        self.prevSlide.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=3, xOffset=4, yOffset=4))

        self.slides_right.move(530, 80)
        self.slides_right.resize(10000, 50)
        self.slides_right.setFont(QFont("Times", 30, QFont.Bold))

        self.slides_left.move(-10000, 80)
        self.slides_left.resize(10270, 50)
        self.slides_left.setFont(QFont("Times", 30, QFont.Bold))
        self.slides_left.setAlignment(Qt.AlignRight)

        self.btn_file_open.clicked.connect(self.open_file)
        self.nextSlide.clicked.connect(self.next)
        self.prevSlide.clicked.connect(self.previous)
        self.btn_del.clicked.connect(self.delete)
        self.saveFile.clicked.connect(self.save_file)

    def open_file(self):
        self.path = QFileDialog.getOpenFileName(directory='my_docs', filter='*.sli')[0]
        if self.path != '':
            if len(open(self.path, 'r').read()) > 102400:
                self.path = ''
                print('long')
                QMessageBox.critical(self, 'too large file', 'Ваш файл превышает размер 100кб')
            else:
                print('file opening')
                self.data = open(self.path, 'r').read().split('###')
                print(self.data)
                self.index = 0
                self.slideName.setText(f'Слайд {self.index}')
                self.slideText.clear()
                self.slideText.appendPlainText(self.data[self.index])
                self.fileName.setText(self.path[self.path.rfind('/') + 1:self.path.rfind('.')])
                self.slides_count()

    def save_file(self):
        self.data[self.index] = self.slideText.toPlainText()
        if self.fileName.text() != '':
            with open(f"my_docs\{self.fileName.text()}.sli", 'w') as f:
                f.write('###'.join(self.data))
            QMessageBox.about(self, 'saving complete', 'Ваш файл был успешно сохранен')
        else:
            QMessageBox.critical(self, 'unnamed file', 'Укажите имя файла')

    def slides_count(self):
        self.slides_right.setText(". " * (len(self.data) - self.index - 1))
        self.slides_left.setText(" ." * self.index)

    def next(self):
        self.data[self.index] = self.slideText.toPlainText()
        self.index += 1
        self.slides_count()
        if self.index == len(self.data):
            self.data.append('')
        self.slideText.clear()
        self.slideName.setText(f'Слайд {self.index}')
        if self.data[self.index] != '':
            self.slideText.appendPlainText(self.data[self.index])

    def previous(self):
        self.data[self.index] = self.slideText.toPlainText()
        self.index -= 1
        if self.index == -1:
            self.index = 0
        self.slides_count()
        self.slideName.setText(f'Слайд {self.index}')
        self.slideText.clear()
        self.slideText.appendPlainText(self.data[self.index])

    def delete(self):
        if len(self.data) != 1:
            self.data.pop(self.index)
            if self.index != 0:
                if self.index == len(self.data):
                    self.index -= 1
                self.slides_count()
                self.slideName.setText(f'Слайд {self.index}')
            self.slideText.clear()
            self.slideText.appendPlainText(self.data[self.index])
        else:
            self.slideText.clear()
            self.data[0] = ''


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w1 = redactor_main()
    w1.show()
    sys.exit(app.exec())
