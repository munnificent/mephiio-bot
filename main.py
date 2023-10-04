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
from telebot.apihelper import ApiException
from info import *  # содержит TOKEN BACKGROUND_DIR DATABASE_FILE weekdays

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the bot
bot = telebot.TeleBot(TOKEN)

# Список идентификаторов администраторов
admin_ids = [6222762191, 736503376]

@bot.message_handler(commands=['send'])
def send_message_to_students(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, 'Вы не являетесь администратором!')
        return

    group_name, text_message = parse_admin_message(message.text)
    if not group_name or not text_message:
        bot.reply_to(message, 'Недостаточно аргументов! Используйте команду в формате: /send group_name text_message')
        return

    telegram_ids = fetch_students_telegram_ids(group_name)
    send_messages_to_students(telegram_ids, text_message)

    bot.reply_to(message, 'Рассылка выполнена успешно!')


def is_admin(user_id):
    return user_id in admin_ids


def parse_admin_message(text):
    message_parts = text.split()
    if len(message_parts) < 2:
        return None, None
    group_name = message_parts[1]
    text_message = ' '.join(message_parts[2:])
    return group_name, text_message


def fetch_students_telegram_ids(group_name):
    with sqlite3.connect(DATABASE_FILE) as connection:
        cursor = connection.cursor()
        query = "SELECT telegram_id FROM student WHERE group_name = ?"
        cursor.execute(query, (group_name,))
        results = cursor.fetchall()
    return [result[0] for result in results]


def send_messages_to_students(telegram_ids, text_message):
    for telegram_id in telegram_ids:
        try:
            bot.send_message(chat_id=telegram_id, text=text_message)
        except ApiException as e:
            if e.description == "Forbidden: bot was blocked by the user":
                error_message = f"Attention please! The user {telegram_id} has blocked the bot. I can't send anything to them."
                notify_admins(error_message)

def notify_admins(message):
    for admin_id in admin_ids:
        bot.send_message(chat_id=admin_id, text=message)


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
    # Load random background image of size 1200x675
    background_path = get_random_background()
    image = Image.open(background_path)

    # Fetch the schedule
    student_group = get_student_group(telegram_chat_id)
    schedule = get_schedule(current_day, student_group)

    # Image and table dimensions
    image_width, image_height = image.size
    table_x = 50
    table_y = 50
    cell_width = (image_width - table_x * 2) // 5
    cell_height = 50

    # Create image drawing context
    draw = ImageDraw.Draw(image)

    # Set font and text sizes
    font_path = os.path.join(FONT_DIR, 'SANTELLO.ttf')
    font = ImageFont.truetype(font_path, 22)
    header_font = ImageFont.truetype(font_path, 24)

    # Draw the table headers
    draw_table_headers(draw, table_x, table_y, cell_width, cell_height, header_font)

    # Draw the schedule
    draw_schedule(draw, table_x, table_y, cell_width, cell_height, font, schedule)

    # Convert image to bytes
    image_bytes = BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes.seek(0)

    return image_bytes


def get_random_background():
    backgrounds = os.listdir(BACKGROUND_DIR)
    background_image = random.choice(backgrounds)
    return os.path.join(BACKGROUND_DIR, background_image)


def draw_table_headers(draw, x, y, cell_width, cell_height, font):
    headers = ["Начало", "Конец", "Предмет", "Аудитория", "Преподаватель"]

    for i, header in enumerate(headers):
        cell_x = x + cell_width * i
        draw_cell(draw, cell_x, y, cell_width, cell_height, header, font, color_header, color_text1)


def draw_schedule(draw, x, y, cell_width, cell_height, font, schedule):
    for i, entry in enumerate(schedule):
        row_y = y + cell_height * (i + 1)
        for j, value in enumerate(entry):
            cell_x = x + cell_width * j
            draw_cell(draw, cell_x, row_y, cell_width, cell_height, str(value), font, color_tab, color_text2)


def draw_cell(draw, x, y, width, height, text, font, fill_color, text_color):
    draw.rectangle([(x, y), (x + width, y + height)], outline=color_cell, fill=fill_color)
    draw.text((x + 10, y + 10), text, font=font, fill=text_color)

    
@bot.message_handler(commands=['start'])
def start_handler(message):
    # Send a greeting message
    greeting_msg = (f"Привет {message.from_user.first_name}! Я бот-рассыльщик расписания и уведомлений Университета КазНПУ. "
                    "Я готов помочь тебе быть в курсе всех актуальных событий и изменений в учебном процессе. "
                    "Для получения информации просто обратись ко мне. Давай вместе сделаем твою учебу более организованной и успешной!")
    bot.send_message(message.chat.id, greeting_msg)
    
    # Send a random sticker
    stickers = os.listdir('stic')
    sticker_path = os.path.join('stic', random.choice(stickers))
    with open(sticker_path, 'rb') as sticker:
        bot.send_sticker(message.chat.id, sticker)
    
    # Send a keyboard with options
    send_options_keyboard(message.chat.id)


def send_options_keyboard(chat_id):
    """Sends a keyboard with options to the user."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    options = ["Расписание на сегодня", "Расписание на завтра", "Следующая пара"]
    for option in options:
        markup.add(types.KeyboardButton(option))
    bot.send_message(chat_id, "Выберите одну из опций:", reply_markup=markup)


def send_image_to_telegram(chat_id, image_bytes):
    # Save the BytesIO object as a temporary file
    with tempfile.NamedTemporaryFile(suffix='.png') as temp_file:
        temp_file.write(image_bytes.getvalue())
        temp_file.seek(0)

        # Send the image as a photo message
        bot.send_photo(chat_id, temp_file)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    def get_day_based_on_message(msg):
        """Returns the current day or tomorrow based on the input message."""
        timezone = pendulum.timezone("Asia/Almaty")
        if msg == "Расписание на сегодня":
            day = pendulum.now(timezone).format("dddd")
        elif msg == "Расписание на завтра":
            day = pendulum.now(timezone).add(days=1).format("dddd")
        else:
            day = None
        return weekdays.get(day) if day else None
    
    def send_schedule_image_error(chat_id):
        """Sends an error message when there's an issue with the schedule image."""
        logger.error("Error generating schedule image: %s", str(e))
        bot.send_message(chat_id, "An error occurred while generating the schedule image.")
        bot.send_message(chat_id, " Возможно вас нет в базе, обратитесь к @munificent_archon")
    
    def send_next_lesson_error(chat_id):
        """Sends an error message when there's an issue with getting the next lesson."""
        logger.error("Error getting next lesson: %s", str(e))
        bot.send_message(chat_id, "An error occurred while getting the next lesson.")

    user_messages = {
        "Расписание на сегодня": "Расписание на сегодня:",
        "Расписание на завтра": "Расписание на завтра:"
    }

    if message.text in user_messages:
        bot.send_message(message.chat.id, user_messages[message.text])
        day = get_day_based_on_message(message.text)
        if day:
            try:
                schedule_image = generate_schedule_image(message.chat.id, day)
                send_image_to_telegram(message.chat.id, schedule_image)
            except Exception as e:
                send_schedule_image_error(message.chat.id)
                
    elif message.text == "Следующая пара":
        timezone = pendulum.timezone("Asia/Almaty")
        current_day = get_day_based_on_message("Расписание на сегодня")
        current_time = pendulum.now(timezone).time()
        time_formatted = current_time.strftime("%H:%M")
        try:
            student_group = get_student_group(message.chat.id)
            next_lesson = get_next_lesson(current_day, student_group, time_formatted)
            if next_lesson:
                week_day, time_start, time_end, course_name, auditory_number = next_lesson
                next_lesson_text = f"Следующая пара:\n{week_day}: {time_start} - {time_end} предмет {course_name} аудитория {auditory_number}"
            else:
                next_lesson_text = "На сегодня больше нет пар."
            bot.send_message(message.chat.id, next_lesson_text)
        except Exception as e:
            send_next_lesson_error(message.chat.id)




# Start the bot
bot.infinity_polling(timeout=10, long_polling_timeout = 5)