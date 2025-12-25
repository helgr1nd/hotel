from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class RoomCreate(BaseModel):
    description: str = Field(min_length=1)
    price: int = Field(gt=0)

class RoomResponse(BaseModel):
    room_id: int

class RoomItem(BaseModel):
    id: int
    description: str
    price_per_night: int
    created_at: date

# Booking
class BookingCreate(BaseModel):
    room_id: int
    date_start: date
    date_end: date

class BookingResponse(BaseModel):
    booking_id: int

class BookingListItem(BaseModel):
    booking_id: int
    date_start: date
    date_end: date

class RoomSortParams(BaseModel):
    sort_by: Optional[str] = "created_at"
    order: Optional[str] = "desc"