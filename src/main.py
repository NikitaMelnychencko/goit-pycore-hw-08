from services.NotebookServices import AddressBook
from services.DataServices import DataServices
from helper.color_loger import log_error
from controlers.index import (
    add_contact, change_contact, find_contact, remove_phone,
    remove_contact, add_birthday, show_birthday, show_birthdays,
    show_all, exit_program
)

def parse_input(user_input):
  cmd, *args = user_input.split()
  cmd = cmd.strip().lower()
  return cmd, *args


welcome_bunner = """
 █████╗ ███████╗███████╗██╗███████╗████████╗ █████╗ ███╗   ██╗████████╗    ██████╗  ██████╗ ████████╗
██╔══██╗██╔════╝██╔════╝██║██╔════╝╚══██╔══╝██╔══██╗████╗  ██║╚══██╔══╝    ██╔══██╗██╔═══██╗╚══██╔══╝
███████║███████╗███████╗██║███████╗   ██║   ███████║██╔██╗ ██║   ██║       ██████╔╝██║   ██║   ██║
██╔══██║╚════██║╚════██║██║╚════██║   ██║   ██╔══██║██║╚██╗██║   ██║       ██╔══██╗██║   ██║   ██║
██║  ██║███████║███████║██║███████║   ██║   ██║  ██║██║ ╚████║   ██║       ██████╔╝╚██████╔╝   ██║
╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝       ╚═════╝  ╚═════╝    ╚═╝

"""

commands = """
  Commands:
  ---------
  1. hello
  2. add <username> <phone>
  3. change <username> <old_phone> <new_phone>
  4. remove_phone <username> <phone>
    Description: remove phone from contact
  5. remove <username>
    Description: remove contact
  6. phone <username>
  7. add-birthday <username> <birthday> Format:DD.MM.YYYY
  8. show-birthday <username>
  9. birthdays
  10. all
  11. close, exit
  ---------
"""


def main():
    data = DataServices()
    book = AddressBook(data.get_init_data())
    print(welcome_bunner)
    print("Welcome to the assistant bot!")
    print(commands)

    while True:
        user_input = input("Enter a command: ")
        try:
            command, *args = parse_input(user_input)
        except Exception as e:
            log_error("Invalid command.")
            continue

        match (command.lower()):
            case "hello":
                print("How can I help you?")
            case "add":
                add_contact(book, args)
            case "change":
                change_contact(book, args)
            case "phone":
                find_contact(book, args)
            case "remove_phone":
                remove_phone(book, args)
            case "remove":
                remove_contact(book, args)
            case "add-birthday":
                add_birthday(book, args)
            case "show-birthday":
                show_birthday(book, args)
            case "birthdays":
                show_birthdays(book, args)
            case "all":
                show_all(book, args)
            case "exit" | "close":
                if exit_program(book, data):
                    break
            case _:
                log_error("Invalid command.")

if __name__ == "__main__":
    main()
