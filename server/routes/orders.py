
from fastapi import APIRouter, Depends, HTTPException
from database import orders_collection, cart_collection, games_collection
from auth import get_current_user
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/orders", tags=["Orders"])

def serialize(o):
    o["id"] = str(o["_id"])
    del o["_id"]
    return o

@router.post("/place")
async def place_order(user=Depends(get_current_user)):
    user_id = str(user["_id"])
    cart = await cart_collection.find_one({"user_id": user_id})
    if not cart or not cart.get("items"):
        raise HTTPException(status_code=400, detail="Cart is empty")
    items = []
    total = 0
    for item in cart["items"]:
        game = await games_collection.find_one({"_id": ObjectId(item["game_id"])})
        if game:
            line = {
                "game_id":  item["game_id"],
                "title":    game["title"],
                "price":    game["price"],
                "quantity": item["quantity"]
            }
            total += game["price"] * item["quantity"]
            items.append(line)
    order = {
        "user_id":    user_id,
        "items":      items,
        "total":      total,
        "status":     "confirmed",
        "created_at": datetime.utcnow()
    }
    await orders_collection.insert_one(order)
    await cart_collection.delete_one({"user_id": user_id})
    return {"message": "Order placed", "total": total}

@router.get("/")
async def get_orders(user=Depends(get_current_user)):
    orders = await orders_collection.find(
        {"user_id": str(user["_id"])}
    ).to_list(50)
    return [serialize(o) for o in orders]
