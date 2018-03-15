from database import database as db
import card_helper
#from timeout import timeout, TimeoutError

"""
Module for testing additions and changes.
"""


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

def splituid(uid):
    parsedID = ""

    for i in range(len(uid)):
        if i % 2 == 0:
            parsedID += " "
        parsedID += uid[i]
    return parsedID.strip()


def test_json_response():
    import json

    def create_json(dictionary):
        return json.dumps(dictionary)

    def name_card(uid, name):
        card_helper.db.open_database()
        card_helper.name_card(uid, name)
        result = {"uid": uid,
                  "name": card_helper.db.get_card_name(uid)}

        return create_json(result)

    print(name_card("de vi ce 01", "Device uno"))


#@timeout(1)
def check_for_card():
    uid, name = card_helper.wait_for_card()
    return uid, name


if __name__ == "__main__":
    # try:
    #     db.open_database()
    #
    #     while True:
    #         try:
    #             uid, name = check_for_card()
    #             print("Found %s (%s)" % (uid, name))
    #         except TimeoutError:
    #             print("No card found...")
    #
    #
    # except KeyboardInterrupt:
    #     db.close_database()
    test_json_response()
    print(splituid("device01"))