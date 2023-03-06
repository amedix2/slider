"""

made by amedix

"""
import socket
import random
import time

import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from threading import Thread

sock = socket.socket()

sock.bind((socket.gethostname(), 11111))
sock.listen(1000)

print('server is running')

TOKEN = '5937626790:AAGLqO3_UbPa9I144s7sBp28Ddi7ymcG4NI'

bot = Bot(token='5937626790:AAGLqO3_UbPa9I144s7sBp28Ddi7ymcG4NI')
dp = Dispatcher(bot)

BASE_SESSIONS = []
BASE_LISTEN = []
BASE_REG = {}


class session:
    def __init__(self, room, conn, addr, user_id):
        self.connection = conn
        self.address = addr
        self.uid = int(user_id)
        self.room_id = room

    def get_room_id(self):
        return self.room_id

    def get_connection(self):
        return self.connection

    def get_address(self):
        return self.address

    def get_uid(self):
        return int(self.uid)

    def set_uid(self, us):
        self.uid = int(us)


def room_id():
    return f'{chr(random.randint(65, 90))}{chr(random.randint(65, 90))}' \
           f'{chr(random.randint(65, 90))}{chr(random.randint(65, 90))}'


def conns(sock):
    global BASE_SESSIONS

    while True:
        conn, addr = sock.accept()
        print(f'connected {addr}')
        time.sleep(0.1)
        r = room_id()
        conn.send(bytes(r, 'utf-8'))
        print(f'room_id sent to {addr}')
        BASE_SESSIONS.append(session(r, conn, addr, 0))
        BASE_LISTEN.append(Thread(target=disconns, args=(conn, addr), daemon=True))
        BASE_LISTEN[-1].start()


def disconns(conn, addr):
    data = b''
    try:
        data = conn.recv(1024)
    except Exception:
        pass
    print(data, addr)
    idx = -1
    for i in range(len(BASE_SESSIONS)):
        if addr == BASE_SESSIONS[i].get_address():
            idx = i
            break
    if idx != -1:
        params = {
            'chat_id': BASE_SESSIONS[idx].get_uid(),
            'text': 'Удаленный компьютер прервал соединение. Введи новый код для подключения:'
        }

        response = requests.get('https://api.telegram.org/bot'+TOKEN+'/sendMessage', params=params)
        print(response)
        if BASE_SESSIONS[idx].get_uid() != 0:
            BASE_REG[BASE_SESSIONS[idx].get_uid()] = True
        BASE_SESSIONS.pop(idx)
        BASE_LISTEN.pop(idx)


def main_bot(dp):
    @dp.message_handler(commands=['start'])
    async def process_start_command(message: types.Message):
        await bot.send_message(message.from_user.id,
                               "Привет!\nЭтот бот управляет презентацией\n\nВведи код с экрана для "
                               "того, чтобы подключится и использовать приложение Slider:")
        BASE_REG[message.from_user.id] = True

    @dp.message_handler(commands=['reg'])
    async def process_start_command(message: types.Message):
        await bot.send_message(message.from_user.id,
                               "Введи код с экрана для "
                               "того, чтобы подключится и использовать приложение Slider:")
        BASE_REG[message.from_user.id] = True

    @dp.message_handler(content_types=['text'])
    async def main(message: types.Message):
        btn_l = KeyboardButton('<<<')
        btn_r = KeyboardButton('>>>')

        keybd = ReplyKeyboardMarkup()
        keybd.add(btn_l, btn_r)

        if message.from_user.id not in BASE_REG.keys():
            await bot.send_message(message.from_user.id, 'Вы не прошли регистрацию!\nИспользуйте команду /start или '
                                                         '/reg')
        else:
            if BASE_REG[message.from_user.id]:
                idx = -1
                for i in range(len(BASE_SESSIONS)):
                    if message.text.upper() == BASE_SESSIONS[i].get_room_id():
                        idx = i
                        break
                if idx != -1:
                    if BASE_SESSIONS[idx].get_uid() != 0:
                        await bot.send_message(message.from_user.id, f'Сессия {BASE_SESSIONS[idx].get_room_id()} уже '
                                                                     f'занята другим пользователем. ')
                    else:
                        BASE_SESSIONS[idx].set_uid(message.from_user.id)
                        BASE_REG[message.from_user.id] = False
                        try:
                            print(1)
                            BASE_SESSIONS[idx].get_connection().send(bytes(message.from_user.username, 'utf-8'))
                            await bot.send_message(message.from_user.id, "Авторизация прошла успешно!\n\n"
                                                                         "Нажмите >>> для того, чтобы переключится на "
                                                                         "следущий "
                                                                         "слайд.\n\n"
                                                                         "Нажмите <<< для того, чтобы переключится на "
                                                                         "предыдуший "
                                                                         "слайд.",
                                                   reply_markup=keybd)
                        except Exception:
                            await bot.send_message(message.from_user.id, 'Не удалось подключится к компьютеру, так как '
                                                                         'удаленный хост разорвал соединение. Попробуйте '
                                                                         'перезапустить приложение на вашем '
                                                                         'компьютере.\n\nВведите новый код:',
                                                   reply_markup=types.ReplyKeyboardRemove())
                            BASE_REG[message.from_user.id] = True
                            BASE_SESSIONS.pop(idx)
                            BASE_LISTEN.pop(idx)
                else:
                    await bot.send_message(message.from_user.id, "Ошибка авторизации: сессия не найден.\n"
                                                                 "Проверьте правильность введненного с экрана кода"
                                                                 " и повторите попытку.")
            else:
                idx = -1
                for i in range(len(BASE_SESSIONS)):
                    if message.from_user.id == BASE_SESSIONS[i].get_uid():
                        idx = i
                        break
                if idx != -1:
                    if message.text == '>>>':
                        try:
                            BASE_SESSIONS[idx].get_connection().send(bytes('right', 'utf-8'))
                            await bot.send_message(message.from_user.id, "Включаем следущий слайд...")
                        except Exception:
                            await bot.send_message(message.from_user.id, 'Не удалось подключится к компьютеру, так как '
                                                                         'удаленный хост разорвал соединение. Попробуйте '
                                                                         'перезапустить приложение на вашем '
                                                                         'компьютере.\n\nВведите новый код:',
                                                   reply_markup=types.ReplyKeyboardRemove())
                            BASE_REG[message.from_user.id] = True
                            BASE_SESSIONS.pop(idx)
                            BASE_LISTEN.pop(idx)
                    elif message.text == '<<<':
                        try:
                            BASE_SESSIONS[idx].get_connection().send(bytes('left', 'utf-8'))
                            await bot.send_message(message.from_user.id, "Включаем предыдущий слайд...")
                        except Exception:
                            await bot.send_message(message.from_user.id, 'Не удалось подключится к компьютеру, так как '
                                                                         'удаленный хост разорвал соединение. Попробуйте '
                                                                         'перезапустить приложение на вашем '
                                                                         'компьютере.\n\nВведите новый код:',
                                                   reply_markup=types.ReplyKeyboardRemove())
                            BASE_REG[message.from_user.id] = True
                            BASE_SESSIONS.pop(idx)
                            BASE_LISTEN.pop(idx)
                    else:
                        await bot.send_message(message.from_user.id, "Такой команды нет.")
                else:
                    await bot.send_message(message.from_user.id,
                                           'Вы не прошли регистрацию!\nИспользуйте команду /start или /reg')

        print(BASE_SESSIONS)
        print(BASE_LISTEN)
        print(BASE_REG)


if __name__ == '__main__':
    conns_thread = Thread(target=conns, args=(sock,), daemon=True)
    bot_thread = Thread(target=main_bot, args=(dp,))
    conns_thread.start()
    bot_thread.start()

    executor.start_polling(dp, skip_updates=True)