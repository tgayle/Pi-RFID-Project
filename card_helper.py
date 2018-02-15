from database import database as db


def name_card(card, name):
    confirm = "no"

    print("Are you sure that you want to name this card %s" % name)
    if confirm is not "yes" or confirm is not "y":
        print("Cancelled.")
        return

    db.name_card(card, name)

    return

def name_card_ask_for_name(card):
    name = input("What would you like this card to be named? ")

    print("Are you sure that you want to name this card '%s'" % name)
    confirm = input("Yes or No: ")

    if confirm is not "yes" or confirm is not "y":
        print("Cancelled.")
        return

    db.name_card(card, name)

