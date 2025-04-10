from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from bson import ObjectId

from models.note import Note
from config.db import conn
from schemas.note import note_schema, notes

note_router = APIRouter()

templates = Jinja2Templates(directory="templates")

@note_router.get("/", response_class=HTMLResponse)
async def note_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@note_router.get("/notes", response_class=HTMLResponse)
async def all_items(request: Request):
    # docs = conn.notes.notes.find_one({})
    docs = conn.notes.notes.find({})
    docs_list = list(docs)
    # print(docs_list)
    return templates.TemplateResponse("notes.html", {"request": request, "notes": reversed(docs_list), "length": len(docs_list)})

@note_router.post("/", response_class=HTMLResponse)
async def add_note(request: Request):
    form = await request.form()
    # print(form)
    inserted_note = conn.notes.notes.insert_one({
        "title": form["title"],
        "note": form["note"],
        "important": True if form.get("important") == "on" else False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    status = None
    if inserted_note.acknowledged:
        status = True
    else:
        status = False
    docs = conn.notes.notes.find({})
    docs_list = list(docs)
    docs_list = reversed(docs_list)
    return templates.TemplateResponse("notes.html", {"request": request, "notes": docs_list, "status": status})

@note_router.put("/update", response_class=JSONResponse)
async def update_note(request: Request):
    try:
        form = await request.json()  # Parse JSON data from the request body
        note_id = form.get("id")
        print(form)
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
        print(result)

        if result.matched_count == 0:
            return {"status": "error", "message": "Note not found"}
        return {"status": "success", "message": "Note updated successfully! Please refresh the page"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

@note_router.delete("/delete", response_class=JSONResponse)
async def delete_note(request: Request):
    try:
        form = await request.json()
        id = form.get("id")
        print(form)
        conn.notes.notes.delete_one({"_id": ObjectId(id)})
        return {"status": "success", "message": "Note deleted successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@note_router.get("/details/{id}", response_class=JSONResponse)
async def note_details(request: Request, id: str):
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
