from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

import models as models, database as database, crud as crud
import empresas as empresas
import schemas 

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="API de Gerenciamento de Empresas")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(empresas.router)

SECRET_KEY = "9FGH8U0G8BVH8G"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# A classe que lida com a autenticação via header 'Authorization'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/")

# Função que cria o token de acesso
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.get("/")
def root():
    return {"message": "API de Empresas - Ecomp Jr"}


@app.post("/admin/")
def admin_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(database.get_db)):
    admin_user = crud.create_or_login_admin(db, form_data)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin_user.nome}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
