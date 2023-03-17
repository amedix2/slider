"""

made by amedix and twitmix

"""
import os
import socket
import sys
from pathlib import Path
from threading import Thread
import keyboard
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGraphicsDropShadowEffect, QMainWindow, QLabel, \
    QFileDialog, QMessageBox, QScrollBar

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
            file_data = open(path, "r", encoding='utf-8').read()
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
        sock.connect((config.app_settings.ip_serv, 11111))
        key = str(sock.recv(16))[2:-1]
        connection.set_room(selfobj, 'sending file...')
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
    os.system('redactor.py')


class main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.color_btn = config.colors.light_grey

        self.setGeometry(560, 240, 800, 600)
        self.setWindowTitle('Slider alfa ver 1.01')
        self.setStyleSheet(f'background-color: {config.colors.super_light_grey}; border-radius: 15')

        self.btn_c = QPushButton('Подключить\nустройство', self)
        self.btn_c.setFont(QFont("Times", 65, QFont.Bold))
        self.btn_c.resize(760, 300)
        self.btn_c.move(20, 20)
        self.btn_c.setStyleSheet(f'background-color: {self.color_btn}; border-radius: 15')
        self.btn_c.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=15, xOffset=7, yOffset=7))

        self.btn_f = QPushButton('Выбрать файл', self)
        self.btn_f.setFont(QFont("Times", 23, QFont.Bold))
        self.btn_f.resize(370, 110)
        self.btn_f.move(20, 340)
        self.btn_f.setStyleSheet(f'background-color: {self.color_btn}; border-radius: 15')
        self.btn_f.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=15, xOffset=7, yOffset=7))

        self.btn_i = QPushButton('Инструкция', self)
        self.btn_i.setFont(QFont("Times", 23, QFont.Bold))
        self.btn_i.resize(370, 110)
        self.btn_i.move(410, 340)
        self.btn_i.setStyleSheet(f'background-color: {self.color_btn}; border-radius: 15')
        self.btn_i.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=15, xOffset=7, yOffset=7))

        self.btn_q = QPushButton('QR-код', self)
        self.btn_q.setFont(QFont("Times", 23, QFont.Bold))
        self.btn_q.resize(370, 110)
        self.btn_q.move(20, 470)
        self.btn_q.setStyleSheet(f'background-color: {self.color_btn}; border-radius: 15')
        self.btn_q.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=15, xOffset=7, yOffset=7))

        self.btn_b = QPushButton('Обратная связь', self)
        self.btn_b.setFont(QFont("Times", 23, QFont.Bold))
        self.btn_b.resize(370, 110)
        self.btn_b.move(410, 470)
        self.btn_b.setStyleSheet(f'background-color: {self.color_btn}; border-radius: 15')
        self.btn_b.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=15, xOffset=7, yOffset=7))

        self.btn_c.clicked.connect(self.con)
        self.btn_f.clicked.connect(self.file)
        self.btn_q.clicked.connect(self.qr)
        self.btn_b.clicked.connect(self.fb)
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

    def fb(self):
        self.feedback = feedback(self)
        self.feedback.show()

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
        self.btn_openRedactor.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=15, xOffset=7, yOffset=7))

        self.btn_myProjects = QPushButton('мои проекты', self)
        self.btn_myProjects.setFont(QFont("Times", 23, QFont.Bold))
        self.btn_myProjects.resize(480, 100)
        self.btn_myProjects.move(20, 140)
        self.btn_myProjects.setStyleSheet(f'background-color: {config.colors.light_grey}; border-radius: 15')
        self.btn_myProjects.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=15, xOffset=7, yOffset=7))

        self.btn_uploadFile = QPushButton('загрузить свой файл', self)
        self.btn_uploadFile.setFont(QFont("Times", 23, QFont.Bold))
        self.btn_uploadFile.resize(480, 100)
        self.btn_uploadFile.move(20, 260)
        self.btn_uploadFile.setStyleSheet(f'background-color: {config.colors.light_grey}; border-radius: 15')
        self.btn_uploadFile.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=15, xOffset=7, yOffset=7))

        self.btn_uploadFile.clicked.connect(self.other_docs)
        self.btn_myProjects.clicked.connect(self.my_docs)
        self.btn_openRedactor.clicked.connect(self.redactor)

    def redactor(self):
        self.close()
        th_redactor = Thread(target=redactor_launch, daemon=True)
        th_redactor.start()

    def open_file(self, dir):
        self.path = QFileDialog.getOpenFileName(directory=dir, filter='*.txt')[0]
        print(self.path)
        if self.path != '':
            if len(open(self.path, 'r').read()) > 4194304:
                self.path = ''
                print('long')
                QMessageBox.critical(self, 'too large file', 'Ваш файл превышает размер 4мб ')
            else:
                config.app_settings.set_path(self, self.path)
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


class feedback(QWidget):
    def __init__(self, *a):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(1380, 670, 520, 170)
        self.setWindowTitle('Feedback')
        self.setStyleSheet(f'background-color: {config.colors.light_grey};')

        self.us = QLabel(self)
        self.us.setFont(QFont("Times", 30, QFont.Bold))
        self.us.setText(f'amedix2@gmail.com\nt.me/amedix2\nvk.com/amedix')
        self.us.resize(520, 170)
        self.us.move(0, 0)
        self.us.setAlignment(Qt.AlignCenter)


class instruction(QWidget):
    def __init__(self, *a):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(1380, 240, 520, 380)
        self.setWindowTitle('Instruction')
        self.setStyleSheet(f'background-color: #ffffff;')


if __name__ == '__main__':
    gui_thread = Thread(target=GUI)
    gui_thread.start()
