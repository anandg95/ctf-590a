from fastapi import FastAPI, Form, Request
import sqlite3
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# delete db if exists
try:
    os.remove("db.sqlite3")
except FileNotFoundError:
    pass

with open("flag.txt") as f:
    flag = f.read()

os.remove("flag.txt")


con = sqlite3.connect('db.sqlite3')

with con:
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS user (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT, password TEXT, flag TEXT)
        """
    )
    con.execute("INSERT INTO user (name, password, flag) VALUES ('labuser', 'dfec82e77aa2', 'N/A')")
    con.execute("INSERT INTO user (name, password, flag) VALUES ('georgia', '097acd76e11d', 'N/A')")
    con.execute(f"INSERT INTO user (name, password, flag) VALUES ('admin', 'ddb65e4512d', '{flag}')")


@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    con = sqlite3.connect("db.sqlite3")
    statement = f"SELECT * from user WHERE (name='{username}') AND (password='{password}') LIMIT 1 OFFSET 0;"

    try:
        d = con.execute(statement).fetchone()
    except sqlite3.Error as e:
        return f"Error! in SQL --> {statement}"

    if not d:
        return "Wrong Credentials"
    return f"(id, name, password, flag), {d}"

@app.get('/')
def landing(request: Request):
    return templates.TemplateResponse("login.html", context={"request": request})