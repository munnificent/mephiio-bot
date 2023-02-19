import os
import pendulum
import telebot
import sys
from telebot import types

API_TOKEN ="5977431904:AAEOhW9tVQDGljpWo5GM3Pb-aQ4UGLFH924"
admins = [736503376]

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

almaty_timezone = pendulum.timezone("Asia/Almaty")

with open("data/zvvs1.txt", "r") as file1:
    zvvs1_users = [line.strip() for line in file1]

with open("data/zvvs2.txt", "r") as file2:
    zvvs2_users = [line.strip() for line in file2]

def handle_message(user_id, message):
    current_day = pendulum.now(almaty_timezone).strftime("%A")
    image_folder = ""
    image_name = ""
    if str(user_id) in zvvs1_users:
        image_folder = "image1"
        image_name = current_day + "1" + ".png"
        print(image_name)
    elif str(user_id) in zvvs2_users:
        print("hello")
        image_folder = "image2"
        image_name = current_day + "2" + ".png"
        print(image_name)
    else:
        return

    image_path = os.path.join(image_folder, image_name)
    print(image_path)
    send_image(user_id, image_path)

def send_image(user_id, image_path):
    bot = telebot.TeleBot(API_TOKEN)
    with open(image_path, 'rb') as f:
        bot.send_photo(user_id,f)

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_name = message.from_user.first_name
    bot.send_message(message.chat.id, f"Привет, {user_name}!")
    with open("stick/welcome.tgs", "rb") as sticker:
        bot.send_sticker(message.chat.id, sticker)

@bot.message_handler(commands=['today'])
def handle_schedule(message):
    user_id = message.chat.id
    handle_message(user_id, message)

@bot.message_handler(commands=['send'])
def handle_send(message):
    if message.from_user.id not in admins:
        return

    text = message.text.split(" ", 1)[1]

    for user_id in zvvs1_users + zvvs2_users:
        bot.send_message(user_id, text)

@bot.message_handler(commands=['tomorrow'])
def handle_tomorrow(message):
    user_id = message.chat.id
    tomorrow = pendulum.now(almaty_timezone).add(days=1).strftime("%A")
    if str(user_id) in zvvs1_users:
        image_folder = "image1"
        image_name = tomorrow + "1" + ".png"
    elif str(user_id) in zvvs2_users:
        image_folder = "image2"
        image_name = tomorrow + "2" + ".png"
    else:
        return

    image_path = os.path.join(image_folder, image_name)
    send_image(user_id, image_path)


if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        pass

bot.polling()