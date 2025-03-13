

from fastapi import APIRouter, Depends , HTTPException, status
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.models.user import User

from app.schemas.userCreate import UserCreate  
from app.schemas.loginRequest import LoginRequest  
from app.security.security import get_password_hash  
from app.security.security import verify_password 
from app.security.security import create_access_token 
from fastapi.responses import JSONResponse

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
    user = db.query(User.id).filter(User.email == user_email).first()
    if user:
        return {
            "id": user.id,
        }
    return {"error": "User not found"}


@router.get("/contact_information/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User.name, User.last_name, User.phone_contac_emerg, User.name_contac_emerg).filter(User.id == user_id).first()
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
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado."
        )

    try:
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

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Usuario creado exitosamente", "user_id": new_user.id}
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el usuario: {str(e)}"
        )
    return new_user


@router.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password): 
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )

    access_token = create_access_token(data={"sub": db_user.email})

    return {
        "message": f"Bienvenido, {db_user.name}!",  
        "access_token": access_token,
        "id_user": db_user.id,
        "token_type": "bearer"
    }

