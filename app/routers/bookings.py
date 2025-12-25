from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("/", response_model=schemas.BookingResponse)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    # Проверка существования номера
    room = db.query(models.Room).filter(models.Room.id == booking.room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")


    overlapping = db.query(models.Booking).filter(
        models.Booking.room_id == booking.room_id,
        and_(
            models.Booking.date_start < booking.date_end,
            models.Booking.date_end > booking.date_start
        )
    ).first()
    if overlapping:
        raise HTTPException(status_code=400, detail="Room already booked for these dates")


    db_booking = models.Booking(
        room_id=booking.room_id,
        date_start=booking.date_start,
        date_end=booking.date_end
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return {"booking_id": db_booking.id}

@router.delete("/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(booking)
    db.commit()
    return {"message": f"Booking {booking_id} deleted"}

@router.get("/list", response_model=list[schemas.BookingListItem])
def get_bookings_by_room(
    room_id: int = Query(..., description="ID номера отеля"),
    db: Session = Depends(get_db)
):
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    bookings = db.query(models.Booking).filter(
        models.Booking.room_id == room_id
    ).order_by(models.Booking.date_start).all()

    return [
        {
            "booking_id": b.id,
            "date_start": b.date_start,
            "date_end": b.date_end
        }
        for b in bookings
    ]