from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Definir la URL de la base de datos SQLite
# Este es el camino relativo al archivo 'users.db', que se creará en el mismo directorio que el script.
SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"

# Crear el motor de la base de datos
# El motor es responsable de la comunicación con la base de datos.
# El argumento 'check_same_thread=False' es necesario en SQLite para permitir que la misma conexión se use en diferentes hilos.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Crear una fábrica de sesiones
# sessionmaker es una fábrica que proporciona instancias de sesiones para interactuar con la base de datos.
# autocommit=False asegura que las transacciones deben ser confirmadas manualmente.
# autoflush=False desactiva el autoflush, lo que significa que los cambios no se enviarán automáticamente a la base de datos hasta que se confirme.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear una clase base para los modelos de SQLAlchemy
# Todos los modelos definidos en el proyecto heredarán de esta clase Base.
# Esta clase es utilizada por SQLAlchemy para saber cómo mapear las clases de Python a las tablas de la base de datos.
Base = declarative_base()
