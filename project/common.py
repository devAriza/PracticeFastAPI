from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
import jwt

SECRET_KEY = 'EjemploDeSecreto'
#Al utilizar Bearer que trabajaremos con access token. Token type Json
#cliente intente ingresar a endpoint y no posea access token. Podra autenticarse en el endpoint 
oauth2_schema = OAuth2PasswordBearer(tokenUrl = '/api/v1/auth')

#Crear un access token. apartir de un usuario y una fecha de expiracion
def create_access_token(user, days = 7):

    #Token puede conformarse por diferentes valores. Ej 3
    data = {
        'user_id': user.id,
        'username': user.username,
        #fecha de expiracion. Fechaactual + n cantidad de dias.
        'exp': datetime.utcnow() + timedelta(days = days)
    }

    #encode -> generamos access token
    #codificar diccionario utilizando secreto y algoritmo
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")


def decode_access_token(token):
    pass

#Obtener usuario autenticado. Recibe token
def get_current_user(token : str = Depends(oauth2_schema)):
    pass