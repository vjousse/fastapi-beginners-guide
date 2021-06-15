# main.py
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/public", StaticFiles(directory="public"), name="public")

templates = Jinja2Templates(directory="templates")

@app.get("/health")
async def health():
    return {"message": "I'm alive"}

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
