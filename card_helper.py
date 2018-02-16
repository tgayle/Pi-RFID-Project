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

    uid = get_nfc_uid(devices[0])
    return [uid, db.get_card_name(uid)]


def name_card(card, name):
    confirm = "no"

    print("Are you sure that you want to name this card %s" % name)
    if confirm is not "yes" or confirm is not "y":
        print("Cancelled.")
        return

    db.name_card(card, name)


def name_card_ask_for_name(card):
    name = raw_input("What would you like this card to be named? ")

    print("Are you sure that you want to name this card '%s'" % name)


    print("Nickname for %s is now %s" % (card, name))
    db.name_card(card, name)


def add_automation_printmessage(card):
    automation_name = raw_input("What would you like to name this automation?: ")

    print("What would you like this card to print when activated?")
    message = raw_input()
    print("Are you sure you'd like this card to print the following message when activated?: ")
    print('""')
    print(message)
    print(",,")

    print("Yes or No?")
    if not confirm_selection():
        print("Cancelled.")
        return

    def on_finish():
        print("Automation %s was successfully assigned to %s" % (automation_name, card))

    db.add_script(card, automation_name, "PRINT", message, on_finish_callback=on_finish)


def confirm_selection():
    confirm = raw_input().strip().lower()
    if confirm not in yes_confirm_options:
        return False

    return True
