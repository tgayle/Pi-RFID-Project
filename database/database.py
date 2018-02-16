import sqlite3
from sys import maxsize

TABLE_SCRIPT_REFERENCE_NAME = "references"
COLUMN_RFID_ID = "rfid_id"
COLUMN_SCRIPT_NAME = "name"
COLUMN_SCRIPT_TYPE = "type"
COLUMN_SCRIPT_REFERENCE = "script_reference"

TABLE_SCRIPTS_NAME = "scripts"
COLUMN_SCRIPT_ID = "script_id"
COLUMN_SCRIPT = "script"

TABLE_CARD_NICKNAMES_NAME = "cards"

CREATE_REFERENCES_TABLE = '''CREATE TABLE IF NOT EXISTS '%s' (%s TEXT, '%s' TEXT, '%s' TEXT, %s LONG)''' \
                       % (TABLE_SCRIPT_REFERENCE_NAME, COLUMN_RFID_ID, COLUMN_SCRIPT_NAME, COLUMN_SCRIPT_TYPE, COLUMN_SCRIPT_REFERENCE)

CREATE_SCRIPTS_TABLE = '''CREATE TABLE IF NOT EXISTS %s (%s TEXT, %s TEXT, %s TEXT)'''\
                       % (TABLE_SCRIPTS_NAME, COLUMN_SCRIPT_ID, COLUMN_SCRIPT_TYPE, COLUMN_SCRIPT)

CREATE_CARDS_NAMES_LIST_TABLE = "CREATE TABLE IF NOT EXISTS %s (uid TEXT, nickname TEXT)" % TABLE_CARD_NICKNAMES_NAME

_conn = None
_cursor = None


def open_database():
    global _conn
    global _cursor

    _conn = sqlite3.connect("scripts.db")

    _cursor = _conn.cursor()

    _cursor.execute(CREATE_REFERENCES_TABLE)
    _cursor.execute(CREATE_SCRIPTS_TABLE)
    _cursor.execute(CREATE_CARDS_NAMES_LIST_TABLE)


def close_database():
    _conn.commit()
    _cursor.close()
    _conn.close()


def add_script(rfid, script_name, type, on_success_callback, on_failure_callback):

    reference = _get_identifier(script_name)

    try:
        _cursor.execute("SELECT * FROM 'references' WHERE script_reference=?", [reference])
        result = _cursor.fetchall()
        print(result)

        if len(result) > 0:
            print("Script %s already exists and is assigned to %s" % (script_name, rfid))
            on_failure_callback()
            return
        else:
            _cursor.execute("INSERT INTO '%s' (rfid_id, 'name', 'type', script_reference) VALUES (?, ?, ?, ?)"
                            % TABLE_SCRIPT_REFERENCE_NAME, (rfid, script_name, type, reference) )
            _conn.commit()

            print("Added a script.")
            on_success_callback()
            return
    except:
        on_failure_callback()


def _get_identifier(object):
    h = hash(object) # Convert object to a number for identification.
    if h < 0:
        h += maxsize
        # Using the hash function can sometimes return a negative number,
        # so we add sys.maxsize to make sure it's always a positive number.

    return h


def name_card(uid, name):
    _cursor.execute("SELECT * FROM %s WHERE uid=?" % TABLE_CARD_NICKNAMES_NAME, [uid])

    if len(_cursor.fetchall()) > 0:
        _cursor.execute("UPDATE %s SET uid=?, nickname=? WHERE uid=?" % TABLE_CARD_NICKNAMES_NAME, (uid, name, uid))
    else:
        _cursor.execute("INSERT INTO %s (uid, nickname) VALUES (?, ?)" % TABLE_CARD_NICKNAMES_NAME, (uid, name))
    _conn.commit()
    return


def get_card_name(uid):
    _cursor.execute("SELECT nickname from %s WHERE uid=?" % TABLE_CARD_NICKNAMES_NAME, [uid])
    db_result = _cursor.fetchone()

    if db_result is None:
        return None
    else:
        return db_result[0]

def get_all_cardnames():
    _cursor.execute("SELECT * from %s" % TABLE_CARD_NICKNAMES_NAME)
    cards = _cursor.fetchall()

    for i in range(len(cards)):
        cards[i] = [str(cards[i][0]), str(cards[i][1])]

    return cards

def test_success_callback():
    print("Success!")


def test_failure_callback():
    print("Failure.")


if __name__ == "__main__":
    open_database()
    #add_script("testrfid", "Script 1", "PRINT", test_success_callback, failure_callback)
    testcard = "ae ef bc de"

    testcards = [
        ["asdfasd", "nme 1"],
        ["asdfopwe", "nme2"],
        [testcard, "nme3"]
    ]

    for li in testcards:
        name_card(li[0], li[1])

    print("All cards:")
    for card in get_all_cardnames():
        print("%s -> %s" % (card[0], card[1]))

    print("Card %s was nicknamed %s" % (testcard, get_card_name(testcard)))
    print("card name for abcdef is %s" % get_card_name("abcdef"))
    close_database()
