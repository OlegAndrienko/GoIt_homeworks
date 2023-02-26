from collections import UserDict
from collections import UserList
from collections import UserString
import re
from datetime import datetime, timedelta
from calendar import monthrange

users = {}


class AddressBook(UserDict):
    
    rn = 0
    counter = 0
  

    def add_record(self, record):
        self.data[record['name']] = record
       
    
    def iterator(self, record_number = 2):
        
        def __next__(self):
            while AddressBook.counter <= record_number:
                result = self.data[self.counter]
                return result   
            raise StopIteration
            
        return __next__(self)
        
    def __iter__(self):
        return AddressBook.iterator(self)
       


# {'name': name 'phones': [phone, phones], 'birthday': birthday}
class Record(AddressBook, UserDict):

    phone_list = []
    name = ''

    def __init__(self, name, phone, birthday=''):
        self.name = name
        self.phone = phone
        self.birthday = birthday
        self.data = {'name': self.name, 'phone': self.phone, 'birthday': self.birthday}

    def save_record(self, name, phone, birthday):
        phone_list = []
        self.data['name'] = name
        Record.name = name
        phone_list.append(phone)
        self.data['phone'] = phone_list
        self.data['birthday'] = birthday
        # Record.phone_list.append(phone)

    def add_phone(self, name, phone):
        if self.data['name'] == name:
            self.data['phone'].append(phone)

    def remove_phone(self, name, phone):
        if self.data['name'] == name:
            self.data['phone'].remove(phone)
            
    #return numbers of day to next birthday day
    def days_to_birthday(self):
        current_date = datetime.now()
        current_year = current_date.year
        next_year = current_date.year + 1
        bd = self.birthday
        user_bd_month = int(bd[5:7])
        user_bd_day = int(bd[8:])
        user_bd = datetime(current_year, user_bd_month, user_bd_day)
        if current_date > user_bd:
            user_bd = datetime(current_year + 1, 1, 30).date()
            result = user_bd - current_date
            return result
        elif current_date <= user_bd:
            result = user_bd - current_date
            return result
        
    
        


class Field(Record):
    pass


class Name(UserString, Field):

    def set_name(self, name):
        self.data = name

    def get_name(self):
        return self.data


class Phone(UserString, Field):
    
    def __init__(self, phone):
        self.__phone = None
        self.phone = phone
        
    @property
    def phone(self):
        return self.__phone
    
    @phone.setter
    def phone(self, value: str):
        if not value.isalpha() and len(value) == 10:
            self.__phone = value
        else:
            raise Exception('Wrong phone number')
        
 
class Birthday(UserString, Field):
    
    def __init__(self, birthday):
        self.__birthday = None
        self.birthday = birthday
        
    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, value: str):
        if  len(value) == 10:
            self.__birthday = value
        else:
            raise Exception('Wrong birthday data')
    
    
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
