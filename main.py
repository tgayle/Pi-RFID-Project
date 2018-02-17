import card_helper


def print_options(options):
    """
    Prints items with numbers from 1 to len(options)
    :param options: An array of possible options formatted as [option_name, related_function_to_call]
    :return: None
    """
    for i, k in enumerate(options):
        print("%d: %s" % (i + 1, k[0]))


def select_from_options(options):
    """
    Print items with numbers from 1 to len(options) and asks the user to select a number
    :param options: An array of possible options formatted as [option_name, related_function_to_call]
    :return: the number selected by the user.
    """
    print_options(options)
    print("")

    selected_item = int(input())

    while (selected_item > len(options)) or (selected_item < 0):
        print("Please select a valid option.")
        print_options(options)
        selected_item = int(input())
    return selected_item


def read_card():
    """
    Option for user to select. Reads card and prints name.
    :return: None
    """
    if card_helper.is_linux:
        print("Please place an NFC device on the scanner.")
        print("")

        uid_found, card_name = card_helper.wait_for_card()

        if card_name is None:
            print("Device found: %s" % uid_found)
        else:
            print("Device found: %s (%s)" % (card_name, uid_found))
        print('')

    else:
        print("You must be on a linux device with a PN532 to do this.")
    return


def edit_card():
    """
    Provide extra options to a card such as changing name after scanning a card.
    :return: None
    """

    opt_give_card_name = "Give this card a name."

    print("Please place the card you'd like to edit on the scanner.")
    card_uid, card_name = card_helper.wait_for_card()

    if card_name is None:
        print("Settings for card: %s" % card_uid)
    else:
        print("Settings for card %s (%s)" % (card_name, card_uid))
        opt_give_card_name = "Rename this card."

    print("")
    print("What would you like to do?")

    opts = [[opt_give_card_name, card_helper.name_card_ask_for_name]
            ]

    selected_item = select_from_options(opts)
    start_option(opts, selected_item - 1, parameters=card_uid)
    return


def add_automation():
    """
    Adds an automation to a card. May be PRINT, "PYSCR", or "BSHSCR" (print, python script, or bash script)
    :return: None
    """
    print("Place the card you'd like to edit on the scanner.")

    uid, name = card_helper.wait_for_card()

    if name is None:
        print("Card selected: %s" % uid)
    else:
        print("Card selected: %s (%s)" % (name, uid))

    print("")
    print("What would you like this card to do?")
    automation_options = [
        ["Print a message", card_helper.add_automation_printmessage]
    ]

    selection = select_from_options(automation_options)
    start_option(automation_options, selection - 1, parameters=uid)


def execute_automation():
    """
    Runs the automation assigned to a card if available.
    :return: None
    """
    print("Place the card you'd like to execute on the scanner.")

    uid, name = card_helper.wait_for_card()

    script_type, script = card_helper.db.get_script_for_card(uid)

    if script is None or script_type is None:
        if name is None:
            print("There was no automation assigned to %s" % uid)
        else:
            print("There was no automation assigned to %s (%s)" % (name, uid))
        return

    if script_type == "PRINT":
        print(script)
    else:
        print("This type isn't implemented yet. (%s)" % script_type)


def list_cards():
    """
    Prints all the cards currently added to the DB with a nickname.
    :return: None
    """
    cards = card_helper.db.get_all_cardnames()

    for i, c in enumerate(cards):
        print("%d: %s (%s)" % (i + 1, c[0], c[1]))


main_options = [
    ["Read a card's id.", read_card],
    ["Add an automation to a card.", add_automation],
    ["Execute a card's automation.", execute_automation],
    ["Edit a card.", edit_card],
    ["List all added cards.", list_cards]
]


def start_option(options, i, parameters=None):
    """
    Starts an option out of an options array.
    Each item in the options array should be in format [option_name, option_func]
    :param options: An array of options formatted as detailed above.
    :param i: The index of the option to start.
    :param parameters: Optional. Used for passing in arguments to a function called through start_option.
    :return: None
    """
    if parameters is None:
        options[i][1]()
    else:
        options[i][1](parameters)


if __name__ == "__main__":
    card_helper.db.open_database()

    print("What would you like to do?")

    selected_item = select_from_options(main_options)

    print("You selected: %s" % main_options[selected_item - 1][0])
    start_option(main_options, selected_item-1)

    card_helper.db.close_database()

