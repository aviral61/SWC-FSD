
from fastapi import APIRouter, HTTPException, Depends
from database import games_collection
from models import Game
from auth import get_current_user
from bson import ObjectId

router = APIRouter(prefix="/games", tags=["Games"])

def serialize(game) -> dict:
    game["id"] = str(game["_id"])
    del game["_id"]
    return game

@router.get("/")
async def get_all_games():
    games = await games_collection.find().to_list(100)
    return [serialize(g) for g in games]

@router.get("/{game_id}")
async def get_game(game_id: str):
    game = await games_collection.find_one({"_id": ObjectId(game_id)})
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return serialize(game)

@router.post("/")
async def add_game(game: Game, user=Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    result = await games_collection.insert_one(game.dict())
    return {"id": str(result.inserted_id), "message": "Game added"}

@router.put("/{game_id}")
async def update_game(game_id: str, game: Game, user=Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    await games_collection.update_one({"_id": ObjectId(game_id)}, {"$set": game.dict()})
    return {"message": "Game updated"}

@router.delete("/{game_id}")
async def delete_game(game_id: str, user=Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    await games_collection.delete_one({"_id": ObjectId(game_id)})
    return {"message": "Game deleted"}
