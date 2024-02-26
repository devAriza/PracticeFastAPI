from fastapi import HTTPException, APIRouter, Response
from fastapi.security import HTTPBasicCredentials
from ..database import User
from ..schemas import UserRequestModel, UserResponseModel

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

