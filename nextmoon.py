import datetime
import ephem


def get_moon_dates(year, next_fn):
    start_of_year = ephem.Date(datetime.date(year, 1, 1))
    end_of_year = ephem.Date(datetime.date(year + 1, 1, 1))
    # print(f" start_of_year {start_of_year}")
    # print(f" end_of_year {end_of_year}")
    moon_dates_nf = []
    date = start_of_year

    while date < end_of_year:
        date = next_fn(date)
        date_and_time = date.datetime() + datetime.timedelta(hours=3)
        moon_dates_nf.append(date_and_time)
    return moon_dates_nf[:-1]


def getnextupinfo():
    todaynow = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
    print(f"today = {todaynow}")

    #a_date = ephem.now()
    # print(a_date)

    year = todaynow.year
    # print(year)

    new_moon_dates = get_moon_dates(year, ephem.next_new_moon)
    full_moon_dates = get_moon_dates(year, ephem.next_full_moon)
    fq_moon_dates = get_moon_dates(year, ephem.next_first_quarter_moon)
    lq_moon_dates = get_moon_dates(year, ephem.next_last_quarter_moon)

    # full_moon_dn = min([d for d in full_moon_dates if d.date() >= todaynow.date()], key=lambda s: s - todaynow)
    # new_moon_dn = min([d for d in new_moon_dates if d.date() >= todaynow.date()], key=lambda s: s - todaynow)
    # fq_moon_dn = min([d for d in fq_moon_dates if d.date() >= todaynow.date()], key=lambda s: s - todaynow)
    # lq_moon_dn = min([d for d in lq_moon_dates if d.date() >= todaynow.date()], key=lambda s: s - todaynow)

    try:
        fq_moon_dn = min([d for d in fq_moon_dates if d.date() >= todaynow.date()], key=lambda s: s - todaynow)
    except:
        fq_moon_dn = ephem.next_first_quarter_moon(todaynow).datetime() + datetime.timedelta(hours=3)

    try:
        full_moon_dn = min([d for d in full_moon_dates if d.date() >= todaynow.date()], key=lambda s: s - todaynow)
    except:
        full_moon_dn = ephem.next_full_moon(todaynow).datetime() + datetime.timedelta(hours=3)

    try:
        new_moon_dn = min([d for d in new_moon_dates if d.date() >= todaynow.date()], key=lambda s: s - todaynow)
    except:
        new_moon_dn = ephem.next_new_moon(todaynow).datetime() + datetime.timedelta(hours=3)

    try:
        lq_moon_dn = min([d for d in lq_moon_dates if d.date() >= todaynow.date()], key=lambda s: s - todaynow)
    except:
        lq_moon_dn = ephem.next_last_quarter_moon(todaynow).datetime() + datetime.timedelta(hours=3)

    moondict = {'Полнолуние \U0001F315': full_moon_dn, 'Новолуние \U0001F311': new_moon_dn, 'Первая четверть \U0001F313': fq_moon_dn,
                'Последняя четверть \U0001F317': lq_moon_dn}
    moondictsorted = {k: v for k, v in sorted(moondict.items(), key=lambda item: item[1])}

    # print(moondict)
    print(moondictsorted)

    # print(moondictsorted.keys())
    # print(moondictsorted.values())
    keys = []
    values = []
    for k, v in moondictsorted.items():
        keys.append(k)
        values.append(v)
    ind = 0
    key = keys[ind]
    value = values[ind]
    return key, value

def getFoolMoonDates():
    todaynow = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
    print(f"today = {todaynow}")
    year = todaynow.year
    full_moon_dates = get_moon_dates(year, ephem.next_full_moon)
    return full_moon_dates

def is_holiday(todaynow, lunardate):
    f, s, t = get_three_dates(todaynow)
    # print(f)
    # print(s)
    # print(t)
    # print(todaynow)
    if f == lunardate or s == lunardate or t == lunardate:
        return True
    else:
        return False


def get_three_dates(date):
    firstDate = date - datetime.timedelta(days=1)
    secondDate = date  # - datetime.timedelta(days=0)
    thirdDate = date + datetime.timedelta(days=1)

    return firstDate.date(), secondDate.date(), thirdDate.date()
# moontype, date = getnextupinfo()
# print(moontype, date.strftime('%Y-%m-%d or %d %b %H:%M %A'))

cald = {'Monday': 'в понедельник', 'Tuesday': 'во вторник', 'Wednesday': 'в среду', 'Thursday': 'в четверг', 'Friday': 'в пятницу',
        'Saturday': 'в субботу', 'Sunday': 'в воскресенье'}

moontype, date = getnextupinfo()
todaynow = datetime.datetime.utcnow() + datetime.timedelta(hours=3)#+ datetime.timedelta(days=6)
d = date.date() -todaynow.date()
daysdelta = d.days
print(d)
dd = {0:'сегодня!', 1:'завтра!', 2: 'послезавтра', 3: 'через 2 дня', 4: 'через 3 дня', 5: 'через 4 дня', 6: 'через 5 дней',
      7: 'через 6 дней', 8: 'через 7 дней', 9: 'через 8 дней', 10: 'через 9 дней',11: 'через 10 дней', 12: 'через 11 дней'}
print(dd[daysdelta])
# Ночное время - с 22 до 6 часов

# todaynow = datetime.datetime.utcnow() + datetime.timedelta(hours=3)

# print(date)
# newdate = date - datetime.timedelta(days=1)
# print(newdate)
# print(newdate.date())
#
# wk = cald[date.strftime('%A')]
# print(type(wk))
# print(f"Завтра в {wk.lower()} упосатха")
