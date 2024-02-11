from fastapi import FastAPI, HTTPException #importar clase FastAPI
from database import User, Movie, UserReview
from database import database as connection
from schemas import UserBaseModel

#Ingresar a documentacion del servicio web con URL/docs

#Crear instancia de FastAPI
app = FastAPI(title = 'Proyecto para reseniar peliculas', #titulo de proyecto
              description = 'En este proyecto, seremos capaces de reseniar peliculas', #description for project
              version = '1' #versionar proyecto
              )


#Ejecutar cuando el server este por comenzar
@app.on_event('startup')
async def startup_event():
    if connection.is_closed():
        connection.connect()

    #Creacion de tablas. En caso de existir no pasa nada
    connection.create_tables([User, Movie, UserReview]) 


#Ejecutar cuando el server este por finalizar
@app.on_event('shutdown')
def shutdown_event():
    if not connection.is_closed():
        connection.close()


#La funcion encargada de retornar respuesta
#Si hay multiples funciones, se completen de forma asincrona con 'async'
@app.get('/')
async def index():
    return 'Hola mundo, desde un server en FastAPI'


@app.get('/about')
async def about():
    return app.description

@app.post('/users')
async def create_user(user: UserBaseModel): #indicamos clase de tipo BaseModel, correctos datos de entrada

    #Verificar con consulta, si el username ya existe sin que el server deje de funcionar
    if User.select().where(User.username == user.username).exists():
        #notificar error
        return HTTPException(409, 'El username ya se encuentra en uso.')

    #utilizar metodo de clase sin uso de objeto
    hash_password = User.create_password(user.password)

    user = User.create(
        username = user.username,
        #asignar la contrasenia hash al atributo creado
        password = hash_password
    )

    return user.id