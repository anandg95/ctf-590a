from fastapi import FastAPI, Request, Response, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import backend.db as db
from backend import config

app = FastAPI()

templates = Jinja2Templates(directory="template")


# preprocess
for challenge_id, x in db.all_static.items():
    for filename, filepath in x.items():
        db.all_static[challenge_id][filename] = (filepath, f"http://localhost:{config.app_port}/static/{challenge_id}/{filename}")


@app.post("/submit")
def verify_submission( request: Request, id: int = Form(...), submitted_flag: str = Form(...)):
    correct =  db.verify(id, submitted_flag)
    return templates.TemplateResponse("index.html", context={"request": request, "status": db.status(), "all_challenges": db.all_challenges, "all_static": db.all_static})



@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request, "status": db.status(), "all_challenges": db.all_challenges, "all_static": db.all_static})


@app.get("/static/{challenge_id}/{filename}")
def get_static_file(challenge_id: int, filename: str):
    if filename in db.all_static.get(challenge_id, {}):
        return FileResponse(db.all_static[challenge_id][filename][0])

# developer API
@app.get("/uncheck")
def uncheck_all_answers():
    db.uncheck_all()
