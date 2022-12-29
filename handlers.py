import telebot
import utils

TOKEN = ''
bot = telebot.TeleBot(TOKEN)

lang = 'ru'


@bot.message_handler(commands=['help', 'start'])
def start(message):
    global lang
    if lang == 'ru':
        bot.send_message(message.chat.id, "/help\n\n"
                                          "/convert <token> <amount> - конвертирует выбранную вами валюту в TON\n\n"
                                          "/price <token> - показывает курс тона к выбранной вами валюте\n\n"
                                          "/language - выбор языка бота (ENG, RU)")
    else:
        bot.send_message(message.chat.id, "/help\n\n"
                                          "/convert <token> <amount> - converts the currency of your choice to TON\n\n"
                                          "/price <token> - показывает курс тона к выбранной вами валюте\n\n"
                                          "/language - выбор языка бота (ENG, RU)")


@bot.message_handler(regexp="/price")
def request_forecast(message):
    global lang
    mes = message.text.upper()
    if mes == '/PRICE' and lang == 'ru':
        bot.send_message(message.chat.id, "Введенно недостаточно данных, попробуйте /price usdt")
    elif mes == '/PRICE' and lang == 'eng':
        bot.send_message(message.chat.id, "Not enough data entered, try /price usdt")
    else:
        mes = mes.replace('/PRICE ', '')
        get_ton_rate(message, mes)


def get_ton_rate(message, cur):
    if 1 < len(cur) < 5:
        ans = utils.get_ton(cur)
        if ans is not None:
            bot.send_message(message.chat.id, ans + " " + cur)
        else:
            translate_error_message(message)
    else:
        translate_error_message(message)


@bot.message_handler(regexp="/convert")
def request_forecast(message):
    global lang
    mes = message.text.upper()
    if mes == '/CONVERT' and lang == 'ru':
        bot.send_message(message.chat.id, "Введенно недостаточно данных, попробуйте /convert usdt 1000")
    elif mes == '/CONVERT' and lang == 'eng':
        bot.send_message(message.chat.id, "Not enough data entered, try /convert usdt 1000")
    else:
        mes = mes.replace('/CONVERT', '')
        converter(mes.split(), message)


@bot.message_handler(regexp="/language")
def request_forecast(message):
    global lang
    mes = message.text.upper()
    if mes == '/LANGUAGE RU':
        lang = 'ru'
    elif mes == '/LANGUAGE ENG':
        lang = 'eng'
    else:
        bot.send_message(message.chat.id, "RU/ENG")


def converter(req, message):
    if len(req) > 1:
        currency = req[0].upper()
        count = float(req[1])
        if 1 < len(currency) < 5:
            ans = utils.get_ton(currency)
            if ans is not None:
                res = utils.convert(count, float(ans))
                bot.send_message(message.chat.id, str(res) + ' TON')
            else:
                translate_error_message(message)
        else:
            translate_error_message(message)
    else:
        translate_error_message(message)


def translate_error_message(message):
    global lang
    if lang == 'ru':
        return bot.send_message(message.chat.id, "Неправильно введена валюта")
    else:
        return bot.send_message(message.chat.id, "Currency entered incorrectly")


bot.polling(none_stop=True)
