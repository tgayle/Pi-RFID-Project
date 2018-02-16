from database import database as db

db.open_database()


def test_success_callback():
    print("Success!")


def test_failure_callback():
    print("Failure.")


def test_naming_cards():
    testcards = [
        ["asdfasd", "nme 1"],
        ["asdfopwe", "nme2"],
        ["ae ef bc de", "nme3"]
    ]

    for li in testcards:
        db.name_card(li[0], li[1])

    print("All cards:")
    for card in db.get_all_cardnames():
        print("%s -> %s" % (card[0], card[1]))

    print("card name for abcdef is %s" % db.get_card_name("abcdef"))


db.close_database()