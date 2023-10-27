"""
Console Assistant Bot

This is a simple console-based assistant bot that allows users to manage contacts.
Users can add, change, and view contact details.

Usage:
- 'add [name] [phone]': Add a new contact with a name and phone number.
- 'change [name] [new_phone]': Change the phone number for an existing contact.
- 'phone [name]': View the phone number for a specific contact.
- 'all': View all contacts and their phone numbers.
- 'add-birthday [name] [birthday]': Set the birthday for a contact with the given name.
- 'show-birthday [name]': Show the birthday for a contact with the given name.
- 'birthdays': Show the names of contacts who have birthdays in
   the next week, grouped by the day of the week.
- 'hello': Greetings from the bot.
- 'close' or 'exit': Exit the bot.

Instructions:
- Enter commands as described above to interact with the bot.
- The bot will provide feedback and instructions based on the commands.

"""

from collections import defaultdict, UserDict
from datetime import datetime, timedelta


class Field:
    """
    The Field class represents a basic field in a contact record.

    Attributes:
    - value: The value stored in the field.

    Methods:
    - __init__(self, value): Initializes a new Field instance with the given value.
    - __str__(self): Returns a string representation of the field's value.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """
    The Name class represents the name field in a contact record.

    Attributes:
    - value: The name value stored in the field.

    Methods:
    - __init__(self, value): Initializes a new Name instance with the given name value.
    """

    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)


class Phone(Field):
    """
    The Phone class represents a phone number field in a contact record.

    Attributes:
    - value: The phone number value stored in the field.

    Methods:
    - __init__(self, value): Initializes a new Phone instance with the given phone number value.
    - validate_phone(self): Checks if the phone number has a valid format (10 digits).

    Example usage:
    phone = Phone("1234567890")
    print(phone)  # Output: 1234567890
    """

    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Invalid phone number format")
        super().__init__(value)

    @staticmethod
    def validate_phone(value):
        """
        Checks if the phone number has a valid format (10 digits).

        Returns:
        - True if the phone number has a valid format, False otherwise.
        """
        return len(value) == 10 and value.isdigit()


class Birthday(Field):
    """
    The Birthday class represents a birthday date field in a contact record.

    Attributes:
    - value: The birthday date value stored in the field (format: DD.MM.YYYY).

    Methods:
    - __init__(self, value): Initializes a new Birthday instance with the given birthday date value.
    - validate_birthday(self): Checks if the birthday date has a valid format (DD.MM.YYYY).
    - to_datetime(self): Return a datetime object based on the given Birthday

    Example usage:
    birthday = Birthday("15.06.1990")
    print(birthday)  # Output: 15.06.1990
    """

    def __init__(self, value):
        if not self.validate_birthday(value):
            raise ValueError("Invalid birthday format. Use DD.MM.YYYY")
        super().__init__(value)

    @staticmethod
    def validate_birthday(value):
        """
        Checks if the birthday date has a valid format (DD.MM.YYYY).

        Returns:
        - True if the birthday date has a valid format, False otherwise.
        """
        try:
            datetime.strptime(value, '%d.%m.%Y')
            return True
        except ValueError:
            return False

    def to_datetime(self):
        """
        Return a datetime object based on the value of this Birthday
        """
        return datetime.strptime(self.value, '%d.%m.%Y')


class Record:
    """
    The Record class represents a contact record containing information about a person.

    Attributes:
    - name: An instance of the Name class representing the contact's name (required).
    - phones: A list of Phone instances representing phone numbers for the contact.
    - birthday: An instance of the Birthday class representing the contact's birthday (optional).

    Methods:
    - __init__(self, name): Initializes a new Record instance with the given name.
    - add_phone(self, phone): Adds a phone number to the contact's record.
    - remove_phone(self, phone): Removes a phone number from the contact's record.
    - edit_phone(self, old_phone, new_phone): Edits a phone number in the contact's record.
    - find_phone(self, phone): Finds and returns a phone number in the contact's record.
    - __str__(self): Returns a string representation of the contact record.

    Example usage:
    john = Record("John")
    john.add_phone("1234567890")
    john.add_birthday("15.06.1990")
    print(john)
    # Output: Contact name: John Doe, phones: 1234567890; 5555555555
    """

    def __init__(self, name):
        """
        Initializes a new Record instance with the given name.

        Args:
        - name: A string representing the contact's name (required).
        """
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        """
        Adds a phone number to the contact's record.

        Args:
        - phone: A string representing the phone number.
        """
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        """
        Adds the birthday to the contact's record.

        Args:
        - phone: A string representing the birthday.
        """
        self.birthday = Birthday(birthday)

    def remove_phone(self, phone):
        """
        Removes a phone number from the contact's record.

        Args:
        - phone: A string representing the phone number to be removed.
        """
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        """
        Edits a phone number in the contact's record.

        Args:
        - old_phone: A string representing the old phone number.
        - new_phone: A string representing the new phone number.
        """
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                break

    def find_phone(self, phone):
        """
        Finds and returns a phone number in the contact's record.

        Args:
        - phone: A string representing the phone number to be found.

        Returns:
        - An instance of the Phone class representing the found phone number or None if not found.
        """
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def get_birthday(self):
        """
        Returns the birthday of the contact's record.

        Returns:
        - An instance of the Birthday class representing the birthday or
          None if the birthday is not set.
        """
        return self.birthday

    def __str__(self):
        phones_str = "; ".join(str(phone) for phone in self.phones)
        return f"Contact name: {self.name}, phones: {phones_str}"


class AddressBook(UserDict):
    """
    The AddressBook class represents an address book that stores and manages contact records.

    Attributes:
    - data: A dictionary where keys are contact names (str) and values are Record instances.

    Methods:
    - add_record(self, record): Adds a contact record to the address book.
    - find(self, name): Finds and returns a contact record by name.
    - delete(self, name): Deletes a contact record by name.
    - get_birthdays_per_week(self): Returns a list of contacts with birthdays in the next week.

    Example usage:
    book = AddressBook()
    john = Record("John Doe")
    john.add_phone("1234567890")
    john.add_birthday("29.10.2023)
    book.add_record(john)
    jane = Record("Jane")
    jane.add_phone("9876543210")
    jane.add_birthday("30.10.2023)
    book.add_record(jane)
    """

    def add_record(self, record):
        """
        Adds a contact record to the address book.

        Args:
        - record: An instance of the Record class representing the contact record.
        """
        self.data[record.name.value] = record

    def find(self, name) -> Record:
        """
        Finds and returns a contact record by name.

        Args:
        - name: A string representing the name of the contact to be found.

        Returns:
        - An instance of the Record class representing the found contact record or
          None if not found.
        """
        return self.data.get(name, None)

    def delete(self, name):
        """
        Deletes a contact record by name.

        Args:
        - name: A string representing the name of the contact to be deleted.
        """
        if name in self.data:
            del self.data[name]

    def get_birthdays_per_week(self):
        """
        Returns the upcoming birthdays within the next week, grouped by the day of the week.

        Returns:
        - dict with users to greet next week.
        """
        birthdays_by_day = defaultdict(list)

        today = datetime.today().date()

        for name in self.data:
            birthday = self.data[name].get_birthday()

            if not birthday:
                continue

            birthday = birthday.to_datetime().date()

            birthday_this_year = birthday.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(
                    year=today.year + 1)

            if birthday_this_year.weekday() > 4:
                delta_days = 6 - birthday_this_year.weekday() + 1
                birthday_this_year = birthday_this_year.replace(
                    day=birthday.day + delta_days)

            delta_days = (birthday_this_year - today).days
            if delta_days >= 7:
                continue

            day_of_week = (today + timedelta(days=delta_days)).strftime("%A")

            birthdays_by_day[day_of_week].append(name)

        return birthdays_by_day


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
    try:
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
    except ValueError:
        return None, []

    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    """
    Adds a contact into address book.

    Args:
    args (list of str): A list containing the name (str) and phone number (str).
    book (dict): An address book containing contacts where keys are names and
                     values are Records.

    Returns:
    str: A message confirming the addition of the contact or an error message.
    """
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return "Contact added."


@input_error
def change_contact(args, book: AddressBook):
    """
    Changes the phone number for an existing contact.

    Args:
    args (list of str): A list containing the name (str) and the new phone number (str).
    book (dict): An address book containing contacts where keys are names and
                     values are Records.

    Returns:
    str: A message confirming the contact update or an error message.
    """
    name, new_phone = args

    record = book.find(name)

    if record is None:
        raise KeyError(name)

    record.add_phone(new_phone)
    return "Contact updated."


@input_error
def show_phone(args, book: AddressBook):
    """
    Shows the phone number for a specific contact.

    Args:
    args (list of str): A list containing the name (str) of the contact.
    book (dict): An address book containing contacts where keys are names and
                     values are Records.

    Returns:
    str: The phone number of the contact or an error message.
    """
    if len(args) != 1:
        raise IndexError()

    name = args[0]

    record = book.find(name)

    if record is None:
        raise KeyError(name)

    return record.phones[0].value


@input_error
def show_all(book: AddressBook):
    """
    Shows all contacts and their phone numbers.

    Args:
    book (dict): An address book containing contacts where keys are names and
                     values are Records.

    Returns:
    str: A formatted string containing all contacts and phone numbers or
         a message if no contacts are found.
    """
    if not book:
        return "No contacts found."

    return "\n".join([f"{name}: {record.phones[0].value}"
                      for name, record in book.items()])


@input_error
def add_birthday(args, book: AddressBook):
    """
    Adds the birthday for a contact.

    Args:
    args (list of str): A list containing the name (str) and the birthday (str).
    book (dict): An address book containing contacts where keys are names and
                     values are Records.

    Returns:
    str: A message confirming the addition of the birthday or an error message.
    """
    name, birthday = args

    record = book.find(name)

    if record is None:
        raise KeyError(name)

    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book: AddressBook):
    """
    Shows the birthday for a specific contact.

    Args:
    args (list of str): A list containing the name (str) of the contact.
    book (dict): An address book containing contacts where keys are names and
                     values are Records.

    Returns:
    str: The birthday of the contact or an error message.
    """
    if len(args) != 1:
        raise IndexError()

    name = args[0]

    record = book.find(name)

    if record is None:
        raise KeyError(name)

    birthday = record.get_birthday()

    if birthday is None:
        return "Birthday is not set."

    return record.birthday.value


@input_error
def birthdays(book: AddressBook):
    """
    Prints the names of contacts who have birthdays in
    the next week, grouped by the day of the week.

    Args:
    book (dict): An address book containing contacts where keys are names and
                     values are Records.
    """
    bdays = book.get_birthdays_per_week()

    if not bdays:
        print("No birthdays in the next week.")
        return

    print("Birthdays in the next week:")
    for day, name in bdays.items():
        print(f"{day}: {name}")


def main():
    """
    Main function for the console assistant bot.
    """
    book = AddressBook()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            birthdays(book)
        elif command == "hello":
            print("How can I help you?")
        elif command in ["close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
