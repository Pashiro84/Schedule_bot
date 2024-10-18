import schedule as sch
import week_day as wd
import json
from datetime import datetime, timedelta
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, ContextTypes, filters, CallbackQueryHandler
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
import os
import shedulmes as smes




# Устанавливаем временную зону Красноярска
krasnoyarsk_tz = pytz.timezone('Asia/Krasnoyarsk')



#Сохранение настроек

# Имя файла для сохранения данных пользователей
USER_SETTINGS_FILE = 'user_settings.json'

# Загрузка данных пользователей из файла
def load_user_settings():
    if os.path.exists(USER_SETTINGS_FILE):
        with open(USER_SETTINGS_FILE, 'r') as file:
            return json.load(file)
    return {}

# Сохранение данных пользователей в файл
def save_user_settings():
    with open(USER_SETTINGS_FILE, 'w') as file:
        json.dump(user_settings, file, indent=4)

# Загрузка настроек пользователей при запуске
user_settings = load_user_settings()




# Функция для старта бота и регистрации пользователя
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    # Инициализируем настройки пользователя, если их нет
    if user_id not in user_settings:
        keyboard = [[InlineKeyboardButton("Подгруппа А", callback_data='group_a'), InlineKeyboardButton("Подгруппа Б", callback_data='group_b')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('Привет! Я бот, который напоминает о расписании уроков. Пожайлуста, выберете подгруппу', reply_markup=reply_markup)
    else:
        keyboard = [
            ["Пары сегодня", "Пары завтра"],
            ["Расписание на неделю"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text('Привет! Я бот, который напоминает о расписании уроков.', reply_markup=reply_markup)


async def time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    today = datetime.now(krasnoyarsk_tz).strftime('%A')
    current_time = datetime.now(krasnoyarsk_tz)
    await update.message.reply_text(f'Время в Красноярске {today}, {current_time}.')


# Функция для отображения пар на сегодня
async def show_today(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        today = datetime.now(krasnoyarsk_tz).strftime('%A')
        user_id = str(update.effective_user.id)
        subgroup = user_settings[user_id]['subgroup']
        await update.message.reply_text(smes.shedule_day('сегодня',today,subgroup))
    except Exception as e:
        await update.message.reply_text(f'Произошла ошибка: пользователь не найден. (наберите /start)\n {e}')


# Функция для отображения пар на завтра
async def show_tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        tomorrow = (datetime.now(krasnoyarsk_tz) + timedelta(days=1)).strftime('%A')
        user_id = str(update.effective_user.id)
        subgroup = user_settings[user_id]['subgroup']
        await update.message.reply_text(smes.shedule_day('завтра',tomorrow,subgroup))
    except Exception as e:
        await update.message.reply_text(f'Произошла ошибка: пользователь не найден. (наберите /start)\n {e}')

# Функция для отображения расписания на неделю
async def show_week(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_id = str(update.effective_user.id)
        subgroup = user_settings[user_id]['subgroup']
        await update.message.reply_text(smes.shedule_week(subgroup))
    except Exception as e:
        await update.message.reply_text(f'Произошла ошибка: пользователь не найден. (наберите /start)\n {e}')


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Обязательный ответ на callback_query
    user_id = str(update.effective_user.id)

    # Определение клавиатуры
    keyboard = [
        ["Пары сегодня", "Пары завтра"],
        ["Расписание на неделю"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    # Обработка выбора пользователя
    if query.data == 'group_a':
        # Корректное обновление настроек пользователя
        user_settings[user_id] = {'reminder_enabled': True, 'subgroup': "A"}
        save_user_settings()
        await query.edit_message_text(text="Вы выбрали подгруппу А.")  # Инлайн-клавиатура не поддерживает ReplyKeyboardMarkup
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Вы можете посмотреть расписание на сегодня, на завтра, на неделю.", reply_markup=reply_markup)

    elif query.data == 'group_b':
        user_settings[user_id] = {'reminder_enabled': True, 'subgroup': "B"}
        save_user_settings()
        await query.edit_message_text(text="Вы выбрали подгруппу Б.")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Вы можете посмотреть расписание на сегодня, на завтра, на неделю.", reply_markup=reply_markup)

# Основная функция для запуска бота
def main():
    try:
        # Замените 'YOUR_BOT_TOKEN' на токен вашего бота
        application = Application.builder().token("YOUR_BOT_TOKEN").build()

        # Регистрация команд и обработчиков сообщений
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("time", time))
        application.add_handler(CallbackQueryHandler(button_callback))

        application.add_handler(MessageHandler(filters.TEXT & filters.Regex('Пары сегодня'), show_today))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex('Пары завтра'), show_tomorrow))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex('Расписание на неделю'), show_week))


        # Запуск бота
        application.run_polling()

    except Exception as e:
        print(f"Произошла ошибка при запуске бота: {e}")

if __name__ == '__main__':
    main()


