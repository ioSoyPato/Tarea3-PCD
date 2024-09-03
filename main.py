from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import uvicorn
from typing import List

# Instancia de la aplicación FastAPI
app = FastAPI()

# Crear todas las tablas en la base de datos (si no existen) usando los modelos definidos en models.py
models.Base.metadata.create_all(bind=engine)

# Función para obtener una sesión de la base de datos
# Se utiliza para gestionar la conexión a la base de datos y garantizar que se cierre correctamente.
def get_db():
    try:
        db = SessionLocal()  # Crear una nueva sesión
        yield db  # Devuelve la sesión para su uso
    finally:
        db.close()  # Cierra la sesión después de que se haya usado

# Modelo de entrada de datos para crear o actualizar usuarios
# Define los campos requeridos y sus restricciones usando Pydantic
class UserCreate(BaseModel):
    user_name: str = Field(min_length=1)  # Nombre de usuario, no puede estar vacío
    user_email: str = Field(min_length=1)  # Correo electrónico del usuario, no puede estar vacío
    age: int = Field(gt=0, lt=110, default=None)  # Edad del usuario, debe ser un número positivo menor a 110
    recommendations: List[str] = []  # Lista de recomendaciones para el usuario, por defecto vacía
    zip_code: str = Field(min_length=4, max_length=8, default=None)  # Código postal del usuario, longitud entre 4 y 8 caracteres

# Endpoint GET para leer todos los usuarios de la base de datos
# Retorna una lista de todos los usuarios almacenados en la base de datos.
@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# Endpoint POST para crear un nuevo usuario
# Valida que el correo electrónico no esté ya registrado y agrega el usuario a la base de datos.
@app.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Comprobar si el correo ya está registrado en la base de datos
    db_user = db.query(models.User).filter(models.User.user_email == user.user_email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")  # Error si el correo ya existe

    # Crear un nuevo objeto de usuario usando los datos proporcionados
    user_model = models.User(
        user_name=user.user_name,
        user_email=user.user_email,
        age=user.age,
        zip_code=user.zip_code
    )
    user_model.set_recommendations(user.recommendations)  # Serializar la lista de recomendaciones y guardarla

    # Agregar el nuevo usuario a la base de datos
    db.add(user_model)
    db.commit()  # Confirmar la transacción
    db.refresh(user_model)  # Actualizar el modelo con los datos de la base de datos

    return user_model  # Retornar el usuario creado

# Endpoint PUT para actualizar un usuario existente
# Busca al usuario por su ID, y si existe, actualiza su información.
@app.put("/{user_id}")
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    # Buscar el usuario en la base de datos por su ID
    user_model = db.query(models.User).filter(models.User.user_id == user_id).first()

    # Si el usuario no existe, retornar un error 404
    if user_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {user_id} : Does not exist"
        )

    # Actualizar los campos del usuario con los nuevos valores proporcionados
    user_model.user_name = user.user_name
    user_model.user_email = user.user_email
    user_model.age = user.age
    user_model.set_recommendations(user.recommendations)  # Serializar y actualizar las recomendaciones
    user_model.zip_code = user.zip_code

    db.commit()  # Confirmar los cambios en la base de datos
    db.refresh(user_model)  # Actualizar el modelo con los datos de la base de datos

    return user_model  # Retornar el usuario actualizado

# Endpoint DELETE para eliminar un usuario
# Elimina al usuario con el ID especificado de la base de datos.
@app.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # Buscar el usuario en la base de datos por su ID
    user_model = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail=f"User ID {user_id} does not exist")  # Error si el usuario no existe

    # Eliminar el usuario de la base de datos
    db.delete(user_model)
    db.commit()  # Confirmar la eliminación

    return {"detail": f"User ID {user_id} has been deleted"}  # Retornar un mensaje de éxito

# Endpoint GET para obtener las recomendaciones de un usuario específico
# Deserializa y retorna la lista de recomendaciones para el usuario con el ID proporcionado.
@app.get("/{user_id}/recommendations")
def get_user_recommendations(user_id: int, db: Session = Depends(get_db)):
    # Buscar el usuario en la base de datos por su ID
    user_model = db.query(models.User).filter(models.User.user_id == user_id).first()

    # Si el usuario no existe, retornar un error 404
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {"recommendations": user_model.get_recommendations()}  # Retornar las recomendaciones deserializadas

# Punto de entrada para ejecutar la aplicación
# Inicia el servidor de FastAPI en el puerto 4444.
if __name__ == "__main__":
    uvicorn.run(app, port=4444)
