from datetime import date
import re
from pydantic import EmailStr, field_validator
from sqlmodel import Field, SQLModel

#Trip
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
    


# Token models
class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str | None = None



# User models
class UserInDB(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True)
    username: str  = Field(max_length=50, unique=True)
    email: EmailStr = Field(max_length=50, unique=True)
    hashed_password: str 
    disabled: bool = False

class UserRead(SQLModel):
    id: int | None = None
    username: str
    email: str | None = None
    disabled: bool | None = None

class UserCreate(SQLModel):
    username: str
    email: EmailStr
    password: str
    password_repeat: str

    @field_validator("password_repeat")
    def passwords_match(cls, v, info):
        # info.data enthält alle bisherigen Felder
        password = info.data.get("password")
        if password is not None and v != password:
            raise ValueError("Passwörter stimmen nicht überein")
        return v
    
    @field_validator("password")
    def password_policy(cls, v):
        # mindestens 8 Zeichen
        if len(v) < 8:
            raise ValueError("Passwort muss mindestens 8 Zeichen lang sein")
        # mindestens ein Großbuchstabe
        if not re.search(r"[A-Z]", v):
            raise ValueError("Passwort muss mindestens einen Großbuchstaben enthalten")
        # mindestens ein Kleinbuchstabe
        if not re.search(r"[a-z]", v):
            raise ValueError("Passwort muss mindestens einen Kleinbuchstaben enthalten")
        # mindestens eine Zahl
        if not re.search(r"\d", v):
            raise ValueError("Passwort muss mindestens eine Zahl enthalten")
        # mindestens ein Sonderzeichen
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Passwort muss mindestens ein Sonderzeichen enthalten")
        return v





