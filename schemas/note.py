
def note_schema(item) -> dict:
    return {
        "id": item["_id"],
        "title": item["title"],
        "note": item["note"],
        "created_at": item["created_at"],
        "important": item["important"]
    }

def notes(items) -> list:
    return [note_schema(item) for item in items]

