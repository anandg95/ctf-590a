import sqlite3
from backend.challenge_register import create_flags, start_challenge_services, fetch_details # only to be called in this order

def conn_factory():
    return sqlite3.connect("app_db.sqlite3")

conn = conn_factory()

table_name = "challenge"
db_flags = {}
try:
    for id, flag in conn.execute(f"SELECT id, flag from {table_name}").fetchall():
        db_flags[str(id)] = flag
except sqlite3.Error:
    pass

# create table if not exists
exists_table = conn.execute(f"SELECT name FROM sqlite_master WHERE name='{table_name}'").fetchone() is not None
if not exists_table:
    with conn:
        conn.execute(
            f"""
            CREATE TABLE {table_name} (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, flag TEXT, hint TEXT, answered INT)
            """
        )
        
create_flags(db_flags)
start_challenge_services()
all_challenges, all_static = fetch_details()

# create challenge entries if not exists
for challenge in all_challenges:
    exists = conn.execute(f"SELECT * FROM {table_name} WHERE id={challenge['id']}").fetchone() is not None
    if not exists:
        conn = conn_factory()
        with conn:
            command = f"""
                INSERT INTO {table_name} (id, name, description, hint, flag, answered) VALUES ('{challenge["id"]}', '{challenge["name"]}', 
                '{challenge["description"]}', '{challenge["hint"]}', '{challenge["flag"]}', 0)
                """
            conn.execute(command)




def verify(challenge_id, submitted_flag):
    conn = conn_factory()
    real_flag = conn.execute(f"SELECT flag from {table_name} where id=?", (challenge_id,)).fetchone()[0]
    if real_flag == submitted_flag:
        with conn:
            conn.execute(f"UPDATE {table_name} SET answered=1 where id=?", (challenge_id,))
        return True
    else:
        return False


def status():
    "Answer status of all challenges - mapping from id to (bool, flag)"
    conn = conn_factory()
    return {id: flag if bool(answered) else "Enter flag here" for id, answered, flag in conn.execute(f"SELECT id, answered, flag from {table_name}").fetchall()}

def uncheck_all():
    conn = conn_factory()
    with conn:
        conn.execute(f"UPDATE {table_name} SET answered=0")
    