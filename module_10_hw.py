# Критерії прийому
# 1. Реалізовано всі класи із завдання.
# 2. Записи Record у AddressBook зберігаються як значення у словнику. 
# В якості ключів використовується значення Record.name.value.
# 3. Record зберігає об'єкт Name в окремому атрибуті.
# 4. Record зберігає список об'єктів Phone в окремому атрибуті.
# 5. Record реалізує методи для додавання/видалення/редагування об'єктів Phone.
# 6. AddressBook реалізує метод add_record, який додає Record у self.data.


from collections import UserDict
from collections import UserList
from collections import UserString
import re

users = {}


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record['name']] = record


# {'name': name 'phones': [phone, phones]}
class Record(AddressBook, UserDict):

    phone_list = []
    name = ''

    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.data = {'name': self.name, 'phone': self.phone}

    def save_record(self, name, phone):
        phone_list = []
        self.data['name'] = name
        Record.name = name
        phone_list.append(phone)
        self.data['phone'] = phone_list
        # Record.phone_list.append(phone)

    def add_phone(self, name, phone):
        if self.data['name'] == name:
            self.data['phone'].append(phone)

    def remove_phone(self, name, phone):
        if self.data['name'] == name:
            self.data['phone'].remove(phone)


class Field(Record):
    pass


class Name(UserString, Field):

    def set_name(self, name):
        self.data = name

    def get_name(self):
        return self.data


class Phone(UserString, Field):

    def set_phone(self, phone):
        self.data = phone

    def get_phones(self):
        return self.data
 
#commands


def hello(*args):
    return 'How can I help you?'


# def add(name, phone):
    # name = args[0].capitalize()
    # users[name] = args[1]
    
    return f'User {name} was added'


def change(*args):
    name = args[0]
    for key in users.keys():
        if key == name:
            users[key] = args[1]
            return f"New {key}'s phone number is {args[1]}"


def phone(*args):
    name = args[0]
    for key, value in users.items():
        if key == name:
            return f"User {key} has phone {value}"


def show_all(*args):
        return users


def close(*args):
    return 'Good by!'


def input_error(func):
    def inner(command, name, phone):
        print('Function is calling')
        try:
            result = func(command, name, phone)
            return result
        except:
            return 'Error'
    return inner


def parser(user_command_lower):
    command = ''
    arg_1 = ''
    arg_2 = ''
    if re.findall("^hello", user_command_lower) and len(user_command_lower.split()) == 1:
        arg_list = user_command_lower.split()
        command = arg_list[0]
        return command, arg_1, arg_2
    elif re.findall("^add", user_command_lower) and len(user_command_lower.split()) == 3:
        arg_list = user_command_lower.split()
        command = arg_list[0]
        arg_1 = arg_list[1].capitalize()
        arg_2 = arg_list[2]
        return command, arg_1, arg_2
    elif re.findall("^change", user_command_lower) and len(user_command_lower.split()) == 3:
        arg_list = user_command_lower.split()
        command = arg_list[0]
        arg_1 = arg_list[1].capitalize()
        arg_2 = arg_list[2]
        return command, arg_1, arg_2
    elif re.findall("^phone", user_command_lower) and len(user_command_lower.split()) == 2:
        arg_list = user_command_lower.split()
        command = arg_list[0]
        arg_1 = arg_list[1].capitalize()
        return command, arg_1, arg_2
    elif user_command_lower == "show all":
        command = "show all"
        return command, arg_1, arg_2
    elif user_command_lower == "good by" or user_command_lower == "close" or user_command_lower == "exit":
        command = 'close'
        return command, arg_1, arg_2
    else:
        return command, arg_1, arg_2


@input_error
def handler(command, name, phone):
    if command == 'add':
        rec = Record(name, phone)
        rec.save_record(name, phone)
        ab = AddressBook()
        ab.add_record(rec)
        print (f'User {name} was added')
    elif command == 'hello':
        return hello()
    elif command == 'change':
       return change
    elif command == 'phone':
        return phone
    elif command == 'show all':
        return show_all
    elif command == 'good by' or command == 'close' or command == 'exit':
        return close
    else:
        return hello

def main():
    
    while True:
        user_command = input('Input you comand: ')
        user_command_lower = user_command.lower()
        result = parser(user_command_lower)
        command = result[0]
        name = Name(result[1])
        phone = Phone(result[2])
        print(handler(command, name, phone))
        if command == 'good by' or command == 'close' or command == 'exit':
            break

   

if __name__ == "__main__":
    main()
