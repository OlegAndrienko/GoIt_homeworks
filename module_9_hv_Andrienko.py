def main():

    import re

    users = {}

    def hello(*args):
        return 'How can I help you?'

    def add(*args):
        name = args[0].capitalize()
        users[name] = args[1]
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
        def inner(command):
            print('Function is calling')
            try:
                result = func(command)
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
    def handler(command):
        if command == 'add':
            return add
        elif command == 'hello':
            return hello
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

    while True:
        user_command = input('Input you comand: ')
        user_command_lower = user_command.lower()
        result = parser(user_command_lower)
        command = result[0]
        arg_1 = result[1]
        arg_2 = result[2]
        print(handler(command)(arg_1, arg_2))
        if command == 'good by' or command == 'close' or command == 'exit':
            break


if __name__ == "__main__":
    main()
