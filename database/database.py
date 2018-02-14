import sqlite3
import sys

TABLE_SCRIPT_REFERENCE_NAME = "references"
COLUMN_RFID_ID = "rfid_id"
COLUMN_SCRIPT_NAME = "name"
COLUMN_SCRIPT_TYPE = "type"
COLUMN_SCRIPT_REFERENCE = "script_reference"

TABLE_SCRIPTS_NAME = "scripts"
COLUMN_SCRIPT_ID = "script_id"
COLUMN_SCRIPT = "script"


CREATE_REFERENCES_TABLE = '''CREATE TABLE IF NOT EXISTS '%s' (%s TEXT, %s TEXT, %s TEXT, %s LONG)''' \
                       % (TABLE_SCRIPT_REFERENCE_NAME, COLUMN_RFID_ID, COLUMN_SCRIPT_NAME, COLUMN_SCRIPT_TYPE, COLUMN_SCRIPT_REFERENCE)

CREATE_SCRIPTS_TABLE = '''CREATE TABLE IF NOT EXISTS %s (%s TEXT, %s TEXT, %s TEXT)'''\
                       % (TABLE_SCRIPTS_NAME, COLUMN_SCRIPT_ID, COLUMN_SCRIPT_TYPE, COLUMN_SCRIPT)

_conn = sqlite3.connect("scripts.db")

_cursor = _conn.cursor()

_cursor.execute(CREATE_REFERENCES_TABLE)
_cursor.execute(CREATE_SCRIPTS_TABLE)

def close_database():
    _cursor.close()
    _conn.close()

def add_script(rfid, script_name, type, on_success_callback, on_failure_callback):

    reference = _get_identifier(script_name)
    print("id for %s is %s" % (script_name, reference))

    _cursor.execute("SELECT * FROM 'references' WHERE script_reference=?", [reference])
    print(_cursor.fetchall().__str__())
    result = _cursor.fetchone()
    print(result)

    if result is None:
        print("Script %s already exists and is assigned to %s" % (script_name, rfid))

    else:
        _cursor.execute("INSERT INTO '%s' (rfid_id, name, type, script_reference) VALUES (?, ?, ?, ?)"
                        % TABLE_SCRIPT_REFERENCE_NAME, (rfid, script_name, type, reference) )
        _conn.commit()

        print("Added a script.")


def _get_identifier(object):
    h = hash(object)
    if h < 0:
        h += sys.maxsize

    return h


if __name__ == "__main__":
    add_script("testrfid", "Script 1", "PRINT")

    close_database()
