from fastapi import HTTPException, APIRouter, Response, Cookie, Depends
from fastapi.security import HTTPBasicCredentials
from ..database import User
from ..schemas import UserRequestModel, UserResponseModel, ReviewResponseModel
from ..common import oauth2_schema
from typing import List

#Crear rutas bajo contexto y nos permite aniadir prefijo.
router = APIRouter(prefix = '/users')

#indicar tipo de respuesta = objeto serializado
@router.post('', response_model = UserResponseModel)
async def create_user(user: UserRequestModel): #indicamos clase de tipo BaseModel, correctos datos de entrada

    #Verificar con consulta, si el username ya existe sin que el server deje de funcionar
    if User.select().where(User.username == user.username).exists():
        #notificar error
        raise HTTPException(409, 'El username ya se encuentra en uso.')

    #utilizar metodo de clase sin uso de objeto
    hash_password = User.create_password(user.password)

    user = User.create(
        username = user.username,
        #asignar la contrasenia hash al atributo creado
        password = hash_password
    )

    #Serializar objeto para ser enviado como respuesta del server. Se convierte a un diccionario


    #retornar Modelo, que nos permite validar datos de entrada y de salida
    return user

#Endpoint para login
#Conocer que usuario se esta autenticando, usuario debe enviar user y password con HTTPUserCredentials
#25/02/2024
@router.post('/login', response_model = UserResponseModel)
async def login(credentials: HTTPBasicCredentials, response: Response):
    
    user = User.select().where(User.username == credentials.username).first()

    if user is None:
        raise HTTPException(404, 'User not found')
    
    if user.password != User.create_password(credentials.password):
        raise HTTPException(404, 'Password error')
    
    #Crear y enviar cookie al cliente. Servidor envia cookie al cliente y no tendra que autenticarse nuevamente.
    #Crear cookie es con Response (fastapi). Anadir cookie como respuesta al servidor

    #Crear y enviar cookies
    response.set_cookie(key = 'user_id', value = user.id) #Token generado respecto a usuario

    return user

'''
#Resenias de usuarios
@router.get('/reviews',response_model = List[ReviewResponseModel])
#Se almacena valor de la cookie que tiene el mismo valor del cookie creado
async def get_reviews(user_id : int = Cookie(None)):

    user = User.select().where(User.id == user_id).first()

    if user is None:
        raise HTTPException(404,"User not found")
    
    # #Obtener valor de cookie
    # return user_id

    #Retornar listado de resenias del usuario
    return [user_review for user_review in user.reviews]
'''

#Cliente realice peticion sobre endpoint se debe de enviar access token
@router.get('/reviews')
#Se almacena valor de la cookie que tiene el mismo valor del cookie creado
#Bloquear con parametro de tipo oauth2passwordBearer. Obtener el usuario apartir del access token
async def get_reviews(token : str = Depends(oauth2_schema)):
    return {
        'token' : token
    }

