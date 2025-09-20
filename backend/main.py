from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import backend.models as models, backend.database as database, backend.crud as crud
import backend.empresas as empresas

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="API de Gerenciamento de Empresas")

app.include_router(empresas.router)

@app.get("/")
def root():
    return {"message": "API de Empresas - Ecomp Jr"}

@app.post("/admins/", response_model=models.AdminOut)
def admin_create(name: str, senha: str, db: Session = Depends(database.get_db)):
    return crud.create_admin(name, senha, db)


@app.post("/admins/login")
def login_admin(nome: str, senha: str, db: Session = Depends(database.get_db)):
    admin = db.query(models.Admin).filter(models.Admin.nome == nome).first()
    if not admin or not admin.verify_password(senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    return {"message": f"Bem-vindo, {admin.nome}!"}
