"""

made by amedix and twitmix

"""
import os
import socket
import sys
from pathlib import Path
from threading import Thread
import keyboard
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGraphicsDropShadowEffect, QMainWindow, QLabel, \
    QFileDialog, QMessageBox, QScrollBar, QVBoxLayout, QScrollArea, QLineEdit, QTextEdit, QGridLayout

import config

exit_flag = True
opened_con = False

sock = socket.socket()


def keybd(s, selfobj):
    global exit_flag
    try:
        data = str(s.recv(8))[2:-1]
        print(data)
        try:
            keyboard.send(data)
        except Exception:
            print('unknown command')

    except Exception:
        exit_flag = False
        connection.set_room(selfobj, 'error')
        print('disconnected')


def send_file(sock, key):
    path = config.app_settings.path
    print('path:', path)
    if path != '':
        try:
            file_data = open(path, "r").read()
            i = 4096
            while True:
                text = file_data[i - 4096:i]
                if text:
                    sock.send(bytes(text, 'utf-8'))
                else:
                    sock.send(bytes(key, 'utf-8'))
                    break
                i += 4096
        except Exception:
            sock.send(bytes(key, 'utf-8'))
    else:
        sock.send(bytes(key, 'utf-8'))


def conn_to_serv(selfobj):
    global exit_flag, sock
    sock = socket.socket()
    try:
        print(config.app_settings.ip_serv)
        sock.connect((config.app_settings.ip_serv, 11111))
        key = str(sock.recv(16))[2:-1]
        connection.set_room(selfobj, 'load')
        send_file(sock, key)
        room_id = str(sock.recv(4))[2:-1]
        print(room_id)
        connection.set_room(selfobj, room_id)
        username = str(sock.recv(1024))[2:-1]
        connection.set_username(selfobj, f'Подключенный пользователь\n{username}', False)
        exit_flag = True
        while exit_flag:
            if exit_flag:
                keybd(sock, selfobj)
            else:
                break
        sock.close()
    except Exception:
        connection.set_room(selfobj, 'error')
        connection.set_username(selfobj, 'Проверьте ваше\nинтернет соединение', True)


def GUI():
    app = QApplication(sys.argv)
    ex = main_window()
    ex.show()
    sys.exit(app.exec())


def redactor_launch():
    os.system('redactor.exe')


class main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.color_btn = config.colors.color_supp

        self.setGeometry(560, 240, 800, 600)
        self.setWindowTitle(config.app_settings.version)
        self.setStyleSheet(f'background-color: {config.colors.color_main}; border-radius: 15')

        self.btn_c = QPushButton('Подключить\nустройство', self)
        self.btn_c.setFont(QFont("Times", 65, QFont.Bold))
        self.btn_c.resize(760, 300)
        self.btn_c.move(20, 20)
        self.btn_c.setStyleSheet(f'background-color: {self.color_btn}; border-radius: 15')
        self.btn_c.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=3, xOffset=4, yOffset=4))

        self.btn_f = QPushButton('Выбрать файл', self)
        self.btn_f.setFont(QFont("Times", 23, QFont.Bold))
        self.btn_f.resize(370, 110)
        self.btn_f.move(20, 340)
        self.btn_f.setStyleSheet(f'background-color: {self.color_btn}; border-radius: 15')
        self.btn_f.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=3, xOffset=4, yOffset=4))

        self.btn_i = QPushButton('Инструкция', self)
        self.btn_i.setFont(QFont("Times", 23, QFont.Bold))
        self.btn_i.resize(370, 110)
        self.btn_i.move(410, 340)
        self.btn_i.setStyleSheet(f'background-color: {self.color_btn}; border-radius: 15')
        self.btn_i.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=3, xOffset=4, yOffset=4))

        self.btn_q = QPushButton('QR-код', self)
        self.btn_q.setFont(QFont("Times", 23, QFont.Bold))
        self.btn_q.resize(370, 110)
        self.btn_q.move(20, 470)
        self.btn_q.setStyleSheet(f'background-color: {self.color_btn}; border-radius: 15')
        self.btn_q.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=3, xOffset=4, yOffset=4))

        self.btn_set = QPushButton('Настройки', self)
        self.btn_set.setFont(QFont("Times", 23, QFont.Bold))
        self.btn_set.resize(370, 110)
        self.btn_set.move(410, 470)
        self.btn_set.setStyleSheet(f'background-color: {self.color_btn}; border-radius: 15')
        self.btn_set.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=3, xOffset=4, yOffset=4))

        self.btn_c.clicked.connect(self.con)
        self.btn_f.clicked.connect(self.file)
        self.btn_q.clicked.connect(self.qr)
        self.btn_set.clicked.connect(self.set)
        self.btn_i.clicked.connect(self.ins)

    def file(self):
        self.win_file = file(self)
        self.win_file.show()

    def guide(self):
        pass

    def con(self):
        global opened_con
        if not opened_con:
            opened_con = True
            self.connection = connection(self)
            self.connection.show()

    def qr(self):
        os.system('start qr-code.jpg')

    def set(self):
        self.settings = settings(self)
        self.settings.show()

    def ins(self):
        self.instruction = instruction(self)
        self.instruction.show()

    def closeEvent(self, event):
        global exit_flag
        try:
            print('dis')
            sock.send(b'dis')
            sock.close()
        except Exception:
            pass
        exit_flag = False
        sys.exit()


class file(QWidget):
    def __init__(self, *a):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(700, 350, 520, 380)
        self.setWindowTitle('Add file')
        self.setStyleSheet(f'background-color: {config.colors.super_light_grey};')

        self.btn_openRedactor = QPushButton('открыть редактор', self)
        self.btn_openRedactor.setFont(QFont("Times", 23, QFont.Bold))
        self.btn_openRedactor.resize(480, 100)
        self.btn_openRedactor.move(20, 20)
        self.btn_openRedactor.setStyleSheet(f'background-color: {config.colors.light_grey}; border-radius: 15')
        self.btn_openRedactor.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=3, xOffset=4, yOffset=4))

        self.btn_myProjects = QPushButton('мои проекты', self)
        self.btn_myProjects.setFont(QFont("Times", 23, QFont.Bold))
        self.btn_myProjects.resize(480, 100)
        self.btn_myProjects.move(20, 140)
        self.btn_myProjects.setStyleSheet(f'background-color: {config.colors.light_grey}; border-radius: 15')
        self.btn_myProjects.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=3, xOffset=4, yOffset=4))

        self.btn_uploadFile = QPushButton('загрузить свой файл', self)
        self.btn_uploadFile.setFont(QFont("Times", 23, QFont.Bold))
        self.btn_uploadFile.resize(480, 100)
        self.btn_uploadFile.move(20, 260)
        self.btn_uploadFile.setStyleSheet(f'background-color: {config.colors.light_grey}; border-radius: 15')
        self.btn_uploadFile.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=3, xOffset=4, yOffset=4))

        self.btn_uploadFile.clicked.connect(self.other_docs)
        self.btn_myProjects.clicked.connect(self.my_docs)
        self.btn_openRedactor.clicked.connect(self.redactor)

    def redactor(self):
        self.close()
        th_redactor = Thread(target=redactor_launch, daemon=True)
        th_redactor.start()

    def open_file(self, dir):
        self.path = QFileDialog.getOpenFileName(directory=dir, filter='*.txt, *.sli')[0]
        print(self.path)
        if self.path != '':
            if len(open(self.path, 'r').read()) > 102400:
                self.path = ''
                print('long')
                QMessageBox.critical(self, 'too large file', 'Ваш файл превышает размер 100кб')
            else:
                config.app_settings.set_path(self.path)
                print(config.app_settings.name)
                self.close()

    def my_docs(self):
        self.open_file('my_docs')

    def other_docs(self):
        self.open_file(f'{Path.home()}\Desktop')


class connection(QWidget):
    def __init__(self, *a):
        super().__init__()
        self.initUI()

    def initUI(self):
        global exit_flag

        exit_flag = True

        self.setGeometry(560, 240, 800, 600)
        self.setWindowTitle('Connection')
        self.setStyleSheet(f'background-color: {config.colors.light_grey};')

        self.rl = QLabel(self)
        self.rl.setFont(QFont("Times", 70, QFont.Bold))
        self.rl.setText('connecting...')
        self.rl.resize(800, 300)
        self.rl.move(0, 20)
        self.rl.setAlignment(Qt.AlignCenter)

        self.us = QLabel(self)
        self.us.setFont(QFont("Times", 33, QFont.Bold))
        self.us.setText(f'Пользователь не подключен')
        self.us.resize(800, 100)
        self.us.move(0, 300)
        self.us.setAlignment(Qt.AlignCenter)

        self.ab = QLabel(self)
        self.ab.setFont(QFont("Times", 15, QFont.Cursive))
        self.ab.setText(
            'Отсканируйсте QR-код с помощью камеры на вашем смартфоне\n или самостоятельно найдите @remoteamedixbot в '
            'Telegram.\n\nДалее, отправте боту код, который вы видите на экране.')
        self.ab.resize(800, 200)
        self.ab.move(0, 400)
        self.ab.setAlignment(Qt.AlignCenter)
        try:
            conn_thread = Thread(target=conn_to_serv, args=(self,), daemon=True)
            conn_thread.start()
        except Exception:
            pass

    def set_username(self, usn, er_flag):
        self.us.setText(f'{usn}')
        self.ab.setText(' ')
        if not er_flag:
            self.ab.setText('Теперь вы можете свернуть приложение и открыть PowerPoint\n'
                            'Для остановки сессии закройте это окно\n\nПриятного использования!')

    def set_room(self, room):
        self.rl.setText(f'{room}')
        font_size = 170 - room.count('W') * 7
        self.rl.setFont(QFont("Times", font_size, QFont.Bold))

    def closeEvent(self, event):
        global exit_flag, opened_con
        opened_con = False
        self.us.setText(f'Пользователь не подключен')
        exit_flag = False
        try:
            print('dis')
            sock.send(b'dis')
            sock.close()
        except Exception:
            pass


class settings(QWidget):
    def __init__(self, *a):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(700, 350, 520, 380)
        self.setWindowTitle('Feedback')
        self.setStyleSheet(f'background-color: {config.colors.super_light_grey};')

        self.us = QLabel(self)
        self.us.setFont(QFont("Times", 27, QFont.Bold))
        self.us.setText(f'Обратная связь:\namedix2@gmail.com\nt.me/amedix2\nvk.com/amedix')
        self.us.resize(520, 200)
        self.us.move(0, 130)
        self.us.setAlignment(Qt.AlignCenter)

        self.ip = QLineEdit(self)
        self.ip.move(20, 30)
        self.ip.resize(260, 50)
        self.ip.setStyleSheet(f'background-color: {config.colors.light_grey}; border-radius: 15')
        self.ip.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=3, xOffset=4, yOffset=4))
        self.ip.setPlaceholderText("Введите ip")
        self.ip.setText(config.app_settings.ip_serv)
        self.ip.setFont(QFont("Times", 20, QFont.Bold))
        self.ip.setAlignment(Qt.AlignCenter)

        self.saveIp = QPushButton('Сохранить', self)
        self.saveIp.setFont(QFont("Times", 23, QFont.Bold))
        self.saveIp.resize(200, 50)
        self.saveIp.move(300, 30)
        self.saveIp.setStyleSheet(f'background-color: {config.colors.light_grey}; border-radius: 15')
        self.saveIp.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=3, xOffset=4, yOffset=4))

        self.saveIp.clicked.connect(self.save_ip)

    def save_ip(self):
        config.app_settings.set_ip(self.ip.text())
        QMessageBox.about(self, 'settings applied', 'Настройки были успешно сохранены')
        print(config.app_settings.ip_serv)

'''
        self.switchColor = QPushButton("Тёмная тема", self)
        self.switchColor.setFont(QFont("Times", 21, QFont.Bold))
        self.switchColor.resize(200, 50)
        self.switchColor.move(40, 110)
        self.switchColor.setCheckable(True)
        self.switchColor.setStyleSheet(f'background-color: {config.colors.light_grey}; border-radius: 15')
        self.switchColor.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=3, xOffset=4, yOffset=4))
'''


'''
        self.saveIp.clicked.connect(self.SaveIp)
        self.switchColor.clicked.connect(self.switchTheme)

    def switchTheme(self):
        if self.switchColor.isChecked():
            config.colors.set_theme(self, 'dark')
            self.switchColor.setText("Светлая тема")
        else:
            config.colors.set_theme(self, 'light')
            self.switchColor.setText("Тёмная тема")
'''


class instruction(QWidget):
    def __init__(self, *a):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(1380, 240, 520, 600)
        self.setWindowTitle('Instruction')
        self.setStyleSheet(f'background-color: {config.colors.super_light_grey};')

        self.insText = QLabel(self)
        self.insText.setFont(QFont("Times", 13))
        self.insText.setText(f'Для того чтобы управлять презентацией с вашего мобильного\nустройства вам нужно:\n1)Зайти в нашего Telegram-бота, которого вы можете найти\nпо адресу @remoteamedixbotили нажав на кнопку "QR-код",\nотсканировать появившийся QR-код.\n2)Нажать на кнопку подключить устройство\n и отправить полученный код боту.\nПосле этого вы можете управлять презентацией.'
                             f'\n\nЗачем нужна кнопка "Выбрать файл"?\nЭта кнопка нужна для добавления текста\nк определённому слайду. Нажав на неё, откроется окно,\nв котором вы можете открыть редактор\nили выбрать уже существующий файл.'
                             f'\n\nКак пользовать редактором?\nВ редакторе вы можете создать новый файл\nили редактировать старый.\nЕсли вы создаете новый:\n1)Вы должны написать название файла.\n2)вы пишите текст к слайдам.\n3)Вам нужно сохранить файл,\nнажав на кнопку "Сохранить файл"\nЕсли вы хотите редактировать файл\nвы должны сначала открыть файл,\nдалее работать также как и с новым файлом.')
        self.insText.resize(520, 600)
        self.insText.move(0, 0)


if __name__ == '__main__':
    gui_thread = Thread(target=GUI)
    gui_thread.start()