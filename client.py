"""

made by amedix

"""
import socket
import keyboard
import sys
import os
from pathlib import Path
from threading import Thread
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QMainWindow, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap

exit_flag = True
path = ''

sock = socket.socket()


def keybd(s, selfobj):
    global exit_flag
    try:
        data = s.recv(8)
        print(data)
        if data == b'right':
            keyboard.send('right')
        elif data == b'left':
            keyboard.send('left')
        else:
            print('unknown command')
    except Exception:
        exit_flag = False
        connection.set_room(selfobj, 'error')
        print('disconnected')


def send_file(sock, key):
    global path
    print('path:', path)
    if path != '':
        try:
            file = open(path, "rb")
            while True:
                file_data = file.read(4096)
                if file_data:
                    print(file_data)
                    sock.send(file_data)
                else:
                    sock.send(bytes(key, 'utf-8'))
                    break
        except Exception:
            sock.send(bytes(key, 'utf-8'))
    else:
        sock.send(bytes(key, 'utf-8'))


def conn_to_serv(selfobj):
    global exit_flag, sock
    sock = socket.socket()
    try:
        sock.connect(('217.114.157.45', 11111))
        key = str(sock.recv(16))[2:-1]
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


class main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(560, 200, 800, 600)
        self.setWindowTitle('Slider')
        self.setStyleSheet('background-color:#999999; border-radius: 15')

        self.btn_c = QPushButton('Подключить\nустройство', self)
        self.btn_c.setFont(QFont("Times", 65, QFont.Bold))
        self.btn_c.resize(760, 300)
        self.btn_c.move(20, 20)
        self.btn_c.setStyleSheet('background-color:#cccccc; border-radius: 15')

        self.btn_f = QPushButton('Загрузить\nтекстовый файл', self)
        self.btn_f.setFont(QFont("Times", 23, QFont.Bold))
        self.btn_f.resize(370, 110)
        self.btn_f.move(20, 340)
        self.btn_f.setStyleSheet('background-color:#cccccc; border-radius: 15')

        self.btn_i = QPushButton('Инструкция', self)
        self.btn_i.setFont(QFont("Times", 23, QFont.Bold))
        self.btn_i.resize(370, 110)
        self.btn_i.move(410, 340)
        self.btn_i.setStyleSheet('background-color:#cccccc; border-radius: 15')

        self.btn_q = QPushButton('QR-код', self)
        self.btn_q.setFont(QFont("Times", 23, QFont.Bold))
        self.btn_q.resize(370, 110)
        self.btn_q.move(20, 470)
        self.btn_q.setStyleSheet('background-color:#cccccc; border-radius: 15')

        self.btn_b = QPushButton('Обратная связь', self)
        self.btn_b.setFont(QFont("Times", 23, QFont.Bold))
        self.btn_b.resize(370, 110)
        self.btn_b.move(410, 470)
        self.btn_b.setStyleSheet('background-color:#cccccc; border-radius: 15')

        self.btn_c.clicked.connect(self.con)
        self.btn_f.clicked.connect(self.file)
        self.btn_q.clicked.connect(self.qr)
        self.btn_b.clicked.connect(self.fb)
        self.btn_i.clicked.connect(self.ins)

    def file(self):
        global path
        path = QFileDialog.getOpenFileName(directory=f'{Path.home()}\Desktop', filter='*.txt')[0]
        print(path)
        if path != '':
            self.btn_f.setText(f'Загружен файл\n{path.split("/")[-1]}')
        else:
            self.btn_f.setText('Загрузить\nтекстовый файл')

    def guide(self):
        pass

    def con(self):
        self.win1 = connection(self)
        self.win1.show()

    def qr(self):
        try:
            self.win2 = QR(self)
            self.win2.show()
        except Exception:
            os.system('start qr-code.png')

    def fb(self):
        self.win3 = feedback(self)
        self.win3.show()

    def ins(self):
        self.win4 = instruction(self)
        self.win4.show()

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


class connection(QWidget):

    def __init__(self, *a):
        super().__init__()
        self.initUI()

    def initUI(self):
        global exit_flag

        exit_flag = True

        self.setGeometry(560, 200, 800, 600)
        self.setWindowTitle('Connection')
        self.setStyleSheet('background-color:#cccccc;')

        self.rl = QLabel(self)
        self.rl.setFont(QFont("Times", 70, QFont.Bold))
        self.rl.setText('connecting...')
        self.rl.resize(800, 200)
        self.rl.move(0, 50)
        self.rl.setAlignment(Qt.AlignCenter)

        self.us = QLabel(self)
        self.us.setFont(QFont("Times", 33, QFont.Bold))
        self.us.setText(f'Пользователь не подключен')
        self.us.resize(800, 600)
        self.us.move(0, 50)
        self.us.setAlignment(Qt.AlignCenter)

        self.ab = QLabel(self)
        self.ab.setFont(QFont("Times", 15, QFont.Cursive))
        self.ab.setText(
            'Отсканируйсте QR-код с помощью камеры на вашем смартфоне\n или самостоятельно найдите @remoteamedixbot в Telegram.\n\n'
            'Далее, отправте боту код, который вы видите на экране.')
        self.ab.resize(800, 600)
        self.ab.move(0, 190)
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
        global exit_flag
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
        self.setGeometry(1380, 625, 520, 175)
        self.setWindowTitle('Feedback')
        self.setStyleSheet('background-color:#cccccc;')

        self.us = QLabel(self)
        self.us.setFont(QFont("Times", 30, QFont.Bold))
        self.us.setText(f'amedix2@gmail.com\nt.me/amedix2\nvk.com/amedix')
        self.us.resize(520, 175)
        self.us.move(0, 0)
        self.us.setAlignment(Qt.AlignCenter)


class QR(QWidget):
    def __init__(self, *a):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(20, 200, 520, 600)
        self.setWindowTitle('QR-code')
        self.setStyleSheet('background-color:#cccccc;')
        self.pixmap = QPixmap('qr-code.png')
        self.image = QLabel(self)
        self.image.resize(520, 600)
        self.image.move(0, 0)
        self.image.setPixmap(self.pixmap)
        self.image.setAlignment(Qt.AlignCenter)


class instruction(QWidget):
    def __init__(self, *a):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(1380, 200, 520, 375)
        self.setWindowTitle('Instruction')
        self.setStyleSheet('background-color:#cccccc;')


if __name__ == '__main__':
    gui_thread = Thread(target=GUI)
    gui_thread.start()
