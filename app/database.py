from sqlalchemy import create_engine, Column, Integer, DECIMAL, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError
from datetime import datetime

# Configuración de la base de datos SQLite (archivo finanzas.db)
engine = create_engine("sqlite:///./finanzas.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Crea una clase base (Base) que usarás para definir los modelos de datos (tablas)
Base = declarative_base()