from datetime import datetime

import telebot
import time

import request_parser
from reminder_DB import SQL_requests

from Telegramm import config, Authorization

TelegramBot = telebot.TeleBot(config.TOKEN)
# текст для кнопок
text_butt_check_ru = "РУС"
text_butt_check_eng = "ENG"

# кнопки для панели
button_check_ru = telebot.types.KeyboardButton(text=text_butt_check_ru)
button_check_eng = telebot.types.KeyboardButton(text=text_butt_check_eng)

# панель (Выбор языка)
keyboard_check_lang = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)

keyboard_check_lang.add(button_check_ru, button_check_eng)


@TelegramBot.message_handler(regexp="(РУС|ENG)")
def handle_message(message):
    user = Authorization.check_user(message.chat.id)
    print(user)
    if user is None:
        TelegramBot.send_message(message.chat.id, "Добро пожаловать")
        SQL_requests.add_user(message.chat.id, message.text)
    else:
        TelegramBot.send_message(message.chat.id, "Добро пожаловать. На каком языке будем общаться? \nWelcome. What "
                                                  "language do you know?",
                                 reply_markup=keyboard_check_lang)


@TelegramBot.message_handler(commands=['Напомнить'])
def command_remind(message):
    user = Authorization.check_user(message.chat.id)
    if user is not None:
        print(message)
        print(str(user) + " Решил создать напоминалку")
        TelegramBot.send_message(message.chat.id, "Ваше напоминане: " + message.text)
        request = str(message.text)
        request_data = request_parser.setRequest(request)
        print(request_data["Text"] + " - " + str(request_data["Date"]))
        add_timer(request_data["Text"], request_data["Date"], message)
    else:
        TelegramBot.send_message(message.chat.id, "Добро пожаловать. На каком языке будем общаться? \nWelcome. What "
                                                  "language do you know?",
                                 reply_markup=keyboard_check_lang)


# Если пользователь запрашивает /start ДОДЕЛАТЬ
@TelegramBot.message_handler(commands=['start'])
def command_start(message):
    user = Authorization.check_user(message.chat.id)
    if user is not None:
        print("Вы у нас уже есть))")
        TelegramBot.send_message(message.chat.id, "Привет, " + message.chat.first_name,)
    else:
        TelegramBot.send_message(message.chat.id, "Добро пожаловать. На каком языке будем общаться? \nWelcome. What "
                                                  "language do you know?",
                                 reply_markup=keyboard_check_lang)


# Обработчик всех текстовых сообщений от пользователя
@TelegramBot.message_handler(func=lambda message: True, content_types=["text"])
def text_definition(message):
    print(message)


def add_timer(remind_text, date, message):
    now = time_now()
    date = datetime.time(date)
    while date > now:
        now = time_now()
        print("Timer инициализирован")
        TelegramBot.send_message(message.chat.id, text=remind_text + " в " + str(date))
        time.sleep(15)


def time_now():
    now = datetime.now()
    now = now.strftime("%H:%M")
    now = datetime.strptime(now, "%H:%M")
    now = datetime.time(now)
    return now


if __name__ == '__main__':
    TelegramBot.polling(none_stop=True)
