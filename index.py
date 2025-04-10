from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.note import note_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(note_router)
