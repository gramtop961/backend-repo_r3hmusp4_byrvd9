import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import MenuItem, CateringRequest, Order

app = FastAPI(title="Coffee Shop API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Coffee Shop Backend is running"}

@app.get("/test")
def test_database():
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
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
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

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# -------- Menu Endpoints --------
@app.post("/api/menu", status_code=201)
async def create_menu_item(item: MenuItem):
    try:
        inserted_id = create_document("menuitem", item)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/menu")
async def list_menu(category: Optional[str] = None):
    try:
        filter_dict = {"category": category} if category else {}
        items = get_documents("menuitem", filter_dict)
        # convert ObjectId to string
        for i in items:
            if i.get("_id"):
                i["_id"] = str(i["_id"])
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------- Catering Endpoints --------
@app.post("/api/catering", status_code=201)
async def request_catering(payload: CateringRequest):
    try:
        inserted_id = create_document("cateringrequest", payload)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------- Orders (Pickup) --------
@app.post("/api/orders", status_code=201)
async def place_order(order: Order):
    try:
        inserted_id = create_document("order", order)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/orders")
async def list_orders(limit: int = 20):
    try:
        docs = get_documents("order", {}, limit=limit)
        for d in docs:
            if d.get("_id"):
                d["_id"] = str(d["_id"])
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
