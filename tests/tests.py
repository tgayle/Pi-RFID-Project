from database import database as db

"""
Module for testing additions and changes.
"""

db.open_database()


def test_success_callback():
    print("Success!")


def test_failure_callback():
    print("Failure.")


def test_naming_cards():
    testcards = [
        ["de vi ce 01", "Name 1"],
        ["de vi ce 02", "Name 2"],
        ["de vi ce 03", "Name 3"]
    ]

    for li in testcards:
        db.name_card_db(li[0], li[1])

    print("All cards:")
    for card in db.get_all_cardnames():
        print("%s -> %s" % (card[0], card[1]))

    print("card name for abcdef is %s" % db.get_card_name("abcdef"))


db.close_database()