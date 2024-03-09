from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from .database import User
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
    #Si el access token no puede ser decodificado por caducidad, retorna None
    try:

        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    
    except Exception as err:

        return None

#Obtener usuario autenticado. Recibe token
def get_current_user(token : str = Depends(oauth2_schema)) -> User:
    data = decode_access_token(token)
    #Obtener usuario autenticado
    if data:
        return User.select().where(User.id == data['user_id']).first()
    else:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Access Token no valido',
            headers = {'WWW-Autenticate' : 'Beraer'}
        )