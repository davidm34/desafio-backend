from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status

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

def create_empresa(db: Session, empresa: schemas.EmpresaCreate):
    db_empresa = models.Empresa(**empresa.dict())
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

