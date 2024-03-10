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
    
#Refactor
class ResponseModel(BaseModel):
    #Sirve para responder con objeto tipo JSON. Convertir modelos de peewee a modelos de pydantic
    class Config:
        from_attributes = True

#Generar respuestas de tipo usuario
class UserResponseModel(ResponseModel):
    id : int
    username : str

#Validar score
class ReviewValidator():
    #validar score este entre 1 - 5
    @field_validator('score')
    def score_validator(cls,score):
        if score < 0 or score > 5:
            raise ValueError('El rango para score es de 0 a 5')
        
        return score
    
# ------------- Movie -------------

class MovieRequestModel(BaseModel):
    title : str

class MovieResponseModel(ResponseModel):
    id : int
    title : str


#Atributos dentro de modelo obligatorios
class ReviewRequestModel(BaseModel, ReviewValidator):
    #user_id : int #Se comenta ya que se sabe el user mediante la autenticacion de aouth2
    movie_id : int
    reviews : str
    score : int

class ReviewResponseModel(ResponseModel):
    id : int
    #Relacionar objetos
    movie: MovieResponseModel
    reviews : str
    score : int

#Editar review
class ReviewRequestPutModel(BaseModel, ReviewValidator):
    reviews : str
    score : int

#Eliminar review
class ReviewRequestDeleteModel(BaseModel, ReviewValidator):
    id : int
    user_id : int
    movie_id : int
    reviews : str
    score : int






    

