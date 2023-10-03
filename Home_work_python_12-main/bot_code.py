from user_dict_class import Record, AddressBook

ADRESS_BOOK = AddressBook().read_from_file()


def get_handler(operator: str):
    return OPERATIONS[operator]


def input_error(func) -> str:
    """for error in user input
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return f"wrong name of contact"
        except ValueError as exception:
            return exception.args[0]
        except IndexError:
            return f"wrong index"
        except TypeError:
            return f"wrong data types. enter numeric"
    return inner


def main() -> None:
    """all input-output block
    """

    while True:
        result = parser(input('wait command: ').lower().strip())
        if result == 'exit':
            print('Good bye!')
            break
        else:
            print(result)


def parser(user_in: str) -> str:
    """analiz user input
    Args:
        user_in (str): user input
    Returns:
        str: text for print
    """
    unk_com = True
    for iter in OPERATIONS.keys():
        if user_in.startswith(iter):
            unk_com = False
            return get_handler(iter)(user_in)
    if unk_com:
        return 'I don\'t undestand you'


@input_error
def cmd_add(user_in: str) -> str:
    """add new contact
    """
    result = user_in.split(' ')
    if len(result) < 3:
        return 'you need use \' \' to separate'
    record = Record(result[1])
    record.phone_add(result[2])
    ADRESS_BOOK.record_add(record)
    return 'Added'


@input_error
def cmd_birthday_add(user_in: str) -> str:
    """add birthday to contact
    """
    result = user_in.split(' ')
    if len(result) < 3:
        return 'you need use \' \' to separate'
    record = ADRESS_BOOK.record_find(result[1])
    record.birthday_add(result[2])
    return 'Added birthday'


@input_error
def cmd_birthday_day(user_in: str) -> str:
    """calc day to birthday of contact
    """
    result = user_in.split(' ')
    if len(result) < 2:
        return 'you need use \' \' to separate'
    record = ADRESS_BOOK.record_find(result[1])
    return record.day_to_birthday()


@input_error
def cmd_change(user_in: str) -> str:
    """change phone finded by name
    """
    result = user_in.split(' ')
    if len(result) < 4:
        return 'you need use \' \' to separate'

    record = ADRESS_BOOK.record_find(result[1])
    if record is None:
        return f'can\'t find rec with name {result[1]}'
    record.phone_change(result[2], result[3])

    return 'Changed'


@input_error
def cmd_delete_rec(user_in: str) -> str:
    result = user_in.split(' ')
    if len(result) < 3:
        return 'you need use \' \' to separate'

    record = ADRESS_BOOK.record_find(result[2])
    if record is None:
        return f'can\'t find rec with name {result[2]}'
    ADRESS_BOOK.record_delete(result[2])

    return 'deleted record'


@input_error
def cmd_delete_phone(user_in: str) -> str:
    result = user_in.split(' ')
    if len(result) < 4:
        return 'you need use \' \' to separate'

    record = ADRESS_BOOK.record_find(result[2])
    if record is None:
        return f'can\'t find rec with name {result[2]}'
    record.phone_delete(result[3])

    return 'deleted phone'


def cmd_hello(user_in: str) -> str:
    return 'How can I help you?'


@input_error
def cmd_find(user_in: str) -> str:
    """find contact of phone
    """
    result = user_in.split(' ')
    if len(result) < 2:
        return 'you need use \' \' to separate'
    return ADRESS_BOOK.str_find(result[1])


def cmd_exit(user_in: str) -> str:
    ADRESS_BOOK.save_to_file()
    return 'exit'


def cmd_show(user_in: str) -> str:
    return ADRESS_BOOK.print_AB()


@input_error
def cmd_phone(user_in: str) -> str:
    """find by key
    """
    result = user_in.split(' ')
    if len(result) < 2:
        return 'you need use \' \' to separate'
    record = ADRESS_BOOK.record_find(result[1])
    if record is None:
        return f'can\'t find rec with name {result[1]}'

    return f'{record.name.value} \nphone: {record.show_rec()}'


OPERATIONS = {
    'add': cmd_add,
    'birthday': cmd_birthday_add,
    'change': cmd_change,
    'conglatulation': cmd_birthday_day,
    'close': cmd_exit,
    'delete id': cmd_delete_rec,
    'delete phone': cmd_delete_phone,
    'exit': cmd_exit,
    'find': cmd_find,
    'good bye': cmd_exit,
    'hello': cmd_hello,
    'phone': cmd_phone,
    'show all': cmd_show,
}

if __name__ == '__main__':
    main()
