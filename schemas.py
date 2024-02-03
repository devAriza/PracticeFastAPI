#validar datos de entrada y salida
from pydantic import BaseModel

#Garantizar que cada uno de los atributos correspondan al tipo de datoy 
class UserBaseModel(BaseModel):
    username: str
    password: str