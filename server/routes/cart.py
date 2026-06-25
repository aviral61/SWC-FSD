
from fastapi import APIRouter, Depends
from database import cart_collection, games_collection
from models import CartItem
from auth import get_current_user
from bson import ObjectId

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("/")
async def get_cart(user=Depends(get_current_user)):
    cart = await cart_collection.find_one({"user_id": str(user["_id"])})
    if not cart:
        return {"items": []}
    return {"items": cart.get("items", [])}

@router.post("/add")
async def add_to_cart(item: CartItem, user=Depends(get_current_user)):
    user_id = str(user["_id"])
    game = await games_collection.find_one({"_id": ObjectId(item.game_id)})
    if not game:
        return {"error": "Game not found"}
    cart = await cart_collection.find_one({"user_id": user_id})
    if cart:
        items = cart.get("items", [])
        for i in items:
            if i["game_id"] == item.game_id:
                i["quantity"] += item.quantity
                break
        else:
            items.append(item.dict())
        await cart_collection.update_one({"user_id": user_id}, {"$set": {"items": items}})
    else:
        await cart_collection.insert_one({"user_id": user_id, "items": [item.dict()]})
    return {"message": "Added to cart"}

@router.delete("/remove/{game_id}")
async def remove_from_cart(game_id: str, user=Depends(get_current_user)):
    user_id = str(user["_id"])
    cart = await cart_collection.find_one({"user_id": user_id})
    if cart:
        items = [i for i in cart.get("items", []) if i["game_id"] != game_id]
        await cart_collection.update_one({"user_id": user_id}, {"$set": {"items": items}})
    return {"message": "Removed from cart"}
