
# -*- coding: utf-8 -*-
from cgitb import text
import telebot #импорт pyTelegramBotAPI 
from telebot import types #также достанем типы
import random #рандом обязательно
import os
import sys
import jellyfish
import Levenshtein
from fuzzywuzzy import fuzz
from datetime import date
from datetime import datetime
import datetime
import json

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

bot = telebot.TeleBot('5725077388:AAENT--CKUVwwRxLA6gDQB2yHG17lqZ14NU')

today1 = date.today()
tomorrow = today1 + datetime.timedelta(days=1)
sample_time = {today1}
sample_time2 = {tomorrow}
json_str = json.dumps(sample_time, default=str)
json_str2 = json.dumps(sample_time2, default=str)

mas = []
if os.path.exists('dic/schedule.txt'):
    f = open('dic/schedule.txt', 'r', encoding='UTF-8')
    for x in f:
        if (len(x.strip()) > 2):
            mas.append(x.strip().lower())
    f.close()

with open('dic/part.txt', 'r', encoding='UTF-8') as f: ## Открываем файл
    my_lines = list(f) ## Помещаем в список.
derek = my_lines[0]

f_read = open("dic/corect.txt", 'r', encoding='UTF-8')
last_line = f_read.readlines()[0]

def answer(text):
    try:
        text = text.lower().strip()
        if os.path.exists('dic/schedule.txt'):
            a = 0
            n = 0
            nn = 0
            for q in mas:
                if ('u: ' in q):
                    # С помощью fuzzywuzzy получаем, насколько похожи две строки
                    aa = (fuzz.token_sort_ratio(q.replace('u: ', ''), text))
                    if (aa > a and aa != a):
                        a = aa
                        nn = n
                n = n + 1
            s = mas[nn + 1]
            return s
        else:
            return 'Ошибка'
    except:
        return 'Ошибка'

answer2 = answer(json_str)
answer1 = answer(json_str2)



@bot.message_handler(commands=['start'])
def send_welcome(massage):
    stic = open('stic/welcome.tgs', 'rb')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("Расписание")
    but2 = types.KeyboardButton("Ближайшие События")
    but3 = types.KeyboardButton("Рассылка")
    markup.add(but1).add(but2).add(but3)
    
    bot.reply_to(massage, "Привет, {0.first_name}\nЧем могу помочь?".format(massage.from_user),parse_mode='html',reply_markup=markup)
    bot.send_sticker(massage.chat.id,stic)


@bot.message_handler(func=lambda message: True)
def menu(message):
    if message.chat.type == 'private':
        if message.text == "Расписание":
            inMurkup = types.InlineKeyboardMarkup(row_width=1)
            but4 = types.InlineKeyboardButton("Расписание на сегодня", callback_data='book1')
            but5 = types.InlineKeyboardButton("Расписание на завтра",callback_data='book2')
            but6 = types.InlineKeyboardButton("Поправки в расписании",callback_data='book3')

            inMurkup.add(but4, but5, but6)

            bot.send_message(message.chat.id, "Что именно интересует", reply_markup=inMurkup)
            
        elif message.text == "Ближайшие События":
            bot.send_message(message.chat.id, derek)
        
        elif message.text == "Рассылка":
            bot.send_message(message.chat.id, "В будущем сделаю функция автомотической рассылки ")

        else:
		        bot.send_message(message.chat.id, "Я не знаю что и ответить")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'book1':
                bot.send_message(call.message.chat.id, answer2)
            elif call.data == 'book2':
                bot.send_message(call.message.chat.id, answer1)
            elif call.data == 'book3':
                bot.send_message(call.message.chat.id, last_line)
            
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Что именно интересует",reply_markup=None)
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
				text='Встретимся на занятиях')
    except Exception as e:
		    print(repr(e))

bot.polling(none_stop=True, interval=0)
