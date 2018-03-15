from database import database as db
from platform import system

is_linux = (system() == "Linux")
yes_confirm_options = ["yes", "y"]

if is_linux:
    """
    Determine if the device this is running on is a linux device and if so, attempt to import necessary nfc modules
    and prepare for later use of the reader.
    """
    import nfc

    context = nfc.init()
    reader = nfc.list_devices(context, 2)[0]

    listener = nfc.open(context, reader)
    modulation = nfc.modulation()

    modulation.nmt = nfc.NMT_ISO14443A
    modulation.nbr = nfc.NBR_106


def parse_nfc_uid(device):
    """
    Parses from the string returned from nfc.str_nfc_target and just returns the uid.
    :param device: An object of the card class from nfc's implementation. Get this from initiator_list_passive_targets
    :return: The uid of the given object.
    """
    num, string = nfc.str_nfc_target(device, False)
    str_list = string.split("\n")
    uid = str_list[2].strip().replace("  ", " ")
    uid = uid[uid.index(": ") + 2:]
    return uid


def wait_for_card():
    """
    Blocks and waits until an NFC device is found by the reader.
    :return: A tuple with the uid found and it's name if available. Name will be None if there is none.
    [uid, card_name]
    """
    number_found, devices = nfc.initiator_list_passive_targets(listener, modulation, 1)
    while number_found < 1:
        number_found, devices = nfc.initiator_list_passive_targets(listener, modulation, 1)

    uid = parse_nfc_uid(devices[0])
    return [uid, db.get_card_name(uid)]


def wait_for_card_noblock():
    """
    Pings for an NFC device. If one isn't found on the scanner at the moment this is called then [None, None]
    is returned.
    :return: Tuple. [uid, card_name] if device found, else [None, None]
    """
    number_found, devices = nfc.initiator_list_passive_targets(listener, modulation, 1)

    try:
        uid = parse_nfc_uid(devices[0])
    except:
        return [None, None]

    return [uid, db.get_card_name(uid)]


def name_card(card, name):
    """
    Assign a name to card and store it in DB
    :param card: The card uid to assign to
    :param name: The name to be assigned to the card.
    :return: None
    """
    db.name_card_db(card, name)


def name_card_ask_for_name(card):
    """
    Ask the user for a name to assign to a card and store it in DB
    :param card: The card uid to assign to
    :return: None
    """

    name = raw_input("What would you like this card to be named? ")

    print("Are you sure that you want to name this card '%s'" % name)

    print("Yes or No?")
    if not confirm_selection():
        print("Cancelled.")
        return

    print("Nickname for %s is now %s" % (card, name))
    db.name_card_db(card, name)


def add_automation_printmessage(card):
    """
    Add an automation to a card that will print a message when activated. Asks user for message to print.
    :param card: Card uid to add automation to.
    :return: None
    """
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
    """
    Waits for user to input something that qualifies as a 'yes', such as "yes' or "y"
    :return: True if the input was something that counts as yes, else False.
    """
    confirm = raw_input().strip().lower()
    if confirm not in yes_confirm_options:
        return False

    return True
