
from PIL import Image, ImageDraw, ImageFont 
import telebot 
from telebot import types 
import sqlite3 
import pendulum 
import io
import datetime
from data_set import days_of_week, TOKEN


bot = telebot.TeleBot(TOKEN)
almaty_timezone = pendulum.timezone("Asia/Almaty")

markup = types.ReplyKeyboardMarkup(resize_keyboard=True) 
today_button = types.KeyboardButton('Расписание на сегодня') 
tomorrow_button = types.KeyboardButton('Расписание на завтра') 
now_button = types.KeyboardButton('Следующая пара') 
markup.add(today_button, tomorrow_button, now_button)


def get_group(idTelegram):
    conn = sqlite3.connect('students.db')
    c =conn.cursor()
    c.execute("SELECT Students.Groupe FROM Students WHERE Students.Telegram=?",(idTelegram,))
    result = c.fetchone()
    conn.close()
    result = result[0]
    return result

def get_schedule(date, group):
    print(group)
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT Schedule.Start_time, Schedule.End_time, Lessons.Course, Teachers.Name, Audience.Number FROM Schedule JOIN Lessons ON Schedule.id_lesson = Lessons.id JOIN Teachers ON Lessons.Teacher = Teachers.id JOIN Audience ON Schedule.id_audience = Audience.id WHERE Schedule.Date = ? AND Schedule.\"Group\" = ?", (date, group))

    rows = c.fetchall()
    schedule = []
    for row in rows:
        schedule.append(list(row))
    conn.close()
    return schedule

def get_schedule_for_time(input_time, day_of_week, group):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()

    # Конвертируем входное время в объект datetime.time
    input_time_obj = datetime.datetime.strptime(input_time, "%H:%M").time()


    # Извлекаем все строки с временем для указанной группы и дня недели
    c.execute("SELECT Start_time, End_time FROM Schedule WHERE \"Group\" = ? AND Date = ?", (group, day_of_week))
    rows = c.fetchall()

    # Проверяем каждую строку на наличие введенного времени в диапазоне старт-конец
    for row in rows:
        start_time_obj = datetime.datetime.strptime(row[0], "%H:%M").time()
        end_time_obj = datetime.datetime.strptime(row[1], "%H:%M").time()

        if start_time_obj <= input_time_obj <= end_time_obj:
            # Возвращаем расписание для найденного времени, дня недели и группы
            c.execute("SELECT Schedule.Start_time, Schedule.End_time, Lessons.Course, Teachers.Name, Audience.Number FROM Schedule JOIN Lessons ON Schedule.id_lesson = Lessons.id JOIN Teachers ON Lessons.Teacher = Teachers.id JOIN Audience ON Schedule.id_audience = Audience.id WHERE Schedule.Start_time=? AND Schedule.Date=? AND Schedule.\"Group\"=?", (row[0], day_of_week, group))
            result = c.fetchall()
            conn.close()
            return result

    # Возвращаем None, если введенное время не найдено в диапазоне старт-конец для указанной группы и дня недели
    conn.close()
    return None

def draw_cell(draw, x, y, cell_width, cell_height, text, font, text_color):
    draw.rectangle((x, y, x + cell_width, y + cell_height), outline=(140, 73, 58), width=2)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    tx, ty = x + (cell_width - text_width) // 2, y + (cell_height - text_height) // 2
    draw.text((tx, ty), text, fill=text_color, font=font)

def generate_schedule_image(schedule):
    background_image = Image.open("background.png")
    draw = ImageDraw.Draw(background_image)
    font = ImageFont.truetype("phage.ttf", size=28)
    text_color = (242, 228, 216)

    header = ["Начало", "конец", "Предмет", "Преподаватель", "Кабинет"]
    image_width, image_height = background_image.size
    x_margin, y_margin = 50, 50
    table_width, table_height = image_width - 2 * x_margin, image_height - 2 * y_margin
    cell_width, cell_height = table_width // len(header), table_height // (len(schedule) + 1)
    x, y = x_margin, y_margin

    for i, text in enumerate(header):
        draw_cell(draw, x, y, cell_width, cell_height, text, font, text_color)
        x += cell_width

    y += cell_height
    for row in schedule:
        x = x_margin
        for text in row:
            draw_cell(draw, x, y, cell_width, cell_height, text, font, text_color)
            x += cell_width
        y += cell_height

    return background_image

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_name = message.from_user.first_name
    bot.send_message(message.chat.id, f"Привет, {user_name}!")
    with open("stick/welcome.tgs", "rb") as sticker:
        bot.send_sticker(message.chat.id, sticker)

def send_schedule_image(chat_id, schedule, message_text):
    image = generate_schedule_image(schedule)
    with io.BytesIO() as output:
        image.save(output, format='PNG')
        output.seek(0)
        bot.send_message(chat_id, message_text, reply_markup=markup)
        bot.send_photo(chat_id, photo=output)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    idT = get_group(chat_id)

    almaty_timezone = 'Asia/Almaty'
    days_of_week = {
        'Monday': 'Понедельник',
        'Tuesday': 'Вторник',
        'Wednesday': 'Среда',
        'Thursday': 'Четверг',
        'Friday': 'Пятница',
        'Saturday': 'Суббота',
        'Sunday': 'Воскресенье'
    }

    if message.text == 'Расписание на сегодня':
        today = pendulum.today(almaty_timezone).strftime("%A")
        schedule = get_schedule(days_of_week[today], idT)
        send_schedule_image(chat_id, schedule, 'Вот расписание на сегодня')

    elif message.text == 'Расписание на завтра':
        tomorrow = pendulum.tomorrow(almaty_timezone).strftime("%A")
        schedule = get_schedule(days_of_week[tomorrow], idT)
        send_schedule_image(chat_id, schedule, 'Вот расписание на завтра')

    elif message.text == 'Следующая пара':
        today = pendulum.today(almaty_timezone).strftime("%A")
        now = pendulum.now(almaty_timezone).add(hours=1, minutes=40).strftime('%H:%M')
        schedule = get_schedule_for_time(now, days_of_week[today], idT)
        formatted_schedule = f"{schedule[0][0]}-{schedule[0][1]} {schedule[0][2]} {schedule[0][3]} аудитория {schedule[0][4]}"
        bot.send_message(chat_id, f"Следующая пара в {formatted_schedule}", reply_markup=markup)

    else:
        bot.send_message(chat_id, 'Я не понимаю, что вы хотите. Пожалуйста, выберите команду из списка.', reply_markup=markup)
if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        pass

bot.polling()