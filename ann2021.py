import schedule
import datetime
import time
import nextmoon
import telebot
import redis


token = 'token'


bot = telebot.TeleBot(token)

redis_host = "xxx.xx.xx.xx"
redis_port = 6379
redis_password = "password"


r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

print("Буду делать рассылку всем в телеграм в 10:00 за день и в 07:00 в этот день")


def sendann_tosubscr(messagetext):
    db_keys = r.keys(pattern="*")
    for id in db_keys:
        try:
            bot.send_message(id, messagetext)
        except:
            pass
        time.sleep(0.05)
        #time.sleep(1) раскоментировать, если телега будет жаловаться на превышение лимита сообщений

def sendimageann_tosubscr(messagetext, moontype):
    db_keys = r.keys(pattern="*")
    for id in db_keys:
        try:
            #bot.send_message(id, messagetext)
            if moontype == 'Новолуние \U0001F311':
                with open("imgs/newmoonrus.png", 'rb') as bphoto:
                    bot.send_photo(id, bphoto, messagetext)
            if moontype == 'Полнолуние \U0001F315':
                with open("imgs/fullmoonrus.png", 'rb') as bphoto:
                    bot.send_photo(id, bphoto, messagetext)
            if moontype == 'Последняя четверть \U0001F317':
                with open("imgs/tqrus.png", 'rb') as bphoto:
                    bot.send_photo(id, bphoto, messagetext)
            if moontype == 'Первая четверть \U0001F313':
                with open("imgs/fqrus.png", 'rb') as bphoto:
                    bot.send_photo(id, bphoto, messagetext)


        except:
            pass
        time.sleep(0.05)

def job():
    moontype, date = nextmoon.getnextupinfo()
    #wk = nextmoon.cald[date.strftime('%A')]
    todaynow = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
    # if (todaynow.date()==date.date()):
    #     sendann_tosubscr("Сегодня упосатха")
    newdate = date - datetime.timedelta(days=1)
    if (todaynow.date()==newdate.date()):
        wk = nextmoon.cald[date.strftime('%A')]
        mes = f"Напоминаю о том, что завтра в {wk.lower()} начинается упосатха. \n" \
              f"Луна взойдёт в фазе **{moontype.lower()}** {date.strftime('%d.%m')} в {date.strftime('%H:%M')} (по МСК)"
        sendann_tosubscr(mes)
        print(mes)

def job2():
    moontype, date = nextmoon.getnextupinfo()
    todaynow = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
    newdate = date# - datetime.timedelta(days=0)
    if (todaynow.date()==newdate.date()):
        mes = f"Сегодня упосатха. Старайтесь соблюдать все принятые обеты 🙏\n"
        sendimageann_tosubscr(mes, moontype)
        # sendann_tosubscr(mes)
        # print(mes)

# def job3():
#     moontype, date = nextmoon.getnextupinfo()
#     #wk = nextmoon.cald[date.strftime('%A')]
#     todaynow = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
#     # if (todaynow.date()==date.date()):
#     #     sendann_tosubscr("Сегодня упосатха")
#     newdate = date# - datetime.timedelta(days=0)
#     if (todaynow.date()==newdate.date()):
#         #wk = nextmoon.cald[date.strftime('%A')]
#         #mes = f"Сегодня упосатха. Старайтесь соблюдать все принятые обеты 🙏\n"
#         mes = "тестирование связи 🙏"
#         bot.send_message(71168284, mes)
#         print(mes)

# def job4():
#
#     bot.send_message(71168284, mes)

schedule.every().day.at("10:00").do(job)
schedule.every().day.at("07:00").do(job2)
#schedule.every().day.at("19:27").do(job3)
# schedule.every(30).minutes.do(job4)

while True:
    schedule.run_pending()
    time.sleep(30)