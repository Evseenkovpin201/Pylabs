import os
import telebot
from telebot import types
import openpyxl

# Токен бота
TOKEN = '6153841655:AAGPjRAe651bNGDpMdEsvUwU7EJvaFJ5nZY'

# Создание бота
bot = telebot.TeleBot(TOKEN)

# Обрабатываем команду /sendfile (Для отправки ботом отчета)
@bot.message_handler(commands=['sendfile'])
def send_file(message):
    try:
        # Создание клавиатуры для пользователя для выбора файла
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        filepath = 'report.xlsx'
        # Открытие xlsx файла и добавление названий листов в клавиатуру
        workbook = openpyxl.load_workbook(filename=filepath)
        for ws in workbook.worksheets:
            keyboard.add(types.KeyboardButton(ws.title))
        # Отправка сообщения с клавиатурой
        bot.send_message(message.chat.id, "Выберите лист:", reply_markup=keyboard)
        # Добавление пользователя в очередь, ждущего выбора листа
        bot.register_next_step_handler(message, process_choice, workbook=workbook, filepath=filepath)
    except Exception as e:
        # В случае ошибки отправка сообщения с ошибкой
        bot.send_message(message.chat.id, f'Ошибка: {e}')

# Обрабатываем выбор листа
def process_choice(message, workbook, filepath):
    try:
        # Получение выбранного листа из сообщения
        selected_sheet = message.text
        # Открытие выбранного листа и чтение данных
        worksheet = workbook[selected_sheet]
        data = worksheet.values
        # Создание временного файла с данными
        temp_file = 'temp_file.xlsx'
        book = openpyxl.Workbook()
        sheet = book.active
        for row in data:
            sheet.append(row)
        book.save(temp_file)
        # Отправка временного файла пользователю
        with open(temp_file, 'rb') as f:
            bot.send_document(message.chat.id, f)
        # Удаление временного файла
        os.remove(temp_file)
    except Exception as e:
        # В случае ошибки отправка сообщения с ошибкой
        bot.send_message(message.chat.id, f'Ошибка: {e}')

# Обрабатываем команду /info (Для описания бота)
@bot.message_handler(commands=['info'])
def bot_info(message):
    bot.reply_to(message, 'Этот бот поможет следить за оценками вашего ребёнка,отправляя отчёт в формате excel')

# Обрабатываем команду /help (Для вывода списка команд бота)
@bot.message_handler(commands=['help'])
def bot_help(message):
    command_list = ['/info - информация о боте', '/help - список команд', '/sendfile - отправить отчет об отметка ребёнка']
    bot.send_message(message.chat.id, f'Список команд:\n\n{chr(10).join(command_list)}')

# Запускаем бота
if __name__ == '__main__':
    bot.polling(none_stop=True)