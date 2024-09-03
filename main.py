from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import uvicorn
from typing import List

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Validar la conexión con la base de datos
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Entrada del usuario
class UserCreate(BaseModel):
    user_name: str = Field(min_length=1)
    user_email: str = Field(min_length=1)
    age: int = Field(gt=0, lt=110, default=None)
    recommendations: List[str] = [] 
    zip_code: str = Field(min_length=4, max_length=8, default=None)

@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Revisar si el correo ya está registrado
    db_user = db.query(models.User).filter(models.User.user_email == user.user_email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_model = models.User(
        user_name=user.user_name,
        user_email=user.user_email,
        age=user.age,
        zip_code=user.zip_code
    )
    user_model.set_recommendations(user.recommendations)  # Serializar recomendaciones

    # Agregar el usuario a la db 
    db.add(user_model)
    db.commit()
    db.refresh(user_model)

    return user_model

@app.put("/{user_id}")
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    user_model = db.query(models.User).filter(models.User.user_id == user_id).first()

    if user_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {user_id} : Does not exist"
        )

    user_model.user_name = user.user_name
    user_model.user_email = user.user_email
    user_model.age = user.age
    user_model.set_recommendations(user.recommendations)  
    user_model.zip_code = user.zip_code

    db.commit()
    db.refresh(user_model)

    return user_model

@app.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_model = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail=f"User ID {user_id} does not exist")

    db.delete(user_model)
    db.commit()

    return {"detail": f"User ID {user_id} has been deleted"}

@app.get("/{user_id}/recommendations")
def get_user_recommendations(user_id: int, db: Session = Depends(get_db)):
    user_model = db.query(models.User).filter(models.User.user_id == user_id).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {"recommendations": user_model.get_recommendations()}


if __name__ == "__main__":
    uvicorn.run(app, port=4444)