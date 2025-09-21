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
def admin(admin: schemas.AdminCreate, db: Session = Depends(database.get_db)):
    return crud.create_or_login_admin(db, admin)
