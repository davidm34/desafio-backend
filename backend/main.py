from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models as models, database as database, crud as crud
import empresas as empresas
import schemas 

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="API de Gerenciamento de Empresas")

app.include_router(empresas.router)

@app.get("/")
def root():
    return {"message": "API de Empresas - Ecomp Jr"}

@app.post("/admins/", response_model=schemas.AdminOut)
def admin_create(admin: schemas.AdminCreate, db: Session = Depends(database.get_db)):
    return crud.create_admin(db, admin)


@app.post("/admins/login")
def login_admin(nome: str, senha: str, db: Session = Depends(database.get_db)):
    admin = db.query(models.Admin).filter(models.Admin.nome == nome).first()
    if not admin or not admin.senha == (senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    return {"message": f"Bem-vindo, {admin.nome}!"}
