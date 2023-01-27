#Ваше завдання написати функцію get_birthdays_per_week, 
# яка отримує на вхід список users і виводить у консоль(за допомогою print)
# список користувачів, яких потрібно привітати по днях.
# Користувачів, у яких день народження був на вихідних, потрібно привітати у понеділок.
# Для відладки зручно створити тестовий список users та заповнити його самостійно.
# Функція виводить користувачів з днями народження на тиждень вперед від поточного дня.
# Тиждень починається з понеділка.


from datetime import datetime, timedelta
from calendar import monthrange



def get_birthdays_per_week(users):
    
    month_list = []
    week_list = []
    delta = timedelta(days=7)
    current_date = datetime.now()
    next_day = current_date + delta
    days = monthrange(current_date.year, current_date.month)


    for user in users:
        if user['birthday'].month == current_date.month or user['birthday'].month <= next_day.month:
            month_list.append(user)

    for user in month_list:
        br_day = user['birthday'].day  # 27
        cur_day = current_date.day  # 26
        n_day = next_day.day            # 2,31
        if user['birthday'].month == current_date.month:
            if br_day > cur_day:
                week_list.append(user)
        elif user['birthday'].month > current_date.month:
            # n_day += month_day
            if br_day <= n_day:
                week_list.append(user)


    # 0 - Monday 1 - Tuesday 2 - Wednesday 3 - Thursday 4 - Friday 5 - Saturday 6 - Sunday

    for el in week_list:             # додати день тижня для поздоровлення
        week_day = datetime(current_date.year,
                            el['birthday'].month, el['birthday'].day)
        if week_day.weekday() == 5 or week_day.weekday() == 6:
            cong_day = 'Monday'
            el['week_day'] = cong_day
        else:
            el['week_day'] = week_day.strftime('%A')
        

    br_dict = {}

    for el in week_list:
        el_list = el['week_day']
        if el_list not in br_dict:
            br_dict[el_list] = []
        br_dict[el_list].append(el['name'])

    for key, val in br_dict.items():
        val_str = ''
        val_str = ', '.join(val)
        print(key, ':', val_str)


users = [{'name': 'Oleh', 'birthday': datetime(1964, 12, 15)},
         {'name': 'Mariya', 'birthday': datetime(year=1942, month=12, day=15)},
         {'name': 'Oksana', 'birthday': datetime(year=1965, month=9, day=13)},
         {'name': 'Yulia', 'birthday': datetime(year=1988, month=1, day=31)},
         {'name': 'Max', 'birthday': datetime(year=1999, month=1, day=20)},
         {'name': 'Andry', 'birthday': datetime(year=1999, month=1, day=27)},
         {'name': 'Den', 'birthday': datetime(year=1980, month=1, day=28)},
         {'name': 'Mick', 'birthday': datetime(year=1927, month=2, day=2)},
         {'name': 'Nick', 'birthday': datetime(year=2020, month=2, day=2)},
         ]

get_birthdays_per_week(users)
