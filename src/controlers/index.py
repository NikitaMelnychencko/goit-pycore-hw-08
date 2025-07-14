from helper.color_loger import log_error
from services.NotebookServices import AddressBook, Record, Name, Phone

def validate_args(args, required_count, error_message):
    """Checks if there are enough arguments for the command"""
    if len(args) < required_count:
        print(error_message)
        return False
    return True

def find_contact_safe(book, name):
    """Safely finds contact by name"""
    try:
        return book.find(name)
    except:
        return None

def add_contact(book, args):
	is_valid = validate_args(args, 2, "Please provide name and phone number")
	if is_valid:
		record = find_contact_safe(book, args[0])
		if record:
			record.add_phone(args[1])
			print(book)
		else:
			record = Record(args[0])
			# Check if the name is valid and not empty
			if hasattr(record.name, 'value') and record.name.value != "":
				record.add_phone(args[1])
				if len(record.phones) > 0:
					book.add_record(record)
					print(book)

def change_contact(book, args):
  if not validate_args(args, 3, "Please provide name, old phone number and new phone number"):
    return

  record = find_contact_safe(book, args[0])
  if record:
    record.edit_phone(args[1], args[2])
    print(book)
  else:
    print("Contact not found")

def find_contact(book, args):
  if not validate_args(args, 1, "Please provide name"):
    return

  record = find_contact_safe(book, args[0])
  if record:
    print(record)
  else:
    print("Contact not found")

def remove_phone(book, args):
  if not validate_args(args, 2, "Please provide name and phone number"):
    return

  record = find_contact_safe(book, args[0])
  if record:
    record.remove_phone(args[1])
    print(book)
  else:
    print("Contact not found")

def remove_contact(book, args):
  if not validate_args(args, 1, "Please provide name"):
    return

  record = find_contact_safe(book, args[0])
  if record:
    book.delete(args[0])
    print(book)
  else:
    print("Contact not found")

def add_birthday(book, args):
  if not validate_args(args, 2, "Please provide name and birthday (DD.MM.YYYY)"):
    return

  record = find_contact_safe(book, args[0])
  if record:
    record.add_birthday(args[1])
    print(book)
  else:
    print("Contact not found")

def show_birthday(book, args):
  if not validate_args(args, 1, "Please provide name"):
    return

  record = find_contact_safe(book, args[0])
  if record:
    print(f"Contact name: {args[0]}, Birthday: {record.show_birthday()}")
  else:
    print("Contact not found")

def show_birthdays(book, args):
  upcoming_birthdays = book.get_upcoming_birthdays()
  if upcoming_birthdays:
    for birthday in upcoming_birthdays:
      print(f"Name: {birthday['name']}, Birthday: {birthday['congratulation_date']}")
  else:
    print("No upcoming birthdays")

def show_all(book, args):
  print(book)

def exit_program(book, data):
  all_book = book.get_contacts_for_json()
  data.save_data(all_book)
  print("Goodbye!")
  return True