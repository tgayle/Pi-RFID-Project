from database import database as db
from main import is_linux

yes_confirm_options = ["yes", "y"]

if is_linux:
    import nfc

    context = nfc.init()
    reader = nfc.list_devices(context, 2)[0]

    listener = nfc.open(context, reader)
    modulation = nfc.modulation()

    modulation.nmt = nfc.NMT_ISO14443A
    modulation.nbr = nfc.NBR_106


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


def name_card(card, name):
    confirm = "no"

    print("Are you sure that you want to name this card %s" % name)
    if confirm is not "yes" or confirm is not "y":
        print("Cancelled.")
        return

    db.name_card(card, name)

    return


def name_card_ask_for_name(card):
    name = raw_input("What would you like this card to be named? ")

    print("Are you sure that you want to name this card '%s'" % name)
    confirm = raw_input("Yes or No: ").strip().lower()
    print("confirm is %s " % confirm)
    if confirm not in yes_confirm_options:
        print("Cancelled.")
        return

    print("Nickname for %s is now %s" % (card, name))
    db.name_card(card, name)

