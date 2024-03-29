# mephiio-bot

# Телеграм бот для отправки расписания

Этот репозиторий содержит код для телеграм бота, который отправляет расписание студентам. Расписание, аудитории, преподаватели и другая информация хранятся в базе данных.

## Установка и настройка

1. Убедитесь, что у вас установлен Poetry. Если его нет, установите его, следуя инструкциям на [официальном сайте Poetry](https://python-poetry.org/docs/#installation).

2. Склонируйте репозиторий на свой локальный компьютер:

   ```
   git clone https://github.com/munnificent/mephiio-bot
   ```

3. Перейдите в директорию проекта:

   ```
   cd mephiio-bot
   ```

4. Установите зависимости с помощью Poetry:

   ```
   poetry install
   ```

5. В файле `info.py` и измените в нем все необходимые данные для работы программы:

   ```python
   # info.py

   TOKEN = 'your-telegram-bot-token'
   ```

6. Запустите бота:

   ```
   poetry run python main.py
   ```

## Используемые библиотеки и модули

- `telebot`: библиотека для работы с Telegram API.
- `os`: модуль для работы с операционной системой.
- `random`: модуль для генерации случайных чисел и выбора случайных элементов.
- `pendulum`: библиотека для работы с датами и временем.
- `sqlite3`: модуль для работы с базой данных SQLite.
- `PIL`: библиотека для работы с изображениями.
- `logging`: модуль для ведения логирования.
- `io`: модуль для работы с потоками ввода-вывода.
- `tempfile`: модуль для работы с временными файлами.
- `telebot.types`: модуль для работы с типами сообщений и объектами Telegram.

## Лицензия

Че хочу то и делаю