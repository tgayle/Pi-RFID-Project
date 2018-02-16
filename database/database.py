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


def add_script(rfid, script_name, type, script, on_finish_callback=None):

    reference = _get_identifier(script_name)

    _cursor.execute("SELECT * FROM 'references' WHERE script_reference=?", [reference])
    result = _cursor.fetchall()

    if len(result) > 0:
        print("The name '%s' is already taken and assigned to %s" % (script_name, rfid))
        return
    else:
        _cursor.execute("INSERT INTO '%s' (rfid_id, 'name', 'type', script_reference) VALUES (?, ?, ?, ?)"
                        % TABLE_SCRIPT_REFERENCE_NAME, (rfid, script_name, type, reference) )

        _cursor.execute("INSERT INTO %s (script_id, 'type', script) VALUES (?, ?, ?)"
                        % TABLE_SCRIPTS_NAME, (reference, type, script))
        _conn.commit()

        if on_finish_callback is not None:
            on_finish_callback()
            return


def get_script_for_card(uid):
    _cursor.execute("SELECT * FROM '%s' WHERE rfid_id=?" % TABLE_SCRIPT_REFERENCE_NAME, [uid])

    cursor_reference = _cursor.fetchone()

    if cursor_reference is None:
        return [None, None]

    _cursor.execute("SELECT type, script FROM %s WHERE script_id=?" % TABLE_SCRIPTS_NAME, [str(cursor_reference[3])])
    returned = _cursor.fetchone()

    return [returned[0], returned[1]]


def _get_identifier(obj):
    h = hash(obj)  # Convert object to a number for identification.
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


