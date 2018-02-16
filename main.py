from platform import system
import card_helper

is_linux = system() == "Linux"


def write_file(string):
    with open("output.txt", "w") as f:
        f.write(string)
        f.write("\n#############################")
        print("Files written")


def print_options(options):
    for i, k in enumerate(options):
        print("%d: %s" % (i + 1, k[0]))


def select_from_options(options):
    print_options(options)
    print("")

    selected_item = int(input())

    while (selected_item > len(options)) or (selected_item < 0):
        print("Please select a valid option.")
        print_options()
        selected_item = int(input())
    return selected_item


def read_card():
    if is_linux:
        print("Please place an NFC device on the scanner.")
        print("")

        uid_found = card_helper.wait_for_card()
        card_name = card_helper.db.get_card_name(uid_found)

        if card_name is None:
            print("Device found: %s" % uid_found)
        else:
            print("Device found: %s (%s)" % (card_name, uid_found))
        print('')

    else:
        print("You must be on a linux device with a PN532 to do this.")
    return


def add_automation():
    return


def edit_card():
    print("Please place the card you'd like to edit on the scanner.")
    card_uid = card_helper.wait_for_card()
    card_name = card_helper.db.get_card_name(card_uid)

    if card_name is None:
        print("Settings for card: %s" % card_uid)
    else:
        print("Settings for card %s (%s)" % (card_name, card_uid))

    print("")
    print("What would you like to do?")

    opts = [["Give this card a name.", card_helper.name_card_ask_for_name]
            ]

    selected_item = select_from_options(opts)
    start_option(opts, selected_item - 1, parameters=card_uid)


main_options = [
    ["Read a card's id.", read_card],
    ["Add an automation to a card.", add_automation],
    ["Edit a card.", edit_card],
]


def start_option(options, i, parameters=None):
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

