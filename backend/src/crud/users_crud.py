from sqlmodel import Session, select
from backend.src.models.models import UserCreate, UserInDB
from backend.src.services.security import get_password_hash

# CREATE
def create_user(db: Session, user_data: UserCreate) -> UserInDB:
    hashed_pw = get_password_hash(user_data.password)
    user = UserInDB(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pw,
        disabled=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# READ
def get_user_by_username(db: Session, username: str) -> UserInDB | None:
    query = select(UserInDB).where(UserInDB.username == username)
    return db.exec(query).first()

def get_user_by_email(db: Session, email: str) -> UserInDB | None:
    query = select(UserInDB).where(UserInDB.email == email)
    return db.exec(query).first()

def get_all_users(db: Session) -> list[UserInDB]:
    query = select(UserInDB)
    return db.exec(query).all()

# UPDATE

# DELETE
def delete_user(db: Session, user: UserInDB) -> None:
    db.delete(user)
    db.commit()