import telebot
from config import token, api_id, api_hash
from news_pars import news_pars
from tg_pars import tg_pars
from datetime import datetime, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from telethon import TelegramClient, sync
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel

delta = timedelta(days=1)

bot = telebot.TeleBot(token)

print("started")

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Этот бот поможет найти свежие новости по твоим ключевым словам")
    global delta
    delta = timedelta(days=1)


@bot.message_handler(commands=['help'])
def help_message(message):
    inf_message = 'Это бот — агрегатор новостей из различных источников\n\n' \
                  '\help — показать помощь\n' \
                  '\keys <ключевые слова через запятую>  — отправить запрос по ключевым словам\n' \
                  '\set_delta — выбрать за какой отрезок времени искать новости\n\n' \
                  '@dtmity — по любым вопросам работы бота'
    bot.send_message(message.chat.id, inf_message)


@bot.message_handler(commands=['keys'])
def keys_message(message):
    keywords = message.text[6:].split(', ')
    news = news_pars(delta, keywords)
    if len(news) == 0:
        bot.send_message(message.chat.id, 'Ничего не найдено(')
    else:
        for new in news:
            bot.send_message(message.chat.id, new, disable_web_page_preview=True, parse_mode='Markdown')
    bot.send_message(message.chat.id, '------------')
    news = tg_pars(delta, keywords)
    if len(news) == 0 or news == -1:
        bot.send_message(message.chat.id, 'Ничего не найдено(')
    else:
        for new in news:
            bot.send_message(message.chat.id, new, disable_web_page_preview=True, parse_mode='Markdown')


@bot.message_handler(commands=['set_delta'])
def vib_message(message):
    keyboard = InlineKeyboardMarkup(row_width=3)
    btn_a = InlineKeyboardButton('24 часа', callback_data='A')
    btn_b = InlineKeyboardButton('12 часов', callback_data='B')
    btn_c = InlineKeyboardButton('2 часа', callback_data='C')
    keyboard.add(btn_a, btn_b, btn_c)
    bot.send_message(message.chat.id, 'Выберите свежесть новостей:', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda c: True)
def handle_callback_query(call):
    global delta
    str_t = ''
    if call.data == 'A':
        delta = timedelta(days=1)
        str_t = 'сутки'
    elif call.data == 'B':
        delta = timedelta(hours=12)
        str_t = '12 часов'
    elif call.data == 'C':
        delta = timedelta(hours=2)
        str_t = '2 часа'
    hide_keyboard = telebot.types.ReplyKeyboardRemove()
    bot.send_message(call.message.chat.id, 'Установлено: ' + str_t, reply_markup=hide_keyboard)


bot.set_my_commands([
    telebot.types.BotCommand("/start", "Перезапуск бота"),
    telebot.types.BotCommand("/help", "Помощь"),
    telebot.types.BotCommand("/keys", "Произвести запрос"),
    telebot.types.BotCommand("/set_delta", "Выбрать временной диапазон")
])

bot.polling(none_stop=True, interval=0)