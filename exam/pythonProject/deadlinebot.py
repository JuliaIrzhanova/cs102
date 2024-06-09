import telebot
from telebot import types
import json
import gspread
import pandas as pd

bot = telebot.TeleBot('7194752809:AAHOLw8YVy2y8d2-ikZJKAQIEEsFuEATKoM')

def is_table_connected():
    try:
        with open("tables.json") as json_file:
            tables = json.load(json_file)
        return len(tables) > 0
    except FileNotFoundError:
        return False

@bot.message_handler(commands=["start"])
def start(message):
    start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if not is_table_connected():
        start_markup.row("Подключить Google-таблицу")
    start_markup.row("Посмотреть дедлайны на этой неделе")
    start_markup.row("Внести новый дедлайн")
    start_markup.row("Редактировать предметы")
    info = bot.send_message(message.chat.id, "Что хотите сделать?", reply_markup=start_markup)
    bot.register_next_step_handler(info, choose_action)

def choose_action(message):
    if message.text == "Подключить Google-таблицу":
        connect_table(message)
    elif message.text == "Редактировать предметы":
        choose_subject_action(message)
    elif message.text == "Редактировать дедлайн":
        choose_deadline_action(message)
    elif message.text == "Посмотреть дедлайны на этой неделе":
        view_deadlines(message)

def connect_table(message):
    msg = bot.send_message(message.chat.id, "Отправьте ссылку на Google-таблицу:")
    bot.register_next_step_handler(msg, save_table_url)

def save_table_url(message):
    url = message.text
    sheet_id = url.split("/d/")[1].split("/")[0]
    try:
        with open("tables.json") as json_file:
            tables = json.load(json_file)
        title = len(tables) + 1
        tables[title] = {"url": url, "id": sheet_id}
    except FileNotFoundError:
        tables = {1: {"url": url, "id": sheet_id}}
    with open("tables.json", 'w') as json_file:
        json.dump(tables, json_file)
    bot.send_message(message.chat.id, "Таблица подключена!")
    display_disciplines(message.chat.id)

def access_current_sheet():
    """ Обращаемся к Google-таблице """
    with open("tables.json") as json_file:
        tables = json.load(json_file)
    sheet_id = tables[max(tables)]["id"]
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    gc = gspread.service_account(filename="credentials.json")
    sh = gc.open_by_key(sheet_id)
    worksheet = sh.sheet1
    # Преобразуем Google-таблицу в таблицу pandas
    df = pd.DataFrame(worksheet.get_all_records())
    print(df.columns)
    return worksheet, tables[max(tables)]["url"], df

def display_disciplines(chat_id):
    worksheet, url, df = access_current_sheet()
    response = "Сохраненные дисциплины:\n"
    for index, row in df.iterrows():
        response += f"<a href='{url}'>{row['Subject']}</a>: {row['Grade']}\n"
    bot.send_message(chat_id, response, parse_mode='HTML')

def view_deadlines(message):
    worksheet, url, df = access_current_sheet()
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')  # Преобразование строк в даты
    upcoming_deadlines = df[df['Date'] <= pd.Timestamp.now() + pd.DateOffset(days=7)]
    response = "Дедлайны на этой неделе:\n"
    for index, row in upcoming_deadlines.iterrows():
        response += f"{row['Subject']}: {row['Date'].strftime('%d/%m/%Y')}\n"
    bot.send_message(message.chat.id, response)

def choose_subject_action(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row("Добавить предмет", "Редактировать предмет", "Удалить предмет")
    msg = bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)
    bot.register_next_step_handler(msg, handle_subject_action)

def handle_subject_action(message):
    if message.text == "Добавить предмет":
        add_new_subject(message)
    elif message.text == "Редактировать предмет":
        update_subject(message)
    elif message.text == "Удалить предмет":
        delete_subject(message)

def choose_deadline_action(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row("Добавить дедлайн", "Изменить дедлайн")
    msg = bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)
    bot.register_next_step_handler(msg, handle_deadline_action)

def handle_deadline_action(message):
    if message.text == "Добавить дедлайн":
        add_new_deadline(message)
    elif message.text == "Изменить дедлайн":
        update_deadline(message)

def choose_removal_action(message):
    msg = bot.send_message(message.chat.id, "Вы действительно хотите удалить все? (да/нет)")
    bot.register_next_step_handler(msg, handle_removal_action)

def handle_removal_action(message):
    if message.text.lower() == "да":
        clear_subject_list(message)
    else:
        bot.send_message(message.chat.id, "Удаление отменено.")

def add_new_subject(message):
    msg = bot.send_message(message.chat.id, "Введите название нового предмета:")
    bot.register_next_step_handler(msg, add_new_subject_url)

def add_new_subject_url(message):
    title = message.text
    msg = bot.send_message(message.chat.id, "Введите ссылку на таблицу предмета:")
    bot.register_next_step_handler(msg, lambda msg: save_new_subject(msg, title))

def save_new_subject(message, title):
    url = message.text
    worksheet, _, _ = access_current_sheet()
    worksheet.append_row([title, url])  # Добавляем новую строку с предметом
    bot.send_message(message.chat.id, f"Предмет '{title}' добавлен.")

def update_subject(message):
    msg = bot.send_message(message.chat.id, "Введите название предмета, который хотите редактировать:")
    bot.register_next_step_handler(msg, get_subject_for_update)

def get_subject_for_update(message):
    subject = message.text
    worksheet, _, df = access_current_sheet()
    if subject in df['Subject'].values:
        msg = bot.send_message(message.chat.id, "Введите новое название предмета:")
        bot.register_next_step_handler(msg, lambda msg: save_subject_update(msg, subject))
    else:
        bot.send_message(message.chat.id, f"Предмет '{subject}' не найден.")

def save_subject_update(message, old_subject):
    new_subject = message.text
    worksheet, _, df = access_current_sheet()
    cell = worksheet.find(old_subject)
    worksheet.update_cell(cell.row, 1, new_subject)  # Обновляем название предмета
    bot.send_message(message.chat.id, f"Название предмета '{old_subject}' изменено на '{new_subject}'.")

def delete_subject(message):
    msg = bot.send_message(message.chat.id, "Введите название предмета, который хотите удалить:")
    bot.register_next_step_handler(msg, get_subject_for_delete)

def get_subject_for_delete(message):
    subject = message.text
    worksheet, _, df = access_current_sheet()
    if subject in df['Subject'].values:
        cell = worksheet.find(subject)
        worksheet.delete_rows(cell.row)  # Удаляем строку с предметом
        bot.send_message(message.chat.id, f"Предмет '{subject}' удален.")
    else:
        bot.send_message(message.chat.id, f"Предмет '{subject}' не найден.")

def clear_subject_list(message):
    worksheet, _, df = access_current_sheet()
    worksheet.delete_rows(2, worksheet.row_count)
    bot.send_message(message.chat.id, "Все предметы удалены.")

def add_new_deadline(message):
    msg = bot.send_message(message.chat.id, "Введите название предмета для добавления дедлайна:")
    bot.register_next_step_handler(msg, get_subject_for_deadline)

def get_subject_for_deadline(message):
    subject = message.text
    msg = bot.send_message(message.chat.id, f"Введите дату дедлайна для '{subject}' (в формате ДД/ММ/ГГГГ):")
    bot.register_next_step_handler(msg, lambda msg: save_new_deadline(msg, subject))

def save_new_deadline(message, subject):
    deadline_date = message.text
    worksheet, _, df = access_current_sheet()
    if subject in df['Subject'].values:
        cell = worksheet.find(subject)
        worksheet.update_cell(cell.row, 3, deadline_date)  # Обновляем дату дедлайна
        bot.send_message(message.chat.id, f"Дедлайн для '{subject}' добавлен/обновлен на {deadline_date}.")
    else:
        bot.send_message(message.chat.id, f"Предмет '{subject}' не найден.")

def update_deadline(message):
    msg = bot.send_message(message.chat.id, "Введите название предмета для изменения дедлайна:")
    bot.register_next_step_handler(msg, get_subject_for_deadline_edit)

def get_subject_for_deadline_edit(message):
    subject = message.text
    msg = bot.send_message(message.chat.id, f"Введите новую дату дедлайна для '{subject}' (в формате ДД/ММ/ГГГГ):")
    bot.register_next_step_handler(msg, lambda msg: save_new_deadline(msg, subject))

if __name__ == "__main__":
    bot.polling(none_stop=True)
