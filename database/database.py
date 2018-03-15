import sqlite3
import threading
from sys import maxsize

_TABLE_SCRIPT_REFERENCE_NAME = "references"
_COLUMN_RFID_ID = "rfid_id"
_COLUMN_SCRIPT_NAME = "name"
_COLUMN_SCRIPT_TYPE = "type"
_COLUMN_SCRIPT_REFERENCE = "script_reference"

_TABLE_SCRIPTS_NAME = "scripts"
_COLUMN_SCRIPT_ID = "script_id"
_COLUMN_SCRIPT = "script"

_TABLE_CARD_NICKNAMES_NAME = "cards"

_CREATE_REFERENCES_TABLE = '''CREATE TABLE IF NOT EXISTS '%s' (%s TEXT, '%s' TEXT, '%s' TEXT, %s LONG)''' \
                       % (_TABLE_SCRIPT_REFERENCE_NAME, _COLUMN_RFID_ID, _COLUMN_SCRIPT_NAME, _COLUMN_SCRIPT_TYPE, _COLUMN_SCRIPT_REFERENCE)

_CREATE_SCRIPTS_TABLE = '''CREATE TABLE IF NOT EXISTS %s (%s TEXT, %s TEXT, %s TEXT)'''\
                       % (_TABLE_SCRIPTS_NAME, _COLUMN_SCRIPT_ID, _COLUMN_SCRIPT_TYPE, _COLUMN_SCRIPT)

_CREATE_CARDS_NAMES_LIST_TABLE = "CREATE TABLE IF NOT EXISTS %s (uid TEXT, nickname TEXT)" % _TABLE_CARD_NICKNAMES_NAME

_conn = None
_cursor = None
lock = threading.Lock()  # Create a lock to prevent multiple cursors when requests come.

def open_database():
    """
    Opens and prepares database.
    :return: None
    """
    lock.acquire(True)
    global _conn
    global _cursor

    _conn = sqlite3.connect("scripts.db")

    _cursor = _conn.cursor()

    _cursor.execute(_CREATE_REFERENCES_TABLE)
    _cursor.execute(_CREATE_SCRIPTS_TABLE)
    _cursor.execute(_CREATE_CARDS_NAMES_LIST_TABLE)
    lock.release()

def close_database():
    """
    Saves all changes to database, then closes cursors and connections to it.
    :return:
    """
    _conn.commit()
    _cursor.close()
    _conn.close()


def add_script(rfid, script_name, type, script, on_finish_callback=None):
    """

    :param rfid: An NFC/RFID card's identifier. An 8 character id separated ever 2 characters for a total of 11 chars.
    :param script_name: The selected name to identify the script.
    :param type: The type of script this is.
    :param script: The script itself. if the type is "PRINT" then this is just the message to print itself.
    :param on_finish_callback: A optional function that may be passed in to let the calling module know when this is
    completed
    :return: None.
    """
    lock.acquire(True)
    reference = _get_identifier(script_name)

    _cursor.execute("SELECT * FROM 'references' WHERE script_reference=?", [reference])
    result = _cursor.fetchall()

    if len(result) > 0:
        card_name = get_card_name(rfid);
        if card_name is None:
            print("The name '%s' is already taken and assigned to %s" % (script_name, rfid))
        else:
            print("The name '%s' is already taken and assigned to %s (%s)" % (script_name, card_name, rfid))
        return

    else:
        _cursor.execute("INSERT INTO '%s' (rfid_id, 'name', 'type', script_reference) VALUES (?, ?, ?, ?)"
                        % _TABLE_SCRIPT_REFERENCE_NAME, (rfid, script_name, type, reference))

        _cursor.execute("INSERT INTO %s (script_id, 'type', script) VALUES (?, ?, ?)"
                        % _TABLE_SCRIPTS_NAME, (reference, type, script))
        _conn.commit()
        lock.release()

        if on_finish_callback is not None:
            on_finish_callback()
            return


def get_script_for_card(uid):
    """

    :param uid: The uid for an NFC/RFID Device
    :return: tuple of 2:
    str: The type of script it was.
    str: The script itself. This will be a path if it is a bash script.

    Returns [None, None] if script is assigned to a card.
    """
    lock.acquire(True)
    _cursor.execute("SELECT * FROM '%s' WHERE rfid_id=?" % _TABLE_SCRIPT_REFERENCE_NAME, [uid])

    cursor_reference = _cursor.fetchone()

    if cursor_reference is None:
        return [None, None]

    _cursor.execute("SELECT type, script FROM %s WHERE script_id=?" % _TABLE_SCRIPTS_NAME, [str(cursor_reference[3])])
    returned = _cursor.fetchone()
    lock.release()
    return [returned[0], returned[1]]


def _get_identifier(obj):
    """
    Returns a number > 0 that can be used for identifying objects.
    :param obj: The object to find the identifier for.
    :return: a number > 0 that is pseudo-unique to the given object.
    """
    h = hash(obj)  # Convert object to a number for identification.
    if h < 0:
        h += maxsize
        # Using the hash function can sometimes return a negative number,
        # so we add sys.maxsize to make sure it's always a positive number.

    return h


def name_card_db(uid, name):
    """
    Assigns a name to an RFID and stores it in the database.
    :param uid: RFID to assign name to.
    :param name: The selected name that will be assigned to the RFID
    :return: None
    """
    lock.acquire(True)
    _cursor.execute("SELECT * FROM %s WHERE uid=?" % _TABLE_CARD_NICKNAMES_NAME, [uid])

    if len(_cursor.fetchall()) > 0:
        _cursor.execute("UPDATE %s SET uid=?, nickname=? WHERE uid=?" % _TABLE_CARD_NICKNAMES_NAME, (uid, name, uid))
    else:
        _cursor.execute("INSERT INTO %s (uid, nickname) VALUES (?, ?)" % _TABLE_CARD_NICKNAMES_NAME, (uid, name))
    _conn.commit()
    lock.release()
    return


def get_card_name(uid):
    """
    Returns the name of an RFID if there is one within the database.
    :param uid: RFID to find the name for.
    :return: None or str
    str: The name assigned to the given RFID.
    None: If there is no name assigned to this RFID, then return None.
    """
    lock.acquire(True)
    _cursor.execute("SELECT nickname from %s WHERE uid=?" % _TABLE_CARD_NICKNAMES_NAME, [uid])
    db_result = _cursor.fetchone()
    lock.release()
    if db_result is None:
        return None
    else:
        return db_result[0]


def get_all_cardnames():
    """
    Returns a list of all cards with their ID and name.
    :return: A list of all cards that have also been named. Each index in the array is formatted as [RFID, nickname]
    """
    lock.acquire(True)
    _cursor.execute("SELECT * from %s" % _TABLE_CARD_NICKNAMES_NAME)
    cards = _cursor.fetchall()

    for i in range(len(cards)):
        cards[i] = [str(cards[i][0]), str(cards[i][1])]
    lock.release()
    return cards


