from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# Configuración de la base de datos
DATABASE_URL = "mysql+pymysql://root:@localhost/casas"

# Crear motor de base de datos
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    echo=False  # Cambiar a True para ver las consultas SQL generadas
)

# Crear sesión
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Base para modelos
Base = declarative_base()

def get_db():
    """Obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Inicializar base de datos (crear tablas si no existen)"""
    Base.metadata.create_all(bind=engine)
