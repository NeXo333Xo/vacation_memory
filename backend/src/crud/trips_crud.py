from sqlmodel import select
from backend.src.models.models import Trip, TripBase, TripUpdate
from backend.src.database.database import SessionDep

# GET
async def get_trip(db: SessionDep, trip_id: int) -> Trip | None:
    return db.get(Trip, trip_id)

async def get_trips(db: SessionDep) -> list[Trip]:
    return db.exec(select(Trip)).all()

# Create
async def save_trip(db: SessionDep, trip: TripBase) -> Trip:
    db_trip = Trip(**trip.model_dump())
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip

# Update
async def update_trip(db: SessionDep, trip_id: int, trip: TripUpdate) -> Trip | None:
    db_trip = db.get(Trip, trip_id)
    if not db_trip:
        return None    
    
    update_data = trip.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_trip, key, value)
    
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip

# Delete
async def delete_trip(db: SessionDep, trip_id: int) -> bool:
    trip = db.get(Trip, trip_id)
    if not trip:
        return False
    db.delete(trip)
    db.commit()
    return True



