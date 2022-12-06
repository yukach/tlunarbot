""" Что делает бот
Кидает пользователю уведомление, что сегодня день упосатхи, если сегодня день упосатхи
Если сегодня определённый праздник весак и т.д. - пишет это тоже в уведомлении и использует соответствующую картинку
Сообщает ближайшие дни упосатхи на месяц по требованию пользоватлея "Когда упосатха?"
По запросу "Когда [буддийский праздник]" Сообщает дату [буддийского праздника] в этом году
По запросу "Когда [буддийский праздник] в [году]" Сообщает дату [буддийского праздника] в [году]

"""

# -*- coding: utf-8 -*-
import datetime
from lunarcalendar import Lunar

import telebot
import cherrypy
import nextmoon
import redis
from telebot import types
from texts import *

token = 'your token'
WEBHOOK_HOST = 'xxx.xx.xxx.xx'
WEBHOOK_PORT = 8443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = 'xxx.xx.xxx.xx'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = 'webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = 'webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (token)

bot = telebot.TeleBot(token)

redis_host = "xxx.xx.xxx.xx"
redis_port = 6379
redis_password = "redis_password"



r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)



dd = {0:'сегодня', 1:'завтра', 2: 'послезавтра', 3: 'через 2 дня', 4: 'через 3 дня', 5: 'через 4 дня', 6: 'через 5 дней',
      7: 'через 6 дней', 8: 'через 7 дней', 9: 'через 8 дней', 10: 'через 9 дней',11: 'через 10 дней', 12: 'через 11 дней'}

daydict = {'01':'1',
           '02':'2',
           '03':'3',
           '04':'4',
           '05':'5',
           '06':'6',
           '07':'7',
           '08':'8',
           '09':'9',
           '10': '10',
           '11': '11',
           '12': '12',
           '13': '13',
           '14': '14',
           '15': '15',
           '16': '16',
           '17': '17',
           '18': '18',
           '19': '19',
           '20': '20',
           '21': '21',
           '22': '22',
           '23': '23',
           '24': '24',
           '25': '25',
           '26': '26',
           '27': '27',
           '28': '28',
           '29': '29',
           '30': '30',
           '31': '31',
           }
monthdict = {'01':'января',
           '02':'февраля',
           '03':'марта',
           '04':'апреля',
           '05':'мая',
           '06':'июня',
           '07':'июля',
           '08':'августа',
           '09':'сентября',
           '10': 'октября',
           '11': 'ноября',
           '12': 'декабря',}

donatekeyboard = types.InlineKeyboardMarkup()
url_yand = types.InlineKeyboardButton(text="Перейти в яндекс-кошелёк", url="https://money.yandex.ru/to/410015684186126")
donatekeyboard.add(url_yand)

maratanhaboard = types.InlineKeyboardMarkup()
url_gruboe = types.InlineKeyboardButton(text="Грубое и утончённое", url="https://telegra.ph/Gruboe-i-utonchennoe-08-07")
url_theravada = types.InlineKeyboardButton(text="Почему я тхеравадин, а не махаянист", url="https://telegra.ph/Pochemu-ya-theravadin-a-ne-mahayanist-12-05")
url_sbtel = types.InlineKeyboardButton(text="История Будды Шакьямуни", url="https://telegra.ph/Istoriya-Buddy-08-02")
url_maratanha = types.InlineKeyboardButton(text="Конец вечно длящегося рабства", url="https://telegra.ph/Vechnoe-rabstvo-Prichiny-i-sposoby-preodoleniya-08-03")
url_aviakata = types.InlineKeyboardButton(text="Безответные вопросы", url="https://ru.wikipedia.org/wiki/%D0%91%D0%B5%D0%B7%D0%BE%D1%82%D0%B2%D0%B5%D1%82%D0%BD%D1%8B%D0%B5_%D0%B2%D0%BE%D0%BF%D1%80%D0%BE%D1%81%D1%8B")
#url_aviakata = types.InlineKeyboardButton(text="Безответные вопросы", url="https://telegra.ph/Bezotvetnye-voprosy-09-13")
url_anapanasati = types.InlineKeyboardButton(text="Медитация анапанасати поэтапно", url="http://theravada.ru/Teaching/Works/meditaciya_anapanasati-sv.htm")
url_anatta = types.InlineKeyboardButton(text="Анатта", url="https://telegra.ph/Anatta-09-13")
url_notfairytail = types.InlineKeyboardButton(text="Козни Девадатты", url="https://telegra.ph/Test-08-21-150")
maratanhaboard.add(url_sbtel)
maratanhaboard.add(url_gruboe)
maratanhaboard.add(url_theravada)
maratanhaboard.add(url_maratanha)
maratanhaboard.add(url_aviakata)
maratanhaboard.add(url_anapanasati)
maratanhaboard.add(url_anatta)
maratanhaboard.add(url_notfairytail)

upboard = types.InlineKeyboardMarkup()
url_uposatha = types.InlineKeyboardButton(text="Подробнее об упосатхе", url="https://dhamma.ru/lib/authors/khantipalo/uposatha.htm")
upboard.add(url_uposatha)

# rkeyboard = types.InlineKeyboardMarkup()
# rbutton = types.InlineKeyboardButton(text="Обновить", callback_data="refresh")
# rkeyboard.add(rbutton)

switch_keyboard = types.InlineKeyboardMarkup()
switch_button = types.InlineKeyboardButton(text="Поделиться", switch_inline_query="moon")
switch_keyboard.add(switch_button)






# Наш вебхук-сервер
class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения

            bot.process_new_updates([update])

            return ''
        else:
            raise cherrypy.HTTPError(403)



def wrtodb(data):
    user_id = data.from_user.id
    user_name = data.from_user.username
    #bot.reply_to(message, f"{user_id} , {user_name}")
    #r.set(user_name, user_id) wrong
    try:
        r.set(user_id, user_name)
    except:
        r.set(user_id, '')

def dfromdb(data):
    user_id = data.from_user.id
    user_name = data.from_user.username
    #bot.reply_to(message, f"{user_id} , {user_name}")
    #r.delete(user_name, user_id) wrong         1374035767
    r.delete(user_id)


def getNextUposatha_text(msg):
    moontype, date = nextmoon.getnextupinfo()
    wk = nextmoon.cald[date.strftime('%A')]
    dayd = date.strftime('%d')
    monthm = date.strftime('%m')
    user_id = msg.from_user.id
    db_keys = r.keys(pattern="*")
    if str(user_id) in db_keys:
        notstate = 'включено'
    else:
        notstate = 'отключено'
        print(f"\n user_id {user_id}\n")
    #bot.reply_to(msg, f"{db_keys} \n{user_id}")
    todaynow = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
    d = date.date() - todaynow.date()
    daysdelta = d.days

    newtext = f"Сегодня {todaynow.strftime('%d.%m.%Y  %H:%M')}\n" \
              f"Ближайшая упосатха - {dd[daysdelta]}, {wk.lower()} {daydict[dayd]} {monthdict[monthm]}\n" \
              f"Луна в фазе: {moontype}\n" \
              f"Начало фазы: {date.strftime('%d.%m.%Y')} в  {date.strftime('%H:%M')} (по МСК)\n"\
              f"Оповещение за день до начала: {notstate}\n"
    return newtext


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def start(message):
    wrtodb(message)
    # bot.reply_to(message,
    #              ("Привет. \nЯ предсказываю дату ближайшей упосатхи \n"
    #               "Набери слово \"упосатха\" или команду /moon\n"
    #               "Оповещение за день до начала упосатхи включено\n"
    #               "Его можно отключить с помощью команды /off из списка команд "))
    bot.send_message(message.chat.id,
                 ("Привет. \nЯ предсказываю дату ближайшей упосатхи \n"
                  "Набери слово \"упосатха\" или команду /moon\n"
                  "Оповещение за день до начала упосатхи включено\n"
                  "Его можно отключить с помощью команды /off из списка команд\n"
                  "Нажми на /help, чтобы увидеть весь список моих команд"))
    bot.send_message(71168284, f"{message.chat.id}")

# Handle '/on'
@bot.message_handler(commands=['on'])
def on(message):
    wrtodb(message)
    # bot.reply_to(message, "Включено специальное оповещение о начале упосатхи.\n"
    #                       "(Чтобы его отключить - набери команду /off)\n")
    bot.send_message(message.chat.id, "Включено специальное оповещение о начале упосатхи.\n"
                          "Чтобы его отключить - набери команду /off\n")
                          #"/moon                 /help  \n")

# Handle '/off'
@bot.message_handler(commands=['off'])
def off(message):
    dfromdb(message)
    # bot.reply_to(message, "Отключено специальное оповещение о начале упосатхи.\n"
    #                       "(Чтобы снова его включить - набери команду /on)\n")
    bot.send_message(message.chat.id, "Отключено специальное оповещение о начале упосатхи.\n"
                          "Чтобы снова его включить - набери команду /on\n")



# @bot.message_handler(commands=['ma'])
# def sa(message):
#     bot.send_message('71168284', 'Сегодня упосатха!!!!')
    #send_announcments('Сегодня упосатха!!!!')
    #porytyan: 804527232



# @bot.callback_query_handler(func=lambda call: True)
# def callback_inline(call):
#     newtext = getNextUposatha_text(call.message)
#
#     cmt1 = call.message.text.split('\n')[0]
#     n1 = newtext.split('\n')[0]
#
#     if call.data == "refresh" and not (cmt1 == n1):
#         strarr = newtext.split('\n')[0:-2]
#         strarr.append(call.message.text.split('\n')[-1])
#         ntt = "\n".join(strarr)
#         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=ntt,
#                               reply_markup=rkeyboard)
#
#         # try:
#         #     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=newtext, reply_markup=rkeyboard)
#         # except:
#         #     # print(f"call.message.text {call.message.text}")
#         #     # print(f"newtext {newtext}")
#         #     #
#         #     # print("  ")
#         #     print(cmt1)
#         #     print(n1)


@bot.message_handler(commands=['nu', 'moon'])
def moon(message):
    newtext = getNextUposatha_text(message)
    #bot.reply_to(message, newtext)
    #bot.send_message(message.chat.id, newtext)
    #bot.send_message(message.chat.id, ":smile:", reply_markup=rkeyboard)
    bot.send_message(message.chat.id, newtext, reply_markup=switch_keyboard)

@bot.message_handler(commands=['holidays'])
def holidays(message):
    fmd = nextmoon.getFoolMoonDates()

    todaynow = datetime.datetime.utcnow() + datetime.timedelta(hours=3)  # - datetime.timedelta(days=1)
    myYear = todaynow.year
    vesakday = Lunar(myYear, 4, 15).to_date()
    mpujaday = Lunar(myYear, 1, 15).to_date()
    apujaday = Lunar(myYear, 6, 15).to_date()

    vesakdaytxt = ""
    mpujadaytxt = ""
    apujadaytxt = ""

    for date in fmd:
        if nextmoon.is_holiday(date, vesakday):
            vesakdaytxt = date
        if nextmoon.is_holiday(date, mpujaday):
            mpujadaytxt = date
        if nextmoon.is_holiday(date, apujaday):
            apujadaytxt = date

    htext = f"""
    Буддийские праздники в {myYear} году:
    Макха Пуджа: {mpujadaytxt.strftime('%d.%m.%Y')}
    Весак: {vesakdaytxt.strftime('%d.%m.%Y')}
    Асалха Пуджа: {apujadaytxt.strftime('%d.%m.%Y')}
    """

    print(htext)
    bot.send_message(message.chat.id, htext)


# @bot.message_handler(commands=['test'])
# def test(message):
#     newtext = getNextUposatha_text(message)
#     #bot.reply_to(message, newtext)
#     rain = u'\U00002614'  # Code: 500's
#     foolmoon = u'\U0001F315'  # Code: 500's
#     lq = u'\U0001F317'
#     newmoon = 	'\U0001F311'
#     fq = '\U0001F313'
#
#     bot.send_message(message.chat.id, lq)
#     bot.send_message(message.chat.id, newtext, reply_markup=rkeyboard)

@bot.message_handler(commands=['about'])
def about(message):
    #bot.reply_to(message, obettext)
    bot.send_message(message.chat.id, obettext, reply_markup=upboard)

@bot.message_handler(commands=['buddha'])
def about(message):
    #bot.reply_to(message, obettext)
    bot.send_message(message.chat.id, "История Будды Шакьямуни и другие полезные статьи по ссылкам", reply_markup=maratanhaboard)

@bot.message_handler(commands=['donate'])
def donate(message):
    #bot.reply_to(message, donatetext)
    bot.send_message(message.chat.id, donatetext, reply_markup=donatekeyboard)





@bot.message_handler(commands=['help'])
def help(message):
    #bot.reply_to(message, helptext)
    bot.send_message(message.chat.id, helptext)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def expression(message):
    lowtext = message.text.lower()
    if 'обет' in lowtext:
        #bot.reply_to(message, f"{type(message.text)}")
        #bot.reply_to(message, obettext)
        bot.send_message(message.chat.id, obettext)
    elif 'упосат' in lowtext:
        newtext = getNextUposatha_text(message)
        #bot.reply_to(message, newtext)
        #bot.send_message(message.chat.id, newtext)
        bot.send_message(message.chat.id, newtext, reply_markup=switch_keyboard)
    elif 'правила' in lowtext:
        #bot.reply_to(message, obettext)
        bot.send_message(message.chat.id, obettext)
    elif 'спасибо' in lowtext:
        #bot.reply_to(message, donatetext)
        #bot.send_message(message.chat.id, donatetext)
        bot.send_message(message.chat.id, donatetext, reply_markup=donatekeyboard)
    elif 'благодарю' in lowtext:
        #bot.reply_to(message, donatetext)
        #bot.send_message(message.chat.id, donatetext)
        bot.send_message(message.chat.id, donatetext, reply_markup=donatekeyboard)
    elif 'весак' in lowtext:
        holidays(message)
    elif 'праздники' in lowtext:
        holidays(message)
    elif 'стат' in lowtext:
        #bot.reply_to(message, donatetext)
        #bot.send_message(message.chat.id, donatetext)
        bot.send_message(message.chat.id, "История Будды Шакьямуни и другие полезные статьи по ссылкам", reply_markup=maratanhaboard)
    else:
        #bot.reply_to(message, helptext)

        bot.send_message(message.chat.id, helptext)


@bot.message_handler(func=lambda message: True, content_types=['audio', 'photo', 'voice', 'video', 'document', 'location', 'contact', 'sticker'])
def expression(message):
    #bot.reply_to(message, helptext)
    bot.send_message(message.chat.id, helptext)


def getNUposatha_forquery():
    moontype, date = nextmoon.getnextupinfo()
    wk = nextmoon.cald[date.strftime('%A')]
    dayd = date.strftime('%d')
    monthm = date.strftime('%m')
    todaynow = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
    d = date.date() - todaynow.date()
    daysdelta = d.days
    newtext = f"Ближайшая упосатха - {dd[daysdelta]}, {wk.lower()} {daydict[dayd]} {monthdict[monthm]}\n" \
              f"Луна в фазе: {moontype}\n" \
              f"Начало фазы: {date.strftime('%d.%m.%Y')} в {date.strftime('%H:%M')} (по МСК)\n"
    return newtext


@bot.inline_handler(func=lambda query: len(query.query) >= 0)
def query_text(query):
    newtext = getNUposatha_forquery()
    mytitle = "Ближайшая упосатха"
    r = types.InlineQueryResultArticle(
        id='1',
        title=mytitle,
        description="Поделиться датой",
        input_message_content=types.InputTextMessageContent(
            message_text=newtext)
    )
    bot.answer_inline_query(query.id, [r])

    #bot.answer_inline_query(query.id, newtext)

#спецуведомление


# Снимаем вебхук перед повторной установкой (избавляет от некоторых проблем)
bot.remove_webhook()

# Ставим заново вебхук
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

# Указываем настройки сервера CherryPy
cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})


cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})







