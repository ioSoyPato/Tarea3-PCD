from sqlalchemy import Column, Integer, String, Text
from database import Base  

# Definición del modelo User
# Este modelo representa la tabla "users" en la base de datos.
# Cada instancia de la clase User corresponderá a una fila en la tabla.
class User(Base):
    # Nombre de la tabla en la base de datos
    __tablename__ = "users"
    
    # Definición de las columnas de la tabla
    # user_id es la columna de clave primaria que identifica de manera única a cada usuario.
    user_id = Column(Integer, primary_key=True, index=True)
    
    # user_name almacena el nombre del usuario como una cadena de texto.
    user_name = Column(String, index=True)
    
    # user_email almacena el correo electrónico del usuario.
    # Es único, lo que significa que no pueden existir dos usuarios con el mismo correo.
    user_email = Column(String, unique=True, index=True)
    
    # age almacena la edad del usuario como un número entero.
    # Es opcional (nullable=True), por lo que puede no tener un valor.
    age = Column(Integer, nullable=True)
    
    # recommendations almacena las recomendaciones del usuario como texto.
    # Este campo es opcional.
    recommendations = Column(Text, nullable=True)
    
    # zip_code almacena el código postal del usuario como una cadena de texto.
    # Este campo también es opcional.
    zip_code = Column(String, nullable=True)
