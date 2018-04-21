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
    uid = card_helper.create_whitespace(uid)

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
    uid = card_helper.create_whitespace(uid)
    card_helper.db.open_database()
    card_helper.name_card(uid, name)
    result = {"uid": uid,
              "name": card_helper.db.get_card_name(uid)}
    card_helper.db.close_database()
    return result


@pico.expose()
def add_automation(uid, name, type, script):
  uid = card_helper.create_whitespace(uid)
  card_helper.db.open_database()
  card_helper.db.add_script(uid, name, type, script)
  db_name, db_type, db_script = card_helper.db.get_script_for_card(uid)
  card_helper.db.close_database()
  return {
    'uid': uid,
    'name': db_name,
    'type': db_type,
    'script': db_script
  }


@pico.expose()
def add_automation_html(uid, name, type, url, data):
  uid = card_helper.create_whitespace(uid)
  if type == "POST":
    script_into_db = "POST\n"
  else:
    script_into_db = "GET\n"
  script_into_db += url + "\n"
  script_into_db += data

  card_helper.db.open_database()
  card_helper.db.add_script(uid, name, "HTMLREQ", script_into_db)
  db_name, db_type, db_script = card_helper.db.get_script_for_card(uid)
  card_helper.db.close_database()
  return {
    'uid': uid,
    'name': db_name,
    'type': db_type,
    'script': db_script
  }


@pico.expose()
def execute_automation(uid):
  uid = card_helper.create_whitespace(uid)
  card_helper.db.open_database()
  name, type, script = card_helper.db.get_script_for_card(uid)
  card_helper.db.close_database()
  if type == "PRINT":
    automation_result = script
  elif type == "PYTHON":
    automation_result = card_helper.run_automation(script)
  elif type == "HTMLREQ":
    method, url, data = card_helper.parse_html_request(script)
    automation_result = card_helper.html_request(method=method, url=url, data=data)
  else:
    automation_result = type

  return {
    "name": name,
    "type": type,
    "script": script,
    "result": automation_result
  }


app = PicoApp()
app.register_module(__name__)
