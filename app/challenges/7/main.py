from fastapi import FastAPI, Header
from fastapi.responses import PlainTextResponse
from typing import Optional

app = FastAPI()

with open("flag.txt") as f:
    flag = f.read()


@app.get("/", response_class=PlainTextResponse)
def home(user_agent: Optional[str] = Header(None)):
    if user_agent is None:
        user_agent = ""
    if "msie 2.0" in user_agent.lower():
        return flag
    else:
        return "I only respond to requests from Internet Explorer 2.0"