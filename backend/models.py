from datetime import date
from sqlmodel import Field, SQLModel

class TripBase(SQLModel):
    title: str = Field(index=True)
    text: str 
    destination: str = Field(index=True)
    start_date: str | None = Field(default=None, index=True)
    end_date: str | None = Field(default=None, index=True)
    price_euro: float | None = Field(default=None, index=True)

class Trip(TripBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class TripUpdate(SQLModel):
    title: str | None = None
    text: str | None = None
    destination: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    price_euro: float | None = None
    






