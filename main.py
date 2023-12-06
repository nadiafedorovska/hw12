import pickle
from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Birthday(Field):
    @Field.value.setter
    def value(self, value):
        if value:
            self._value = datetime.strptime(value, '%Y.%m.%d').date()
        else:
            self._value = None

class Phone(Field):
    def __init__(self, value):
        if not self.is_valid_phone(value):
            raise ValueError("Phone number must be a ten digit string of digits")
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if not self.is_valid_phone(value):
            raise ValueError("Phone number must be a ten digit string of digits")
        self._value = value

    def is_valid_phone(self, value):
        return value.isdigit() and len(value) == 10

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)

    def remove_phone(self, phone):
        for phone in self.phones:
            if phone in self.phones:
                self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        old_phone_obj = Phone(old_phone)
        for phone in self.phones:
            if phone.value == old_phone_obj.value:
                self.remove_phone(old_phone)
                self.add_phone(new_phone)
                return
        raise ValueError(f"Phone {old_phone} not found")

    def days_to_birthday(self):
        try:
            if self.birthday and self.birthday.value:
                today = datetime.now().date()
                next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day).date()
                if today > next_birthday:
                    next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day).date()
                return (next_birthday - today).days
        except Exception as e:
            print(f"Error calculating days to birthday: {e}")
        return None

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, item_number):
        counter = 0
        result = ''
        for item, record in self.data.items():
            result += f'{item}: {record}\n'
            counter += 1
            if counter >= item_number:
                yield result
                counter = 0
                result = ''
        if result:
            yield result

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            print(f"File {filename} not found. ")
        except Exception as e:
            print(f"Error loading data from file {filename}: {e}")