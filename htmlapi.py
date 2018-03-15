import pico
from pico import PicoApp

import card_helper


@pico.expose()
def wait_for_card():
        card_helper.db.open_database()
        a, b = card_helper.wait_for_card()

        result = {
            "uid": a,
            "name": b
        }
        return result


@pico.expose()
def ping_for_card():
    card_helper.db.open_database()
    a, b = card_helper.wait_for_card_noblock()

    result = {
        "uid": a,
        "name": b
    }
    card_helper.db.close_database()
    return result


@pico.expose()
def get_card_name(uid):
    parsed_id = ""

    if len(uid.split()) > 4 or len(uid.split()) == 1:
        for i in range(len(uid)):
            if i % 2 == 0:
                parsed_id += " "
            parsed_id += uid[i]
        uid = parsed_id.strip()

    card_helper.db.open_database()
    name = card_helper.db.get_card_name(uid)
    card_helper.db.close_database()
    return {"uid": uid,
            "name": name}


@pico.expose()
def get_all_cards():
    card_helper.db.open_database()

    list_cards = card_helper.db.get_all_cardnames()
    response = []
    for card in list_cards:
        response.append({"uid": card[0],
                         "name": card[1]})

    card_helper.db.close_database()

    return {"cards": response}


@pico.expose()
def name_card(uid, name):
    card_helper.db.open_database()
    card_helper.name_card(uid, name)
    result = {"uid": uid,
              "name": card_helper.db.get_card_name(uid)}

    return json.dumps(result)


app = PicoApp()
app.register_module(__name__)
