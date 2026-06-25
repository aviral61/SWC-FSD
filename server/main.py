
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, games, cart, orders

app = FastAPI(title="GameKey Store API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(games.router)
app.include_router(cart.router)
app.include_router(orders.router)

@app.get("/")
def root():
    return {"message": "GameKey Store API running"}
