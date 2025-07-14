from helper.color_loger import  log_warning
from decorators.error_decorators import input_error
from collections import UserDict
from dataclasses import dataclass
from datetime import datetime, date, timedelta

class Field:
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return str(self.value)

class Name(Field):
  @input_error
  def __init__(self, value):
    if not value.isalpha():
      raise ValueError("Name must contain only letters")
    self.value = value


class Phone(Field):
  @input_error
  def __init__(self, value):
    if not value.isdigit():
      raise ValueError("Phone number must contain only digits")
    if len(value) != 10:
      raise ValueError("Phone number must be 10 digits")
    self.value = value

class Birthday(Field):
    def __init__(self, value):
        try:
          data = datetime.strptime(value, "%d.%m.%Y")
          if data:
            self.value = value
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

@dataclass
class Record:
  name: Name
  phones: list[Phone] | None
  birthday: Birthday | None

class Record(Record):
  def __init__(self, name):
    self.name = Name(name)
    self.phones = []
    self.birthday = None

  def add_phone(self, phone):
    phone_at_list = Phone(phone)
    if hasattr(phone_at_list, 'value') and phone_at_list.value != "":
      self.phones.append(phone_at_list)

  def remove_phone(self, phone):
    self.phones = [p for p in self.phones if p.value != phone]

  @input_error
  def add_birthday(self, birthday):
    self.birthday = Birthday(birthday)
  @input_error
  def show_birthday(self):
    return self.birthday.value if self.birthday else "No birthday"

  @input_error
  def edit_phone(self, old_phone, new_phone):
    for i, p in enumerate(self.phones):
      if p.value == old_phone:
        phone_at_list = Phone(new_phone)
        if hasattr(phone_at_list, 'value') and phone_at_list.value != "":
          self.phones[i] = phone_at_list
        return
    raise ValueError(f"Phone {old_phone} not found")

  def find_phone(self, phone):
    for p in self.phones:
      if p.value == phone:
        return p
    return None

  def to_dict(self):
    """Converts Record to dictionary for JSON serialization"""
    return {
      "name": self.name.value,
      "phones": [p.value for p in self.phones],
      "birthday": self.birthday.value if self.birthday else None
    }

  @classmethod
  def from_dict(cls, data):
    """Creates Record from dictionary after JSON deserialization"""
    record = cls(data["name"])
    for phone in data.get("phones", []):
      record.add_phone(phone)
    if data.get("birthday"):
      record.add_birthday(data["birthday"])
    return record

  def __str__(self):
    if len(self.phones) > 0 and self.name.value != "":
      return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday.value if self.birthday else 'No birthday'}"
    return ""


class AddressBook(UserDict):
  def __init__(self, initial_contacts=None):
    if initial_contacts and isinstance(list(initial_contacts.values())[0] if initial_contacts else None, dict):
      # If data came from JSON (as dictionaries), convert them to Record objects
      self.data = {}
      for name, contact_data in initial_contacts.items():
        self.data[name] = Record.from_dict(contact_data)
    else:
      # If data are already Record objects
      self.data = initial_contacts if initial_contacts else {}

  def add_record(self, record):
    self.data[record.name.value] = record

  @input_error
  def find(self, name):
    if name == "":
      raise ValueError("Please provide name")
    return self.data.get(name)

  def delete(self, name):
    del self.data[name]

  @staticmethod
  def find_next_weekday(start_date, weekday):
    days_ahead = weekday - start_date.weekday()
    if days_ahead <= 0:
      days_ahead += 7
    return start_date + timedelta(days=days_ahead)

  def adjust_for_weekend(self, birthday):
    if birthday.weekday() >= 5:
      return AddressBook.find_next_weekday(birthday, 0)
    return birthday

  def get_upcoming_birthdays(self, days=7):
    upcoming_birthdays = []
    today = date.today()

    for contact in self.data.values():
      if contact.birthday:
        # Конвертуємо datetime в date для порівняння
        birthday_date = datetime.strptime(contact.birthday.value, "%d.%m.%Y").date()
        birthday_this_year = birthday_date.replace(year=today.year)

        # Перевіряємо, чи не буде припадати день народження вже наступного року
        if birthday_this_year < today:
          birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        if 0 <= (birthday_this_year - today).days <= days:
          # Переносимо дату привітання на наступний робочий день, якщо день народження припадає на вихідний
          birthday_this_year = self.adjust_for_weekend(birthday_this_year)
          congratulation_date_str = birthday_this_year.strftime("%Y.%m.%d")
          upcoming_birthdays.append({"name": contact.name.value, "congratulation_date": congratulation_date_str})
    return upcoming_birthdays

  @input_error
  def get_contacts_for_json(self):
    """Returns contacts in format suitable for JSON serialization"""
    return {name: record.to_dict() for name, record in self.data.items()}

  def __str__(self):
    return "\n".join(str(record) for record in self.data.values())
