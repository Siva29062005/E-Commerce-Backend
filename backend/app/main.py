from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, SessionLocal, engine
from app.db_migrate import run_migrations
from app.routers import auth, cart, contact, newsletter, orders, products, reviews, users, wishlist
from app.seed_data import run_seed


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    run_migrations()
    if settings.seed_on_startup:
        db = SessionLocal()
        try:
            run_seed(db)
        finally:
            db.close()
    yield


app = FastAPI(
    title="VIKINGS API",
    description="Backend for VIKINGS ultra-luxury innerwear storefront",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(reviews.router, prefix="/api")
app.include_router(cart.router, prefix="/api")
app.include_router(wishlist.router, prefix="/api")
app.include_router(orders.router, prefix="/api")
app.include_router(contact.router, prefix="/api")
app.include_router(newsletter.router, prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "vikings-api", "version": "2.0.0"}
