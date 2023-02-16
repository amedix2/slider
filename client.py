"""

made by amedix

"""
import socket
import keyboard
import sys, os
from threading import Thread
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QMainWindow, QLabel

sock = socket.socket()


def conn_to_serv(selfobj):
    global sock
    sock = socket.socket()
    try:
        sock.connect(('92.241.226.146', 11111))
        room_id = str(sock.recv(1024))[2:-1]
        connection.set_room(selfobj, room_id)
        username = str(sock.recv(1024))[2:-1]
        connection.set_username(selfobj, username)
        try:
            while True:
                try:
                    data = sock.recv(1024)
                except Exception:
                    connection.set_room('Подключение к серверу...')
                print(data)
                if data == b'close room':
                    sock.close()
                    break
                elif data == b'right':
                    keyboard.send('right')
                elif data == b'left':
                    keyboard.send('left')

        except Exception:
            print('server disconnect')
    except Exception:
        connection.set_room(selfobj, 'error')


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
        self.setGeometry(150, 150, 300, 300)
        self.setWindowTitle('Slider')

        self.btn1 = QPushButton('Подключить\nустройство', self)
        self.btn1.setFont(QFont("Times", 20, QFont.Bold))
        self.btn1.resize(220, 100)
        self.btn1.move(40, 60)

        self.btn2 = QPushButton('QR-код', self)
        self.btn2.resize(100, 40)
        self.btn2.move(40, 180)

        self.btn3 = QPushButton('Обратная связь', self)
        self.btn3.resize(100, 40)
        self.btn3.move(160, 180)

        self.btn1.clicked.connect(self.con)
        self.btn2.clicked.connect(self.qr)
        self.btn3.clicked.connect(self.fb)

    def con(self):
        self.win1 = connection(self)
        self.win1.show()

    def qr(self):
        os.system('start qr-code.png')

    def fb(self):
        self.win3 = feedback(self)
        self.win3.show()

    def closeEvent(self, event):
        sock.send(b'disconnect')
        sock.close()
        sys.exit()


class connection(QWidget):

    def __init__(self, *a):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(470, 150, 600, 300)
        self.setWindowTitle('Connection')

        self.rl = QLabel(self)
        self.rl.setFont(QFont("Times", 60, QFont.Bold))
        self.rl.setText('connecting...')
        self.rl.resize(600, 100)
        self.rl.move(0, 30)
        self.rl.setAlignment(Qt.AlignCenter)

        self.us = QLabel(self)
        self.us.setFont(QFont("Times", 20, QFont.Bold))
        self.us.setText(f'Пользователь не подключен')
        self.us.resize(600, 100)
        self.us.move(0, 120)
        self.us.setAlignment(Qt.AlignCenter)

        self.ab = QLabel(self)
        self.ab.setFont(QFont("Times", 8, QFont.Cursive))
        self.ab.setText(
            'Отсканируйсте QR-код с помощью камеры на вашем смартфоне\n или самостоятельно найдите @remoteamedixbot в Telegram.\n\n'
            'Далее, отправте боту код, который вы видите на экране.')
        self.ab.resize(600, 100)
        self.ab.move(0, 190)
        self.ab.setAlignment(Qt.AlignCenter)

        conn_thread = Thread(target=conn_to_serv, args=(self, ), daemon=True)
        conn_thread.start()

    def set_username(self, usn):
        self.us.setText(f'Подключенный пользователь\n{usn}')
        self.ab.setText('Теперь вы можете свернуть приложение и открыть PowerPoint\n'
                        'Для остановки сессии закройте это окно\n\nПриятного использования!')

    def set_room(self, room):
        self.rl.setText(f'{room}')

    def closeEvent(self, event):
        self.us.setText(f'Пользователь не подключен')
        sock.send(b'disconnect')


class feedback(QWidget):
    def __init__(self, *a):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(1090, 150, 530, 300)
        self.setWindowTitle('Feedback')

        self.us = QLabel(self)
        self.us.setFont(QFont("Times", 30, QFont.Bold))
        self.us.setText(f'amedix2@gmail.com\nt.me/amedix2\nvk.com/amedix')
        self.us.resize(530, 300)
        self.us.move(0, 0)
        self.us.setAlignment(Qt.AlignCenter)


if __name__ == '__main__':
    gui_thread = Thread(target=GUI)
    gui_thread.start()