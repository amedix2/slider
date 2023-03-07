"""

made by amedix

"""
import socket
import keyboard
import sys
import os
from threading import Thread
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QMainWindow, QLabel, QFileDialog

exit_flag = True
path = ''

sock = socket.socket()


def keybd(s, selfobj):
    global exit_flag
    try:
        data = s.recv(1024)
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


def conn_to_serv(selfobj):
    global exit_flag, sock
    sock = socket.socket()
    try:
        sock.connect(('91.146.59.187', 11111))
        room_id = str(sock.recv(1024))[2:-1]
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
        connection.set_username(selfobj, 'Проверьте ваше интернет соединение', True)


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

        self.btn_c = QPushButton('Подключить\nустройство', self)
        self.btn_c.setFont(QFont("Times", 60, QFont.Bold))
        self.btn_c.resize(600, 300)
        self.btn_c.move(100, 20)

        self.btn_f = QPushButton('Загрузить\nтекстовый файл', self)
        self.btn_f.setFont(QFont("Times", 18, QFont.Bold))
        self.btn_f.resize(290, 100)
        self.btn_f.move(100, 350)

        self.btn_i = QPushButton('Инструкция', self)
        self.btn_i.setFont(QFont("Times", 18, QFont.Bold))
        self.btn_i.resize(290, 100)
        self.btn_i.move(410, 350)

        self.btn_q = QPushButton('QR-код', self)
        self.btn_q.setFont(QFont("Times", 18, QFont.Bold))
        self.btn_q.resize(290, 100)
        self.btn_q.move(100, 480)

        self.btn_b = QPushButton('Обратная связь', self)
        self.btn_b.setFont(QFont("Times", 18, QFont.Bold))
        self.btn_b.resize(290, 100)
        self.btn_b.move(410, 480)


        self.btn_c.clicked.connect(self.con)
        self.btn_f.clicked.connect(self.file)
        self.btn_q.clicked.connect(self.qr)
        self.btn_b.clicked.connect(self.fb)

        self.file = ''

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
        os.system('start qr-code.png')

    def fb(self):
        self.win3 = feedback(self)
        self.win3.show()

    def closeEvent(self, event):
        global exit_flag
        try:
            sock.send(b'disconnect')
        except Exception:
            pass
        exit_flag = False
        sock.close()
        sys.exit()


class connection(QWidget):

    def __init__(self, *a):
        super().__init__()
        self.initUI()

    def initUI(self):
        global exit_flag

        exit_flag = True

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

    def closeEvent(self, event):
        global exit_flag
        self.us.setText(f'Пользователь не подключен')
        exit_flag = False
        try:
            sock.send(b'disconnect')
            sock.close()
        except Exception:
            pass



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
