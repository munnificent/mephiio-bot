# -*- coding: utf-8 -*-
from telebot import types
import os
import sys
from telebot import types
import telebot
from datetime import date
from datetime import datetime
import datetime
import requests
from bs4 import BeautifulSoup as BS

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)



API_TOKEN = "5725077388:AAENT--CKUVwwRxLA6gDQB2yHG17lqZ14NU"

bot = telebot.TeleBot(API_TOKEN)
admins = [736503376]

# работа с ip
joinedFile = open('data/id.txt','r')
joinedUsers = set()
for line in joinedFile:
    joinedUsers.add(line.strip())
joinedFile.close()

# функция даты 
def day(number):
    today1 = datetime.datetime.today().weekday() * number
    return today1

# старт
@bot.message_handler(commands=['start'])
def startJoin(message):
    if not str(message.chat.id) in joinedUsers:
        joinedFile = open('data/id.txt', 'a')
        joinedFile .write(str(message.chat.id) + '\n')
        joinedUsers.add(message.chat.id)
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("Расписание")
    but2 = types.KeyboardButton("Ближайшие События")
    but3 = types.KeyboardButton("Рассылка")
    markup.add(but1).add(but2).add(but3)
    
    stic = open('stic/welcome.tgs', 'rb')
    bot.reply_to(message, "Привет, {0.first_name}\nЧем могу помочь?".format(message.from_user),parse_mode='html',reply_markup=markup)
    bot.send_sticker(message.chat.id,stic)

# рассылка
@bot.message_handler(commands=['send'])
def notify(message):
    command_sender = message.from_user.id
    if command_sender in admins:
        msg = message.text[len('/send'):]
        with open(r'data/id.txt') as ids:
            for line in ids:
                user_id = int(line.strip("\n"))
                try:
                    bot.send_message(user_id,  f'Сообщение\n<b>{msg}<b>\n от</b> {command_sender}</b>', parse_mode='html')
                except Exception as e:
                    bot.send_message(command_sender, f'ошибка отправки сообщения юзеру - <b>{user_id}</b>', parse_mode='html')
    else:
        bot.send_message(command_sender, f'у вас нет прав для запуска команды')


if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        pass

#расписание меню
@bot.message_handler(func=lambda message: True)
def menu(message):
    if message.chat.type == 'private':
        if message.text == "Расписание":
            inMurkup = types.InlineKeyboardMarkup(row_width=1)
            but4 = types.InlineKeyboardButton("Расписание на сегодня", callback_data='data1')
            but5 = types.InlineKeyboardButton("Расписание на завтра",callback_data='data2')
            but6 = types.InlineKeyboardButton("Поправки в расписании",callback_data='data3')

            inMurkup.add(but4, but5, but6)

            bot.send_message(message.chat.id, "Что именно интересует", reply_markup=inMurkup)
            
        elif message.text == "Ближайшие События":
            #работа с словорями
            with open('dic/party.txt', 'r', encoding='UTF-8') as f: ## Открываем файл
                my_lines = list(f) ## Помещаем в список.
            party = my_lines[0]
            bot.send_message(message.chat.id, party)
        
        elif message.text == "Рассылка":
            bot.send_message(message.chat.id, "Автоматическая рассылка доступна админу\nТак же это поле для планирования событий")

        else:
		        bot.send_message(message.chat.id, "Я не знаю что и ответить")

# ответка расписанию
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'data1':
                today1 = day(1)
                if today1 == 0:
                    img = open('pic/monday.png', 'rb')
                    bot.send_photo(call.message.chat.id, img)
                elif today1 == 1:
                    img = open('pic/tuesday.png', 'rb')
                    bot.send_photo(call.message.chat.id, img)
                elif today1 == 2:
                    img = open('pic/wednesday.png', 'rb')
                    bot.send_photo(call.message.chat.id, img)
                elif today1 == 3:
                    img = open('pic/thursday.png', 'rb')
                    bot.send_photo(call.message.chat.id, img)
                elif today1 == 4:
                    img = open('pic/friday.png', 'rb')
                    bot.send_photo(call.message.chat.id, img)
                elif today1 == 5:
                    img = open('pic/saturday.png', 'rb')
                    bot.send_photo(call.message.chat.id, img)
                elif today1 == 6:
                    img = open('pic/saturday.png', 'rb')
                    bot.send_photo(call.message.chat.id, img)
                else:
                    bot.send_message(call.message.chat.id, "Ошибка")
            elif call.data == 'data2':
                today1 = day(1)
                if today1 == 6:
                    img = open('pic/monday.png', 'rb')
                    bot.send_photo(call.message.chat.id, img)
                elif today1 == 0:
                    img = open('pic/tuesday.png', 'rb')
                    bot.send_photo(call.message.chat.id, img)
                elif today1 == 1:
                    img = open('pic/wednesday.png', 'rb')
                    bot.send_photo(call.message.chat.id, img)
                elif today1 == 2:
                    img = open('pic/thursday.png', 'rb')
                    bot.send_photo(call.message.chat.id, img)
                elif today1 == 3:
                    img = open('pic/friday.png', 'rb')
                    bot.send_photo(call.message.chat.id, img)
                elif today1 == 4:
                    img = open('pic/saturday.png', 'rb')
                    bot.send_photo(call.message.chat.id, img)
                elif today1 == 5:
                    img = open('pic/saturday.png', 'rb')
                    bot.send_photo(call.message.chat.id, img)
                else:
                    bot.send_message(call.message.chat.id, "Error")
            elif call.data == 'data3':
                #работа с словорями
                with open('dic/corect.txt', 'r', encoding='UTF-8') as f: ## Открываем файл
                    my_lines = list(f) ## Помещаем в список.
                today1 = day(1)
                if today1 == 6:
                    corection1 = my_lines[today1]
                    corection2 = my_lines[0]
                else:
                    corection1 = my_lines[today1]
                    corection2 = my_lines[today1 + 1 ]

                bot.send_message(call.message.chat.id, corection1)
                bot.send_message(call.message.chat.id, corection2)
            
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Что именно интересует",reply_markup=None)
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
				text='Встретимся на занятиях')
    except Exception as e:
		    print(repr(e))


bot.polling(none_stop=True, interval=0)