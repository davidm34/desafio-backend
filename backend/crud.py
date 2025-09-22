from sqlalchemy.orm import Session
from sqlalchemy import and_
import models as models, schemas as schemas
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from typing import Annotated

def get_empresas(db: Session, cidade: str | None = None, ramo: str | None = None, search: str | None = None):
    query = db.query(models.Empresa)
    if cidade:
        query = query.filter(models.Empresa.cidade)
    if ramo:
        query = query.filter(models.Empresa.ramo_atuacao)
    if search:
        query = query.filter(models.Empresa.nome)
    return query.all()

def get_empresa(db: Session, empresa_id: int):
    empresa = db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada")
    return empresa

def create_empresa(db: Session, empresa: schemas.EmpresaOut):
    db_empresa = models.Empresa(**empresa.model_dump())
    db.add(db_empresa)
    try:
        db.commit()
        db.refresh(db_empresa)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="CNPJ ou Email já cadastrado")
    return db_empresa

def update_empresa(db: Session, empresa_id: int, updates: schemas.EmpresaUpdate):
    empresa = get_empresa(db, empresa_id)
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(empresa, key, value)
    db.commit()
    db.refresh(empresa)
    return empresa

def delete_empresa(db: Session, empresa_id: int):
    empresa = get_empresa(db, empresa_id)
    db.delete(empresa)
    db.commit()
    return {"detail": "Empresa excluída com sucesso"}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_admin_by_name(db: Session, nome: str):
    return db.query(models.Admin).filter(models.Admin.nome == nome).first()

def create_or_login_admin(db: Session, admin: OAuth2PasswordRequestForm):
    existing_admin = get_admin_by_name(db, nome=admin.username)
    

    if existing_admin:
        if verify_password(admin.password, existing_admin.senha):
            return existing_admin 
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas"
            )
    else:
        # Se o admin não existe, cria um novo
        hashed_password = get_password_hash(admin.password)
        db_admin = models.Admin(
            nome=admin.username,
            senha=hashed_password 
        )
        db.add(db_admin)
        db.commit()
        db.refresh(db_admin)
        return db_admin
       