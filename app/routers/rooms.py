from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.post("/", response_model=schemas.RoomResponse)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    db_room = models.Room(
        description=room.description,
        price_per_night=room.price
    )
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return {"room_id": db_room.id}

@router.delete("/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db)):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(db_room)
    db.commit()
    return {"message": f"Room {room_id} and its bookings deleted"}

@router.get("/", response_model=list[schemas.RoomItem])
def get_rooms(
    sort_by: str = Query("created_at", description="Sort by: 'price' or 'created_at'"),
    order: str = Query("desc", description="Order: 'asc' or 'desc'"),
    db: Session = Depends(get_db)
):

    if sort_by == "price":
        order_column = models.Room.price_per_night
    else:
        order_column = models.Room.created_at


    if order == "asc":
        order_func = asc(order_column)
    else:
        order_func = desc(order_column)

    rooms = db.query(models.Room).order_by(order_func).all()
    return rooms