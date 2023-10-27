"""
Console Assistant Bot

This is a simple console-based assistant bot that allows users to manage contacts.
Users can add, change, and view contact details.

Usage:
- 'hello': Greet the bot.
- 'add [name] [phone]': Add a new contact with a name and phone number.
- 'change [name] [new_phone]': Change the phone number for an existing contact.
- 'phone [name]': View the phone number for a specific contact.
- 'all': View all contacts and their phone numbers.
- 'close' or 'exit': Exit the bot.

Instructions:
- Enter commands as described above to interact with the bot.
- The bot will provide feedback and instructions based on the commands.

"""

from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        Phone.validate_phone(value)
        super().__init__(value)

    @classmethod
    def validate_phone(cls, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits")

    def phone_set(self, value):
        Phone.validate_phone(value)
        self.value = value

    def phone_get(self):
        return self.value


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.phone_get() != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.phone_get() == old_phone:
                phone.phone_set(new_phone)
                break

    def find_phone(self, phone):
        for p in self.phones:
            if p.phone_get() == phone:
                return p
        return None

    def __str__(self):
        phones_str = "; ".join(str(phone) for phone in self.phones)
        return f"Contact name: {self.name}, phones: {phones_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]


def input_error(func):
    """
    Decorator to handle input errors and return appropriate messages.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The decorated function.

    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError as e:
            return f"Contact '{e.args[0]}' not found."
        except IndexError:
            return "Invalid command format."

    return inner


def parse_input(user_input: str):
    """
    Parses the user input to extract the command and arguments.

    Args:
    user_input (str): The user's input.

    Returns:
    tuple: A tuple containing the command (str) and a list of arguments (list of str).
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, contacts):
    """
    Adds a contact to the contacts dictionary.

    Args:
    args (list of str): A list containing the name (str) and phone number (str).
    contacts (dict): A dictionary containing contacts where keys are names and 
                     values are phone numbers.

    Returns:
    str: A message confirming the addition of the contact or an error message.
    """
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts):
    """
    Changes the phone number for an existing contact.

    Args:
    args (list of str): A list containing the name (str) and the new phone number (str).
    contacts (dict): A dictionary containing contacts where keys are names and
                     values are phone numbers.

    Returns:
    str: A message confirming the contact update or an error message.
    """
    name, new_phone = args

    if name not in contacts:
        raise KeyError(name)

    contacts[name] = new_phone
    return "Contact updated."


@input_error
def show_phone(args, contacts):
    """
    Shows the phone number for a specific contact.

    Args:
    args (list of str): A list containing the name (str) of the contact.
    contacts (dict): A dictionary containing contacts where keys are names and
                     values are phone numbers.

    Returns:
    str: The phone number of the contact or an error message.
    """
    if len(args) != 1:
        raise IndexError()

    name = args[0]

    if name not in contacts:
        raise KeyError(name)

    return contacts[name]


@input_error
def show_all(contacts):
    """
    Shows all contacts and their phone numbers.

    Args:
    contacts (dict): A dictionary containing contacts where keys are names and
                     values are phone numbers.

    Returns:
    str: A formatted string containing all contacts and phone numbers or
         a message if no contacts are found.
    """
    if not contacts:
        return "No contacts found."

    return "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])


def main():
    """
    Main function for the console assistant bot.
    """
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")


def tests():
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")


if __name__ == "__main__":
    tests()
    main()
