from collections import UserDict
from collections import UserString
import re
from datetime import datetime, timedelta
from calendar import monthrange
import csv
import pickle

users = {}

filename = 'record.csv'


class AddressBook(UserDict):

    rn = 0
    counter = 0

    def add_record(self, record):
        self.data[record.name.value] = record
        
    def remove_record(self, record):
        self.data.pop(record.name.value, None)

    def show_rec(self, name):
        return f'{name} (B-day: {self.data[name].birthday}): {", ".join([str(phone.value) for phone in self.data[name].phones])}'

    def show_all_rec(self):
        return "\n".join(f'{rec.name} (B-day: {rec.birthday}): {", ".join([p.value for p in rec.phones])}' for rec in self.data.values())

    def change_record(self, name_user, old_record_num, new_record_num):
        record = self.data.get(name_user)
        if record:
            record.change(old_record_num, new_record_num)
    
    def iterator(self, n):
        records = list(self.data.keys())
        records_num = len(records)
        count = 0
        result = ''
        if n > records_num:
            n = records_num
        for rec in self.data.values():
            if count < n:
                result += f'{rec.name} (B-day: {rec.birthday}): {", ".join([p.value for p in rec.phones])}\n'
                count += 1
        yield result

    # def __iter__(self):
    #     return AddressBook.iterator(self)

    def write_contacts_to_file(self, filename='record.csv'):
        # user = AddressBook()
        
        with open(filename, 'w', newline='') as fh:
            header = ['name', 'phone', 'birthday']
            writer = csv.DictWriter(fh, fieldnames=header)
            writer.writeheader()
            for value in self.data.values():
                writer.writerow(value.data)
                # for k, v in value.data.items():
             
                
            
    def read_contacts_from_file(self, filename='record.csv'):
        
        with open(filename, 'r', newline='') as fh:
            reader = csv.DictReader(fh)
            for record in reader:
                # print(dict(record))
                user_name = record['name']
                self.data[user_name] = record
            return self.data
                # self.data[record.name.value] = Record
               
                
                # cls = self.__class__.add_record(self, record)
             
                # cls.add_record(self, record)
            # for row in reader:
            #     self.data[row.name.value] = row
        # return reader
        
    def search_conrent(self, key_search = None):
        x = key_search
        result = []
        if x:
            for value in self.data.values():
                print('Value:', value)
                for k, v in value.data.items():
                    if str(v).find(x) == -1:
                        continue
                        # print(f'{x} was not found in {v}')
                    else:
                        print(f'{x}  found in user "{v}"')
                        result.append(value)
                        
            print('Result of your request:') 
            for el in result:
                for k,v in el.data.items():
                    print (k, ':', v)       
        else:
            print('You should input the value for searching')
    # def __getitem__(self, items):
    #     print(type(items), '!!' ,items)
        

class Field:

    def __init__(self, value):
        self._value = value

    def __str__(self):
        return self._value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return str(self._value)

    @Field.value.setter
    def value(self, value):
        self._value = value


class WrongLenPhone(Exception):
    """ Exception for wrong length of the phone number """


class WrongTypePhone(Exception):
    """ Exception when a letter is in the phone number """

class Phone(Field):

    @staticmethod
    def sanitize_phone_number(phone):
        new_phone = (
            str(phone).strip()
            .removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
        )
        try:
            new_phone = [str(int(i)) for i in new_phone]
        except ValueError:
            raise WrongTypePhone('Input correct phone')

        else:
            new_phone = "".join(new_phone)
            if len(new_phone) == 12:
                return f"+{new_phone}"
            elif len(new_phone) == 10:
                return f"+38{new_phone}"
            else:
                raise WrongLenPhone("Length of phone's number is wrong")

    def __init__(self, value):
        super().__init__(value)
        self._value = Phone.sanitize_phone_number(value)

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return str(self._value)

    @Field.value.setter
    def value(self, value):
        self._value = Phone.sanitize_phone_number(value)


class Birthday(datetime):

    @staticmethod
    def sanitize_date(year, month, day):
        try:
            birthday = datetime(year=year, month=month, day=day)
        except ValueError:
            print("Date is not correct. Please write date in format: yyyy-m-d")
        else:
            return str(birthday.date())
        
    def __init__(self, year, month, day):
        self.__birthday = self.sanitize_date(year, month, day)
        
    def __str__(self):
        return str(self.__birthday)

    def __repr__(self):
        return str(self.__birthday)

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, year, month, day):
        self.__birthday = self.sanitize_date(year, month, day)

# {'name': name 'phones': [phone, phones], 'birthday': birthday}
class Record:

    phone_list = []
    name = ''

    def __init__(self, name, phone=None, birthday=None):
        if birthday:
            self.birthday = Birthday(*birthday)
        else:
            self.birthday = None
        self.name = name
        self.phone = Phone(phone)
        self.birthday = birthday
        self.data = {'name': self.name,
                    'phone': self.phone, 'birthday': self.birthday}

    # def save_record(self, name, phone, birthday):
    #     phone_list = []
    #     self.data['name'] = name
    #     Record.name = name
    #     phone_list.append(phone)
    #     self.data['phone'] = phone_list
    #     self.data['birthday'] = birthday
    #     # Record.phone_list.append(phone)

    def add_phone(self, phone):
        phone = Phone(phone)
        if phone.value:
            lst = [phone.value for phone in self.phones]
            if phone.value not in lst:
                self.phones.append(phone)
                return "Phone was added"
        else:
            raise ValueError("Phone number is not correct")
        
    def remove_phone(self, phone_num):
        phone = Phone(phone_num)

        for ph in self.phones:
            if ph.value == phone.value:
                self.phones.remove(ph)
                return f'Phone {phone_num} deleted'
            else:
                return f'Number {phone_num} not found'

    def change(self, old_phone, new_phone):
        old_phone = Phone(old_phone)
        new_phone = Phone(new_phone)

        for phone in self.phones:
            if phone.value == old_phone.value:
                self.phones.remove(phone)
                self.phones.append(new_phone)
                return f'{old_phone} to {new_phone} changed'
            else:
                return print(f"Phone {old_phone} not found in the Record")

    def add_user_birthday(self, year, month, day):
        self.birthday = Birthday.sanitize_date(int(year), int(month), int(day))
    
    # return numbers of day to next birthday day
    # def days_to_birthday(self):
    #     current_date = datetime.now()
    #     current_year = current_date.year
    #     next_year = current_date.year + 1
    #     bd = self.birthday
    #     user_bd_month = int(bd[5:7])
    #     user_bd_day = int(bd[8:])
    #     user_bd = datetime(current_year, user_bd_month, user_bd_day)
    #     if current_date > user_bd:
    #         user_bd = datetime(current_year + 1, 1, 30).date()
    #         result = user_bd - current_date
    #         return result
    #     elif current_date <= user_bd:
    #         result = user_bd - current_date
    #         return result





# commands


# def hello(*args):
#     return 'How can I help you?'


# # def add(name, phone):
#     # name = args[0].capitalize()
#     # users[name] = args[1]

#     return f'User {name} was added'


# def change(*args):
#     name = args[0]
#     for key in users.keys():
#         if key == name:
#             users[key] = args[1]
#             return f"New {key}'s phone number is {args[1]}"


# def phone(*args):
#     name = args[0]
#     for key, value in users.items():
#         if key == name:
#             return f"User {key} has phone {value}"


# def show_all(*args):
#     return users


# def close(*args):
#     return 'Good by!'


# def input_error(func):
#     def inner(command, name, phone):
#         print('Function is calling')
#         try:
#             result = func(command, name, phone)
#             return result
#         except:
#             return 'Error'
#     return inner


# def parser(user_command_lower):
#     command = ''
#     arg_1 = ''
#     arg_2 = ''
#     if re.findall("^hello", user_command_lower) and len(user_command_lower.split()) == 1:
#         arg_list = user_command_lower.split()
#         command = arg_list[0]
#         return command, arg_1, arg_2
#     elif re.findall("^add", user_command_lower) and len(user_command_lower.split()) == 3:
#         arg_list = user_command_lower.split()
#         command = arg_list[0]
#         arg_1 = arg_list[1].capitalize()
#         arg_2 = arg_list[2]
#         return command, arg_1, arg_2
#     elif re.findall("^change", user_command_lower) and len(user_command_lower.split()) == 3:
#         arg_list = user_command_lower.split()
#         command = arg_list[0]
#         arg_1 = arg_list[1].capitalize()
#         arg_2 = arg_list[2]
#         return command, arg_1, arg_2
#     elif re.findall("^phone", user_command_lower) and len(user_command_lower.split()) == 2:
#         arg_list = user_command_lower.split()
#         command = arg_list[0]
#         arg_1 = arg_list[1].capitalize()
#         return command, arg_1, arg_2
#     elif user_command_lower == "show all":
#         command = "show all"
#         return command, arg_1, arg_2
#     elif user_command_lower == "good by" or user_command_lower == "close" or user_command_lower == "exit":
#         command = 'close'
#         return command, arg_1, arg_2
#     else:
#         return command, arg_1, arg_2


# @input_error
# # def handler(command, name, phone):
#     if command == 'add':
#         rec = Record(name, phone)
#         rec.save_record(name, phone)
#         ab = AddressBook()
#         ab.add_record(rec)
#         print(f'User {name} was added')
#     elif command == 'hello':
#         return hello()
#     elif command == 'change':
#        return change
#     elif command == 'phone':
#         return phone
#     elif command == 'show all':
#         return show_all
#     elif command == 'good by' or command == 'close' or command == 'exit':
#         return close
#     else:
#         return hello


def main():

    # while True:
    #     user_command = input('Input you comand: ')
    #     user_command_lower = user_command.lower()
    #     result = parser(user_command_lower)
    #     command = result[0]
    #     name = Name(result[1])
    #     phone = Phone(result[2])
    #     print(handler(command, name, phone))
    #     if command == 'good by' or command == 'close' or command == 'exit':
    #         break
    
    name = Name('Oleh')
    phone = Phone('1234789023')
    birthday = Birthday(1964, 12, 15)
    user = Record(name, phone)
    
    name1 = Name('Oksana')
    phone1 = Phone('1234789023')
    birthday1 = Birthday(1964, 9, 13)
    user1 = Record(name1, phone1)
    
    ab = AddressBook()
    print('ab', type(ab))
    
    ab.add_record(user)
    ab.add_record(user1)
   
  
        
    ab.search_conrent('23')
    
    ab.write_contacts_to_file()
    # ab = AddressBook()
    # reader = ab.read_contacts_from_file()
    
    # ab = AddressBook()
    
    print(ab.read_contacts_from_file())
    
    
    
    
  
   
    
 

    
    
    
    

        

        
        # print(el)
    

if __name__ == "__main__":
    main()
