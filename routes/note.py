from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from bson import ObjectId
from hashlib import sha256

from models.note import Note
from config.db import conn
from schemas.note import note_schema, notes
from decouple import AutoConfig
from fastapi.security import APIKeyHeader

# Load environment variables
config = AutoConfig(search_path=".")

API_KEYS = set(config("API_KEYS", default="").split(","))

# Scheme for API Key header (default: `X-API-Key`)
api_key_header = APIKeyHeader(name="X-API-Key")

# Dependency to validate API key
async def validate_api_key(api_key: str = Depends(api_key_header)):
    if api_key not in API_KEYS:
        raise HTTPException(
            status_code=403,
            detail="Invalid API Key. Access denied."
        )
    return api_key

note_router = APIRouter()

templates = Jinja2Templates(directory="templates")

# Helper function to hash passwords
def hash_password(password: str) -> str:
    return sha256(password.encode()).hexdigest()

# Middleware to check if user is logged in
def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        return None
    return user

@note_router.get("/signup", response_class=HTMLResponse)
async def signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@note_router.post("/signup", response_class=HTMLResponse)
async def signup(request: Request, username: str = Form(...), password: str = Form(...), confirm_password: str = Form(...), email: str = Form(...)):
    form = await request.form()
    print(username, email, password, confirm_password)
    if password != confirm_password:
        return templates.TemplateResponse("signup.html", {"request": request, "error": "Passwords do not match"})
    if len(password) < 6:
        return templates.TemplateResponse("signup.html", {"request": request, "error": "Password must be at least 6 characters long"})
    if len(username) < 3:
        return templates.TemplateResponse("signup.html", {"request": request, "error": "Username must be at least 3 characters long"})
    if len(email) < 5:
        return templates.TemplateResponse("signup.html", {"request": request, "error": "Email must be at least 5 characters long"})
    
    hashed_password = hash_password(password)
    existing_user = conn.notes.users.find_one({"username": username})
    if existing_user:
        return templates.TemplateResponse("signup.html", {"request": request, "error": "Username already exists"})
    conn.notes.users.insert_one({"username": username, "email": email, "password": hashed_password})
    return RedirectResponse(url="/login", status_code=302)

@note_router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@note_router.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    hashed_password = hash_password(password)
    user = conn.notes.users.find_one({"username": username, "password": hashed_password})
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    request.session["user"] = {"username": username, "id": str(user["_id"])}
    return RedirectResponse(url="/notes", status_code=302)

@note_router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=302)

@note_router.get("/", response_class=HTMLResponse)
async def note_form(request: Request, user: dict = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

@note_router.get("/notes", response_class=HTMLResponse)
async def all_items(request: Request, user: dict = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    docs = conn.notes.notes.find({"user_id": user["id"]})
    docs_list = list(docs)
    return templates.TemplateResponse("notes.html", {"request": request, "notes": reversed(docs_list), "length": len(docs_list), "user": user})

@note_router.post("/", response_class=HTMLResponse)
async def add_note(request: Request, user: dict = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    form = await request.form()
    inserted_note = conn.notes.notes.insert_one({
        "title": form["title"],
        "note": form["note"],
        "important": True if form.get("important") == "on" else False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": user["id"]
    })
    status = inserted_note.acknowledged
    docs = conn.notes.notes.find({"user_id": user["id"]})
    docs_list = list(docs)
    return templates.TemplateResponse("notes.html", {"request": request, "notes": reversed(docs_list), "status": status, "user": user})

@note_router.put("/update", response_class=JSONResponse)
async def update_note(request: Request):
    try:
        form = await request.json()  # Parse JSON data from the request body
        note_id = form.get("id")
        # print(form)
        if not note_id:
            return {"status": "error", "message": "Note ID is required"}

        updated_data = {
            "title": form.get("title"),
            "note": form.get("note"),
            "important": form.get("important", False),
        }

        # Remove None values from the update data
        updated_data = {k: v for k, v in updated_data.items() if v is not None}

        result = conn.notes.notes.update_one(
            {"_id": ObjectId(note_id)}, {"$set": updated_data}
        )
        # print(result)

        if result.matched_count == 0:
            return {"status": "error", "message": "Note not found"}
        docs = conn.notes.notes.find({})
        docs_list = list(docs)
        return {"status": "success", "message": "Note updated successfully!", "note_count": len(docs_list)}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

@note_router.delete("/delete", response_class=JSONResponse)
async def delete_note(request: Request):
    try:
        form = await request.json()  # Parse JSON body
        id = form.get("id")
        if not id:
            return {"status": "error", "message": "Note ID is required"}
        conn.notes.notes.delete_one({"_id": ObjectId(id)})
        docs = conn.notes.notes.find({})
        docs_list = list(docs)
        return {"status": "success", "message": "Note deleted successfully!", "note_count": len(docs_list)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@note_router.get("/details/{id}", response_class=JSONResponse)
async def note_details(request: Request, id: str, user: dict = Depends(get_current_user), api_key: str = Depends(validate_api_key)):
    try:
        note_id = ObjectId(id)  # Ensure the ID is converted to ObjectId
        note = conn.notes.notes.find_one({"_id": note_id})
        if note:
            # Convert ObjectId to string for JSON serialization
            note["_id"] = str(note["_id"])
            return {"status": "success", "note": note}
        else:
            return {"status": "error", "message": "Note not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
