from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from routes.note import note_router
from starlette.middleware.sessions import SessionMiddleware
from decouple import AutoConfig
from fastapi.security import APIKeyHeader

# Load environment variables
config = AutoConfig(search_path=".")
SESSION_KEY = config("SESSION_KEY", default="")

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_KEY,  # Replace with a strong secret key
    # Optional: configure session parameters like max_age, same_site, https_only, etc.
    max_age=3600,  # Session expires after 1 hour
    same_site="lax",  # SameSite cookie attribute
    https_only=False,  # Set to True if using HTTPS
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(note_router)
