import telebot
import os
import random
import pendulum
import sqlite3
from PIL import Image, ImageDraw, ImageFont
import logging
from io import BytesIO
import tempfile
from telebot import types
from info import *  # содержит TOKEN BACKGROUND_DIR DATABASE_FILE weekdays

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the bot
bot = telebot.TeleBot(TOKEN)

# Список идентификаторов администраторов
admin_ids = [6222762191, 736503376]

# Обработчик команды от администратора
@bot.message_handler(commands=['send'])
def send_message_to_students(message):
    # Проверка, является ли отправитель команды администратором
    if message.from_user.id not in admin_ids:
        bot.reply_to(message, 'Вы не являетесь администратором!')
        return

    # Получение данных из сообщения администратора
    message_parts = message.text.split()
    if len(message_parts) < 2:
        bot.reply_to(message, 'Недостаточно аргументов! Используйте команду в формате: /send group_name text_message')
        return

    group_name = message_parts[1]
    text_message = ' '.join(message_parts[2:])

    # Получение списка telegram_id студентов по группе
    with sqlite3.connect(DATABASE_FILE) as connection:
        cursor = connection.cursor()
        query = "SELECT telegram_id FROM student WHERE group_name = ?"
        cursor.execute(query, (group_name,))
        results = cursor.fetchall()
    telegram_ids = [result[0] for result in results]

    # Отправка сообщения в чат каждого студента
    for telegram_id in telegram_ids:
        bot.send_message(chat_id=telegram_id, text=text_message)

    # Отправка подтверждения администратору
    bot.reply_to(message, 'Рассылка выполнена успешно!')

# Database query functions
def get_student_group(telegram_chat_id):
    with sqlite3.connect(DATABASE_FILE) as connection:
        cursor = connection.cursor()
        query = "SELECT group_name FROM student WHERE telegram_id = ?"
        cursor.execute(query, (telegram_chat_id,))
        result = cursor.fetchone()
        if result is not None:
            return result[0]
        else:
            raise ValueError("Студент с telegram_chat_id {} не найден".format(telegram_chat_id))

def get_schedule(current_day, student_group):
    with sqlite3.connect(DATABASE_FILE) as connection:
        cursor = connection.cursor()
        query = """
        SELECT s.time_start, s.time_end, c.subject_name, a.number, t.surname
        FROM schedule AS s
        JOIN subject AS c ON s.id_subject = c.id
        JOIN auditory AS a ON s.id_auditory = a.id
        JOIN teachers AS t ON c.teacher_id = t.id
        WHERE s.week_day = ? AND s.group_name = ?
        """
        cursor.execute(query, (current_day, student_group))
        return cursor.fetchall()

def get_next_lesson(current_day, student_group, time_formatted):
    with sqlite3.connect(DATABASE_FILE) as connection:
        cursor = connection.cursor()
        query = """
        SELECT s.week_day, s.time_start, s.time_end, c.subject_name, a.number
        FROM schedule AS s
        JOIN subject AS c ON s.id_subject = c.id
        JOIN auditory AS a ON s.id_auditory = a.id
        WHERE s.week_day = ? AND s.group_name = ? AND s.time_start > ?
        ORDER BY s.time_start
        LIMIT 1
        """
        cursor.execute(query, (current_day, student_group, time_formatted))
        return cursor.fetchone()

def generate_schedule_image(telegram_chat_id, current_day):
    # Загрузка случайного фонового изображения 1200 на 675 размер
    backgrounds = os.listdir(BACKGROUND_DIR)
    background_image = random.choice(backgrounds)
    background_path = os.path.join(BACKGROUND_DIR, background_image)
    image = Image.open(background_path)

    # получение расписания
    student_group = get_student_group(telegram_chat_id)
    schedule = get_schedule(current_day, student_group)

    # Размеры изображения и таблицы
    image_width, image_height = image.size
    table_x = 50
    table_y = 50
    cell_width = (image_width - table_x * 2) // 5
    cell_height = 50

    # Создание изображения
    draw = ImageDraw.Draw(image)


    # Шрифт и размеры текста
    font_path = os.path.join(FONT_DIR, 'SANTELLO.ttf')
    font = ImageFont.truetype(font_path, 22)
    header_font = ImageFont.truetype(font_path, 24)
    

    # Заголовки таблицы
    headers = ["Начало", "Конец", "Предмет", "Аудитория", "Преподаватель"]

    # Отрисовка заголовков
    for i, header in enumerate(headers):
        x = table_x + cell_width * i
        y = table_y
        draw.rectangle([(x, y), (x + cell_width, y + cell_height)], outline=color_cell, fill=color_header)
        draw.text((x + 10, y + 10  ), header, font=header_font, fill=color_text1)

    # Отрисовка расписания
    for i, entry in enumerate(schedule):
        for j, value in enumerate(entry):
            x = table_x + cell_width * j
            y = table_y + cell_height * (i + 1)
            draw.rectangle([(x, y), (x + cell_width, y + cell_height)], outline=color_cell, fill=color_tab)
            draw.text((x + 10, y + 10), str(value), font=font, fill=color_text2)

    # Создание объекта BytesIO для хранения изображения в памяти
    image_bytes = BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes.seek(0)

    return image_bytes
    
# Start command handler
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, f"Привет {message.from_user.first_name}! Я бот-рассыльщик расписания и уведомлений Университета КазНПУ. Я готов помочь тебе быть в курсе всех актуальных событий и изменений в учебном процессе. Для получения информации просто обратись ко мне. Давай вместе сделаем твою учебу более организованной и успешной!")
    stickers = os.listdir('stic')
    sticker = open(os.path.join('stic', random.choice(stickers)), 'rb')
    bot.send_sticker(message.chat.id, sticker)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Расписание на сегодня")
    item2 = types.KeyboardButton("Расписание на завтра")
    item3 = types.KeyboardButton("Следующая пара")
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, "Выберите одну из опций:", reply_markup=markup)

def send_image_to_telegram(chat_id, image_bytes):
    # Save the BytesIO object as a temporary file
    with tempfile.NamedTemporaryFile(suffix='.png') as temp_file:
        temp_file.write(image_bytes.getvalue())
        temp_file.seek(0)

        # Send the image as a photo message
        bot.send_photo(chat_id, temp_file)

# Message handler
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "Расписание на сегодня":
        timezone = pendulum.timezone("Asia/Almaty")
        current_day = pendulum.now(timezone).format("dddd")
        current_day = weekdays[current_day]
        bot.send_message(message.chat.id, "Расписание на сегодня:")
        try:
            schedule_image = generate_schedule_image(message.chat.id, current_day)
            send_image_to_telegram(message.chat.id, schedule_image)
        except Exception as e:
            logger.error("Error generating schedule image: %s", str(e))
            bot.send_message(message.chat.id, "An error occurred while generating the schedule image.")
            bot.send_message(message.chat.id, " Возможно вас нет в базе, обратитесь к @munificent_archon   ")

    elif message.text == "Расписание на завтра":
        timezone = pendulum.timezone("Asia/Almaty")
        tomorrow = pendulum.now(timezone).add(days=1)
        tomorrow_day = tomorrow.format("dddd")
        tomorrow_day = weekdays[tomorrow_day]
        bot.send_message(message.chat.id, "Расписание на завтра:")
        try:
            schedule_image = generate_schedule_image(message.chat.id, tomorrow_day)
            send_image_to_telegram(message.chat.id, schedule_image)
        except Exception as e:
            logger.error("Error generating schedule image: %s", str(e))
            bot.send_message(message.chat.id, "An error occurred while generating the schedule image.")

    elif message.text == "Следующая пара":
        timezone = pendulum.timezone("Asia/Almaty")
        current_time = pendulum.now(timezone).time()
        current_day = pendulum.now(timezone).format("dddd")
        current_day = weekdays[current_day]
        time_formatted = current_time.strftime("%H:%M")
        try:
            student_group = get_student_group(message.chat.id)
            next_lesson = get_next_lesson(current_day, student_group, time_formatted)
            if next_lesson is not None:
                week_day, time_start, time_end, course_name, auditory_number = next_lesson
                next_lesson_text = "Следующая пара:\n{}: {} - {} предмет {} аудитория {}".format(
                    week_day, time_start, time_end, course_name, auditory_number
                )
            else:
                next_lesson_text = "На сегодня больше нет пар."
            bot.send_message(message.chat.id, next_lesson_text)
        except Exception as e:
            logger.error("Error getting next lesson: %s", str(e))
            bot.send_message(message.chat.id, "An error occurred while getting the next lesson.")



# Start the bot
bot.infinity_polling(timeout=10, long_polling_timeout = 5)