# -*- coding: utf8 -*-
import datetime
from lunarcalendar import Lunar
import ephem
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

monthdict = {'01': 'января',
             '02': 'февраля',
             '03': 'марта',
             '04': 'апреля',
             '05': 'мая',
             '06': 'июня',
             '07': 'июля',
             '08': 'августа',
             '09': 'сентября',
             '10': 'октября',
             '11': 'ноября',
             '12': 'декабря', }


def is_holiday(todaynow, lunardate):
    f, s, t = get_three_dates(todaynow)
    print(f)
    print(s)
    print(t)
    print(todaynow)
    if f == lunardate or s == lunardate or t == lunardate:
        return True
    else:
        return False


def get_three_dates(date):
    firstDate = date - datetime.timedelta(days=1)
    secondDate = date  # - datetime.timedelta(days=0)
    thirdDate = date + datetime.timedelta(days=1)

    return firstDate.date(), secondDate.date(), thirdDate.date()


def img_sendann_tosubscr(messagetext, imgdest, mes2):
    db_keys = r.keys(pattern="*")
    for id in db_keys:
        try:
            with open(imgdest, 'rb') as bphoto:
                bot.send_photo(id, bphoto, messagetext)
            bot.send_message(id, mes2)
        except:
            pass
        time.sleep(0.05)


def job_annvesak():
    moontype, date = nextmoon.getnextupinfo()

    todaynow = datetime.datetime.utcnow() + datetime.timedelta(hours=3) #- datetime.timedelta(days=1)
    #nextday = todaynow + datetime.timedelta(days=1)
    myYear = todaynow.year
    vesakday = Lunar(myYear, 4, 15).to_date()
    mpujaday = Lunar(myYear, 1, 15).to_date()
    apujaday = Lunar(myYear, 6, 15).to_date()


    newdate = date
    if (todaynow.date() == newdate.date() and is_holiday(todaynow, vesakday)):
        # sendann_tosubscr(mes)

        print("Весак")
        imgdest = "imgs/vesak.jpg"
        mes = "Друзья, поздравляю вас с Весаком, Днём Будды! 🙏"
        mes2 = f"В этот раз мы отмечаем его {todaynow.day} {monthdict[todaynow.strftime('%m')]}\n\n" \
        "Именно в день Весак два с половиной тысячелетия тому назад в 623 году до нашей эры родился Будда. Также в этот же день Будда достиг просветления и в этот же день Будда покинул этот мир на 80-м году жизни." \
               "\nВ этот день во всех буддийских монастырях проводятся торжественные молебны, местные буддийские храмы украшаются гирляндами из цветов, а с наступлением темноты зажигаются разноцветные фонарики, что символизирует просветление, приходящее в этот мир. Фонарики для Весака делаются из бумаги на лёгком деревянном каркасе. На территории храмов вокруг деревьев Бодхи и ступ принято расставлять масляные лампы. " \
               "Люди в разных странах посылают своим близким и друзьям поздравительные открытки, на которых, как правило, изображаются памятные события из жизни Будды. " \
               "Миряне также посещают местные храмы и монастыри, слушают даршаны (букв. «виденье», «встреча», элемент пуджи) и медитируют в течение всей ночи." \
               "В дни праздника также поощряется дана (пожертвования) как свидетельство милосердия. Миряне, как правило, приносят в монастырь или храм обильное угощение (пищу) в подтверждение того, что они не забывают о своём долге перед монастырской общиной (сангхой). Подношения подчёркивают, что сангха важна для мирян. " \
               "В этот день многие вспоминают первые проповеди Будды, такие как: \n 4 благородные истины \n(https://suttacentral.net/sn56.11/ru/sv), \n докртина «не-я» \n(https://suttacentral.net/sn22.59/ru/sv),\n 4 сводки Дхаммы \n(https://suttacentral.net/mn82/ru/sv) \n... и многие другие Наставления "

        img_sendann_tosubscr(mes, imgdest, mes2)

    if (todaynow.date() == newdate.date() and is_holiday(todaynow, mpujaday)):
        # sendann_tosubscr(mes)
        print("Magha Puja")
        mes = "Друзья, поздравляю вас с Макха Пуджей, Днём Сангхи!"
        mes2 = f"В этот раз мы отмечаем его {todaynow.day} {monthdict[todaynow.strftime('%m')]}\n\n" \
               f"Макха Пуджа - один из знаменательных буддийских праздников. Он приходится на день полнолуния третьего лунного месяца (приблизительно последняя неделя февраля, начало марта). Этот день связан с четырьмя важными событиями, которые произошли в жизни Будды, а именно: \n " \
               f"\n1250 буддийских монахов спонтанно собрались из различных мест, чтобы почтить Будду в Бамбуковой Роще в Раджгахе, Северная Индия, где тогда он остановился.\n" \
               f"\nВсе они были Архатами и были посвящены в монахи лично Буддой . Они собрались вместе в день полной луны на третий лунный месяц. Вечером того же дня Будда прочитал им проповедь \"Овада патимока\", во время которой выдвинул основные принципы своего учения и, в итоге, пришел к трем истинам: делай добро, воздерживайся от зла и очищай свой разум.\n" \
               f"\nЦеремония празднования в буддийских монастырях:\n" \
               f"\nЦеремония песнопения, медитация, размышления о Дхамме\n" \
               f"\nКульминация праздника – свечная процессия – приходится на вечерне-ночное время, обычно после 8 часов. Все собираются возле храма, обязательно украшенного по этому случаю и обходят вокруг храма три раза по часовой стрелке, неся в руках свечи, благовонные палочки и цветы лотоса. " \
               f"\nКаждое из трех шествий имеет определенный смысл: первое совершается в честь самого Будды, второе – в честь всего буддийского сообщества, Сангхи, а третье – в честь его учения Дхаммы."
        imgdest = "imgs/magha.jpg"
        img_sendann_tosubscr(mes, imgdest, mes2)

    if (todaynow.date() == newdate.date() and is_holiday(todaynow, apujaday)):
        # sendann_tosubscr(mes)
        print("Asalha Puja")
        mes = "Друзья, поздравляю вас с Асалха Пуджей, Днём Дхаммы!"
        mes2 = f"В этот раз мы отмечаем его {todaynow.day} {monthdict[todaynow.strftime('%m')]}\n\n" \
        "Будда говорил о трех чудесах: чудо сверхъестественных сил, чудо чтения мыслей и чудо способности обучать. Будда сказал, что он видел опасность в первых двух, и только последнее считал благородным и возвышенным. Способность разъяснить путь к окончательному освобождению - единственное настоящее чудо. " \
               "\nСегодня мы отмечаем Асалха Пуджу, день, когда Будда запустил колесо Дхаммы, провозгласив 4 Благородные Истины. Именно тогда Будда впервые продемонстрировав чудо способности обучать. Через два месяца после своего просветления он прибыл в Олений Парк в Сарнатхе, недалеко от Бенареса (современного Варанаси), чтобы разъяснить учение своим пяти бывшим друзям по аскезе. Сначала эти аскеты были враждебны к Будде и не доверяли ему, потому что они думали, что он потерпел поражение в практике. Их мысли были привязаны к ошибочным представлениям о духовном развитии. Но уже через несколько минут Будда смог смягчить их враждебность и преобразовать ее в веру и вдохновение. Он смог перевернуть их представления. Учение о Серединном Пути было дано с такой силой и красноречием, что они с готовностью приняли его. К концу беседы, Конданна - старейший из членов этой группы, достиг первого уровня просветления, став сотапанной, \"вошедшим в поток\", а остальные четыре стали на Путь.  https://suttacentral.net/sn56.11/ru/sv"
        imgdest = "imgs/asalha.jpg"
        img_sendann_tosubscr(mes, imgdest, mes2)


# myYear = 2021
# print(f"Vesak {myYear} = {Lunar(myYear, 4, 15).to_date()}")  # Vesak и полнолуние
# print(f"Magha Puja {myYear} = {Lunar(myYear, 1, 15).to_date()}")  # Vesak и полнолуние
# print(f"Asalha Puja {myYear} = {Lunar(myYear, 6, 15).to_date()}")  # Vesak и полнолуние

# todaynow = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
# print(type(Lunar(myYear, 4, 15).to_date()))
# print(type(todaynow.date()))
#
# print(todaynow.date())
# print(todaynow.year)
#
# print("---------")

print("Vesak Announcer")

schedule.every().day.at("07:05").do(job_annvesak)


while True:
    schedule.run_pending()
    time.sleep(30)
