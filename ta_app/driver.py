from ta_app.ui import UI


def main():
    ui = UI()

    # login default_superuser default_password
    print("Welcome. Please login (login <username> <password>")
    user_input = ''
    while user_input != "exit":
        user_input = input("> ")
        if user_input != "exit":
            print(ui.command(user_input))

    if ui.get_current_user() != '':
        ui.command('logout')


if __name__ == '__main__':
    main()
