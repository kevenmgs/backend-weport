from fastapi import FastAPI
from app.routes import user_routes
from app.models.database import engine
from app.models.user import Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://192.168.0.17:3000"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(user_routes.router, prefix="/api", tags=["Users"])

@app.get("/")
def root():
    return {"message": "API con FastAPI y MySQL funcionando correctamente"}
