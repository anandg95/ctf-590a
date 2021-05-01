from fastapi import FastAPI, Response, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import asyncio
import random
import os
import json

templates = Jinja2Templates(directory="templates")
app = FastAPI()

pass_key = str(random.randint(2000,7000))

current_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(current_dir, "flag.txt")) as f:
    flag = f.read()

# remove flag now
with open(os.path.join(current_dir, "details.json")) as f:
    details = json.loads(f.read())
if not details.get("persist_flag", False):
    os.remove(os.path.join(current_dir, "flag.txt"))


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


@app.post("/brute/login", response_class=HTMLResponse)
async def brute_login(key: str = Form(...)):
    key = key[:4]
    await asyncio.sleep(1)
    if key == pass_key:
        return Response(content=f"Match! Here is the flag - {flag}", status_code=200)
    else:
        return Response("Mismatch - cant give you the flag", status_code=400)


