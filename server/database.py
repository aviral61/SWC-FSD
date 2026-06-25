from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

client = AsyncIOMotorClient(os.getenv("MONGO_URL"))
db = client[os.getenv("DB_NAME")]

users_collection  = db["users"]
games_collection  = db["games"]
cart_collection   = db["cart"]
orders_collection = db["orders"]
