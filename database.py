from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL

url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="04052004",
    host="localhost",
    database="postgres",
    port=5432
)

engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency para usar nas rotas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()