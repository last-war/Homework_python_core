import datetime
from random import randint, choice


def get_days_in_month(month: int, year: int) -> int:
    """for calculate numbers days in month

    Args:
        month (int): current number of months
        year (int): current year

    Returns:
        int: numbers days in month
    """
    next_year = year
    next_month = month+1
    if next_month == 13:
        next_month = 1
        next_year += 1

    return (datetime.date(next_year, next_month, 1) - datetime.date(year, month, 1)).days


def generate_list(list_range: int) -> list:
    """based on a file of names, generates a list with random dates of birth

    Args:
        list_range (int): required list size

    Returns:
        list: list of dictionaries with keys name and date
    """
    users = []
    name_list = []
    with open("english_top_names.txt", 'r', encoding='utf8') as db_names:
        for line in db_names:
            name_list.append(line.split(' ')[0])
    for _ in range(1, list_range):
        r_month = randint(1, 12)
        r_year = randint(1980, 2000)
        users.append({'name': choice(name_list), 'date': datetime.date(
            r_year, r_month, randint(1, get_days_in_month(r_month, r_year)))})

    return users


def get_birthdays_per_week(users: list) -> None:
    """Prints a list of users to be congratulated by day

    Args:
        users (list): list of dictionaries with keys name and date

    Returns:
        None
    """
    if not len(users):
        return ''
    tmp_dict_user = dict()
    for itr in range(1, 8):
        curdate = datetime.date(
            datetime.date.today().year, datetime.date.today().month, datetime.date.today().day+itr)
        if curdate.isoweekday() == 6 or curdate.isoweekday() == 7 or curdate.isoweekday() == 1:
            if not 'Monday' in tmp_dict_user.keys():
                tmp_dict_user.update({'Monday': []})
        else:
            tmp_dict_user.update({curdate.strftime("%A"): []})
        for cur_user in users:
            try:
                birth_this_year = datetime.date(
                    curdate.year, cur_user['date'].month, cur_user['date'].day)
            except ValueError:
                # якщо цього року не має 29/02
                birth_this_year = datetime.date(
                    curdate.year, cur_user['date'].month+1, 1)

            if birth_this_year == curdate:
                if curdate.isoweekday() == 6 or curdate.isoweekday() == 7 or curdate.isoweekday() == 1:
                    tmp_dict_user['Monday'].append(cur_user['name'])
                else:
                    tmp_dict_user[curdate.strftime(
                        "%A")].append(cur_user['name'])
    for key_day in tmp_dict_user.keys():
        if len(tmp_dict_user[key_day]):
            print(key_day+": "+', '.join(tmp_dict_user[key_day]))


get_birthdays_per_week(generate_list(500))
