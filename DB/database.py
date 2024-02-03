import sqlite3 as sq


db = sq.connect('db/bot.db')
cur = db.cursor()

async def db_start():
    cur.execute("CREATE TABLE IF NOT EXISTS exes("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "tg_id TEXT, "
                "username TEXT, "
                "exercise TEXT, "
                "weight FLOAT)")
    db.commit()


# async def cmd_db_start(user_id, user_firstname):
#     user = cur.execute("SELECT * FROM exes WHERE tg_id == ?", (user_id,)).fetchone()
#     if not user:
#         cur.execute("INSERT INTO exes (tg_id, username) VALUES (?, ?)", (user_id, user_firstname))
#         db.commit()


async def add_weight(user_id, user_firstname, exercise, weight):
    ex_check = cur.execute("SELECT * FROM exes WHERE tg_id == ? AND exercise == ?", (user_id, exercise)).fetchone()
    if ex_check:
        cur.execute("UPDATE exes SET weight = ? WHERE tg_id == ? AND exercise == ?", (weight, user_id, exercise))
        db.commit()
    else:
        cur.execute("INSERT INTO exes (tg_id, username, exercise, weight) VALUES (?, ?, ?, ?)", (user_id, user_firstname, exercise, weight))
        db.commit()


async def list_exes(user_id):
    ex_list = cur.execute("SELECT exercise FROM exes WHERE tg_id == ?", (user_id,)).fetchall()
    return [item[0] for item in ex_list]


async def current_weight(user_id, exercise):
    weight = cur.execute("SELECT weight FROM exes WHERE tg_id == ? AND exercise == ?", (user_id, exercise)).fetchone()
    return weight
