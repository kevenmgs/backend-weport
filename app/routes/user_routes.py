

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.models.user import User

from app.schemas.userCreate import UserCreate  
from app.schemas.loginRequest import LoginRequest  
from app.security.security import get_password_hash  
from app.security.security import verify_password 
from app.security.security import create_access_token  

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/user/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()

@router.get("/user_email/{user_email}")
def get_user(user_email: str, db: Session = Depends(get_db)):
    user = db.query(User.name, User.last_name, User.phone_contac_emerg, User.name_contac_emerg).filter(User.email == user_email).first()
    if user:
        return {
            "name": user.name,
            "last_name": user.last_name,
            "phone_contac_emerg": user.phone_contac_emerg,
            "name_contac_emerg": user.name_contac_emerg
        }
    return {"error": "User not found"}



@router.post("/create_user")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    new_user = User(
        name=user.name,
        last_name=user.last_name,
        phone=user.phone,
        address=user.address,
        name_contac_emerg=user.name_contac_emerg,
        phone_contac_emerg=user.phone_contac_emerg,
        email=user.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password): 
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    access_token = create_access_token(data={"sub": db_user.email})

    return {
        "access_token": access_token,
        "id_user": db_user.id,
        "token_type": "bearer"
    }

