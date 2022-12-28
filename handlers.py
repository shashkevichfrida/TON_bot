import telebot
from telebot import types
import utils


TOKEN = ' '
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.InlineKeyboardButton("Конвертировать")
    button2 = types.InlineKeyboardButton("Курс тона")
    markup.add(button1, button2)
    bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def request_forecast(message: telebot.types.Message):
    if message.text == "Курс тона":
        msg = bot.send_message(message.chat.id, 'Чтобы узнать курс тона, введите код валюты (например USD)')
        bot.register_next_step_handler(msg, get_ton_rate)

    if message.text == "Конвертировать":
        msg = bot.send_message(message.chat.id, 'Чтобы конвертировать валюту введите код валюты + количество (USD 100)')
        bot.register_next_step_handler(msg, converter)


def get_ton_rate(message: telebot.types.Message):
    currency = message.text.upper()
    if 1 < len(currency) < 5:
        ans = utils.get_ton(currency)
        if ans is not None:
            bot.send_message(message.chat.id, ans + " " + currency)
        else:
            bot.send_message(message.chat.id, "Неправильно введена валюта")
    else:
        bot.send_message(message.chat.id, "Неправильно введена валюта")


def converter(message: telebot.types.Message):
    req = message.text.split()
    if len(req) < 2:
        currency = req[0].upper()
        count = float(req[1])
        if 1 < len(currency) < 5:
            ans = utils.get_ton(currency)
            if ans is not None:
                res = utils.convert(count, float(ans))
                bot.send_message(message.chat.id, res)
            else:
                bot.send_message(message.chat.id, "Неправильно введена валюта")
        else:
            bot.send_message(message.chat.id, "Неправильно введена валюта")
    else:
        bot.send_message(message.chat.id, "Неправильно введены данные")


bot.polling(none_stop=True)
