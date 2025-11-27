from fastapi import APIRouter, HTTPException
from backend.src.database.database import SessionDep
from backend.src.crud.trips_crud import get_trips, get_trip, save_trip, update_trip, delete_trip
from backend.src.models.models import TripBase, Trip, TripUpdate

router = APIRouter()

@router.get("/trips/")
async def read_trips(db: SessionDep): 
    trips =  await get_trips(db)
    if not trips:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trips

@router.get("/trips/{trip_id}")
async def read_trip(db: SessionDep, trip_id: int):
    trip = await get_trip(db, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip

@router.post("/trips", response_model=Trip)
async def create_trip(db: SessionDep, trip: TripBase):
    return await save_trip(db, trip)

@router.put("/trips/{trip_id}", response_model=Trip)
async def update_trip_route(db: SessionDep, trip_id: int, trip: TripUpdate):
    updated = await update_trip(db, trip_id, trip)
    if not updated:
        raise HTTPException(status_code=404, detail="Trip not found")
    return updated

@router.delete("/trips/{trip_id}")
async def delete_trip_route(db: SessionDep, trip_id: int):
    if not await delete_trip(db, trip_id):
        raise HTTPException(status_code=404, detail="Trip not found")
    return None
