from collections import UserDict
from datetime import datetime
import pickle


class AddressBook(UserDict):
    filename = 'AddressBook.bin'

    def save_to_file(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self, file)

    def read_from_file(self):
        try:
            with open(self.filename, "rb") as file:
                content = pickle.load(file)
        except FileNotFoundError:
            return self
        return content

    def str_find(self, key):
        result = ''
        # find in names
        for record in self.data.keys():
            if key in record:
                finded_rec = self.data.get(record)
                result += f'{str(finded_rec.name)}:{finded_rec.name.value} \nphone: {finded_rec.show_rec()}\n'
            # find in phones
            rec_res = self.data.get(record).str_find(key)
            if not rec_res is None:
                result += f'{str(rec_res.name)}:{rec_res.name.value} \nphone: {rec_res.show_rec()}\n'
        if result == '':
            result = 'none finded'
        return result

    def record_add(self, cur_rec):

        old_rec = self.record_find(cur_rec.name.value)
        if old_rec is None:
            self.data[cur_rec.name.value] = cur_rec
        else:
            old_rec.phones.append(cur_rec.phones[0])

    def record_find(self, key: str):
        if self.data.get(key):
            return self.data.get(key)
        return None

    def print_AB(self):
        res_str = ''
        cur_page = 1

        for rec_on_page in self.iterator(2):
            res_str += f' __PAGE:{cur_page}__  \n'
            cur_page += 1
            for rec in rec_on_page:
                res_str += f'{str(rec.name)}:{rec.name.value} \nphone: {rec.show_rec()}\n'
            res_str += f'_________\n'
        return res_str

    def record_delete(self, key):
        del self.data[key]

    def iterator(self, len_list=3):
        result = []
        iter = 0

        for record in self.data.values():
            result.append(record)
            iter += 1

            if iter == len_list:
                yield result
                result = []
                iter = 0

        if result:
            yield result


class Record:

    def __init__(self, value):
        self.name = Name(value)
        self.phones = []
        self.birthday = None

    def birthday_add(self, value):
        self.birthday = Birthday(value)

    def day_to_birthday(self):
        if not self.birthday:
            raise ValueError('contact haven\'t birthday info')
        shift = (datetime(datetime.today().year, self.birthday.value.month,
                 self.birthday.value.day).date() - datetime.today().date()).days
        if shift < 0:
            return (datetime(datetime.today().year+1, self.birthday.value.month, self.birthday.value.day).date() - datetime.today().date()).days
        return shift

    def phone_add(self, value):
        self.phones.append(Phone(value))

    def phone_change(self, value_old, value_new):
        try:
            self.phones.remove(self.phone_find(value_old))
        except ValueError:
            raise ValueError('Wrong old phone')
        self.phones.append(Phone(value_new))

    def phone_delete(self, value):
        try:
            self.phones.remove(self.phone_find(value))
        except ValueError:
            raise ValueError('Wrong old phone')

    def phone_find(self, key: str):
        for phone in self.phones:
            if phone.value == key:
                return phone

    def str_find(self, key: str):
        for phone in self.phones:
            if key in phone.value:
                return self

    def show_rec(self):
        res_str = ''
        for iter in self.phones:
            res_str += f'\n{iter.value}'
        if self.birthday:
            res_str += f'\n{str(self.birthday)}:{self.birthday.value}'
        return res_str


class Field:
    field_description = "General"

    def __init__(self, value):
        self._value = None
        self.value = value

    def __str__(self) -> str:
        return f'{self.field_description}'

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Phone(Field):
    field_description = "Phone"

    @Field.value.setter
    def value(self, value: str):
        value = (value.strip().removeprefix("+")
                 .replace("(", "")
                 .replace(")", "")
                 .replace("-", "")
                 .replace(" ", ""))
        if not value.isnumeric():
            raise ValueError('Wrong phones.')
        self._value = value


class Name(Field):
    field_description = "Name"

    @Field.value.setter
    def value(self, value: str):
        if value.isnumeric():
            raise ValueError('Wrong Name.')
        self._value = value


class Birthday(Field):
    field_description = "Birthday"

    @Field.value.setter
    def value(self, value):
        try:
            self._value = datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("Birthday must be format YYYY-m-d")
