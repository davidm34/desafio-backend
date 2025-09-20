from pydantic import BaseModel, EmailStr
from datetime import datetime

class EmpresaBase(BaseModel):
    nome: str
    cnpj: str
    cidade: str
    ramo_atuacao: str
    telefone: str 
    email_contato: EmailStr

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaUpdate(BaseModel):
    nome: str | None = None
    cidade: str | None = None
    ramo_atuacao: str | None = None
    telefone: str | None = None
    email_contato: EmailStr | None = None

class EmpresaOut(EmpresaBase):
    id: int
    data_cadastro: datetime

    class Config:
        orm_mode = True


class AdminBase(BaseModel):
    nome: str
    senha: str

class AdminCreate(AdminBase):
    pass

class AdminOut(AdminBase):
    id: int 
    class Config:
        orm_mode = True