from database import database as db
from platform import system
import card_helper

is_linux = system() == "Linux"

if is_linux:  # Prepare NFC reader for later use.
    import nfc


    context = nfc.init()
    reader = nfc.list_devices(context, 2)[0]

    listener = nfc.open(context, reader)
    modulation = nfc.modulation()

    modulation.nmt = nfc.NMT_ISO14443A
    modulation.nbr = nfc.NBR_106




def write_file(string):
    with open("output.txt", "w") as f:
        f.write(string)
        f.write("\n#############################")
        print("Files written")


def print_options():
    for i, k in enumerate(options):
        print("%d: %s" % (i + 1, k[0]))

def get_nfc_uid(device):
    num, string = nfc.str_nfc_target(device, False)
    str_list = string.split("\n")
    uid = str_list[2].strip().replace("  ", " ")
    uid = uid[uid.index(": ") + 2:]
    return uid


def wait_for_card():
    number_found, devices = nfc.initiator_list_passive_targets(listener, modulation, 16)
    while number_found < 1:
        number_found, devices = nfc.initiator_list_passive_targets(listener, modulation, 16)

    return get_nfc_uid(devices[0])

def read_card():
    if is_linux:
        print("Please place an NFC device on the scanner.")
        print("")

        uid_found = wait_for_card()

        print("Device found: %s" % uid_found)
        print('')

    else:
        print("You must be on a linux device with a PN532 to do this.")
    return

def add_automation():
    return

def edit_card():
    print("Please place the card you'd like to edit on the scanner.")
    card = wait_for_card()

    print("Settings for card %s" % card)
    print("")
    print("What would you like to do?")

    opts = [["Give this card a name.", card_helper.name_card]
            ]

    for i, k in enumerate(opts):
        print("%d: %s" % (i + 1, k[0]))

options = [
    ["Read a card's id.", read_card],
    ["Add an automation to a card.", add_automation],
    ["Edit a card.", edit_card],
]

def start_option(i):
    options[i][1]()


if __name__ == "__main__":
    db.open_database()

    print("What would you like to do?")

    print_options()

    selected_item = int(input())

    while (selected_item > len(options)) or (selected_item < 0):
        print("Please select a valid option.")
        print_options()
        selected_item = int(input())

    print("You selected: %s" % options[selected_item - 1][0])
    start_option(selected_item-1)

    db.close_database()
    print("end program")

