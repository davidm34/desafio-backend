from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from backend.database import Base

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cnpj = Column(String, unique=True, nullable=False)
    cidade = Column(String, nullable=False)
    ramo_atuacao = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    email_contato = Column(String, unique=True, nullable=False)
    data_cadastro = Column(DateTime(timezone=True), server_default=func.now())
    is_Admin = Column(Boolean, nullable=True)


class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    senha = Column(String, nullable=False)
