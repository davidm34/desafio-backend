from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas as schemas, crud as crud, database as database

router = APIRouter(prefix="/empresas", tags=["empresas"])

@router.post("/", response_model=schemas.EmpresaOut)
def create(empresa: schemas.EmpresaCreate, db: Session = Depends(database.get_db)):
    return crud.create_empresa(db, empresa)

@router.get("/", response_model=list[schemas.EmpresaOut])
def list(cidade: str | None = None, ramo: str | None = None, search: str | None = None, db: Session = Depends(database.get_db)):
    return crud.get_empresas(db, cidade, ramo, search)

@router.get("/{empresa_id}", response_model=schemas.EmpresaOut)
def detail(empresa_id: int, db: Session = Depends(database.get_db)):
    return crud.get_empresa(db, empresa_id)

@router.put("/{empresa_id}", response_model=schemas.EmpresaOut)
def update(empresa_id: int, updates: schemas.EmpresaUpdate, db: Session = Depends(database.get_db)):
    return crud.update_empresa(db, empresa_id, updates)

@router.delete("/{empresa_id}")
def delete(empresa_id: int, db: Session = Depends(database.get_db)):
    return crud.delete_empresa(db, empresa_id)
