#validar datos de entrada y salida
from pydantic import BaseModel,field_validator, ValidationError, validator


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