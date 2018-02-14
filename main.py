from database import database as db
from platform import system

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
    #print("ID was %s" % uid)
    return uid


def start_option(i):
    options[i][1]()

def wait_for_card():
    # number_found, devices = nfc.initiator_list_passive_targets(listener, modulation, 16)

    while number_found < 1:
        number_found, devices = nfc.initiator_list_passive_targets(listener, modulation, 16)

    return get_nfc_uid(devices[0])

def read_card():
    if is_linux:
        print("Please place an NFC device on the scanner.")

        number_found, devices = nfc.initiator_list_passive_targets(listener, modulation, 16)

        while number_found < 1:
            number_found, devices = nfc.initiator_list_passive_targets(listener, modulation, 16)

        print()
        print("Devices found:")

        for n in range(number_found):
            num, string = nfc.str_nfc_target(devices[n], False)

            print("%d: %s" % (n + 1, get_nfc_uid(string)))
            print('\n################\n')

    else:
        print("You must be on a linux device with a PN532 to do this.")
    return

def add_automation():
    return

options = [
    ["Read a card's id.", read_card],
    ["Add an automation to a card.", add_automation],
    ]


if __name__ == "__main__":
    print("What would you like to do?")

    # print_options()
    #
    # selected_item = int(input())
    #
    # while (selected_item > len(options)) or (selected_item < 0):
    #     print("Please select a valid option.")
    #     print_options()
    #     selected_item = int(input())
    #
    # print("You selected: %s" % options[selected_item - 1][0])
    # start_option(selected_item-1)

    while True:
        read_card()

