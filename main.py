import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import create_document, get_documents, db
from schemas import Book, Subscriber

app = FastAPI(title="Eddy & Ink API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Eddy & Ink Backend is running"}


@app.get("/api/books", response_model=List[Book])
def list_books(category: Optional[str] = None, limit: int = 50):
    """List books available in the store. Optionally filter by category."""
    try:
        filter_dict = {"category": category} if category else None
        docs = get_documents("book", filter_dict=filter_dict, limit=limit)
        # Convert ObjectId and timestamps to serializable forms
        result: List[Book] = []
        for d in docs:
            d.pop("_id", None)
            # Ensure price is float
            if "price" in d and isinstance(d["price"], (int, float)):
                d["price"] = float(d["price"])  # type: ignore
            result.append(Book(**d))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class SubscribeRequest(Subscriber):
    pass


@app.post("/api/subscribe")
def subscribe(body: SubscribeRequest):
    """Collect newsletter subscribers interested in new releases and promotions."""
    try:
        create_document("subscriber", body)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = getattr(db, 'name', "✅ Connected")
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    # Check environment variables
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
