#validar datos de entrada y salida
from typing import Any
from pydantic import BaseModel,field_validator, ValidationError, validator
from pydantic.v1.utils import GetterDict
from peewee import ModelSelect

#Convertir objeto tipo Model (peewee) a diccionario
class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        #Obtener cada uno de los atributos de objeto Model y comparar con ResponseModel
        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)
        
        return res

#Garantizar que cada uno de los atributos correspondan al tipo de dato
#Valores que se envian. Datos de entrada
class UserRequestModel(BaseModel):
    username: str
    password: str

    @field_validator('username')
    def username_validator(cls, username):
        if len(username) < 3 or len(username) > 50:
            raise ValueError('La longitud debe de encontrarse entre 3 y 50 caracteres.')
        
        return username
    
#Generar respuestas de tipo usuario
class UserResponseModel(BaseModel):
    id : int
    username : str

    #Sirve para responder con objeto tipo JSON. Convertir modelos de peewee a modelos de pydantic
    class Config:
        from_attributes = True
        
#Atributos dentro de modelo obligatorios
class ReviewRequestModel(BaseModel):
    user_id : int
    movie_id : int
    review : str
    score : int

class ReviewResponseModel(BaseModel):
    id : int
    movie_id : int
    review : str
    score : int

    class Config:
        from_attributes = True

class MovieRequestModel(BaseModel):
    title : str

class MovieResponseModel(BaseModel):
    title : str

    class Config:
        from_attributes = True