from fastapi import FastAPI
from app.routers import rooms, bookings

app = FastAPI(
    title="Hotel Booking API",
    description="API для управления номерами отеля и бронированиями",
    version="1.0.0"
)

app.include_router(rooms.router)
app.include_router(bookings.router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"message": "Hotel Booking Service API. Docs at /docs"}