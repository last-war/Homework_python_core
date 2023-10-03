ADRESS_BOOK = dict()


def format_phone_number(func) -> str:
    def inner(phone):
        phone = func(phone)
        return ('+' if len(phone) == 12 else '+38')+phone

    return inner


def get_handler(operator: str):
    return OPERATIONS[operator]


def input_error(func) -> str:
    """for error in user input
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return f"{func.__name__} wrong name of contact"
        except ValueError:
            return f"{func.__name__} wrong value"
        except IndexError:
            return f"{func.__name__} wrong index"
        except TypeError:
            return f"{func.__name__} wrong data types. enter numeric"
    return inner


def main() -> None:
    """all input-output block
    """
    while True:
        result = parser(input('wait command: ').lower().strip())
        #0 - command
        #1 - text
        if result[0] == 'break':
            if len(result) > 1:
                print(result[1])
            break
        elif result[0] == 'print':
            for iter in ADRESS_BOOK.keys():
                print(f'{iter}:{ADRESS_BOOK.get(iter)}')

        if len(result) > 1:
            print(result[1])


def param_control(user_in, num_param):
    # don't used
    result = user_in.split(' ')
    if len(result) < num_param:
        return ['', 'you need use \' \' to separate']


def parser(user_in: str) -> list:
    """analiz user input

    Args:
        user_in (str): user input

    Returns:
        list: 0 - command to while 1 - text for print
    """
    unk_com = True
    for iter in OPERATIONS.keys():
        if user_in.startswith(iter):
            unk_com = False
            return get_handler(iter)(user_in)
    if unk_com:
        return ['', 'I don\'t undestand you']


@format_phone_number
def sanitize_phone_number(phone: str) -> str:
    new_phone = (
        phone.strip().removeprefix("+")
        .replace("(", "")
        .replace(")", "")
        .replace("-", "")
        .replace(" ", "")
    )
    return new_phone


@input_error
def todo_add(user_in: str) -> list:
    """add new contact
    """
    result = user_in.split(' ')
    if len(result) < 3:
        return ['', 'you need use \' \' to separate']
    ADRESS_BOOK[result[1]] = sanitize_phone_number(result[2])
    return ['', 'Added']


@input_error
def todo_change(user_in: str) -> list:
    """change phone fined by name
    """
    result = user_in.split(' ')
    if len(result) < 3:
        return ['', 'you need use \' \' to separate']
    ADRESS_BOOK[result[1]] = sanitize_phone_number(result[2])
    return ['', 'Changed']


def todo_hello(user_in: str) -> list:
    return ['', 'How can I help you?']


def todo_exit(user_in: str) -> list:
    return ['break', 'Good bye!']


def todo_show(user_in: str) -> list:
    if len(ADRESS_BOOK):
        return ['print', 'end of adress book']
    else:
        return ['print', 'adress book is empty']


@input_error
def todo_phone(user_in: str) -> str:
    """find by key
    """
    result = user_in.split(' ')
    if len(result) < 2:
        return ['', 'you need use \' \' to separate']
    return ADRESS_BOOK[result[1]]


OPERATIONS = {
    'add': todo_add,
    'change': todo_change,
    'phone': todo_phone,
    'hello': todo_hello,
    'exit': todo_exit,
    'good bye': todo_exit,
    'close': todo_exit,
    'show all': todo_show
}

if __name__ == '__main__':
    main()
