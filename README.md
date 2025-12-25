Hotel Booking API

Простой REST API для управления номерами отеля и бронированиями, реализованный на FastAPI с PostgreSQL.

Функционал:

1. Управление номерами
- `POST /rooms/` — добавить номер отеля
- `DELETE /rooms/{id}` — удалить номер и все его брони
- `GET /rooms/?sort_by=price&order=asc` — получить список номеров с сортировкой

2. Управление бронированиями
- `POST /bookings/` — добавить бронь номера
- `DELETE /bookings/{id}` — удалить бронь
- `GET /bookings/list?room_id={id}` — получить список броней номера

Технологии:
- Python 3.8+
- FastAPI
- SQLAlchemy (ORM)
- PostgreSQL
- Pydantic (валидация)
