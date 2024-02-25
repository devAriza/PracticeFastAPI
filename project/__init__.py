#Python reconoce a la carpeta como un paquete

from fastapi import FastAPI, APIRouter #importar clase FastAPI
from .database import User, Movie, UserReview
from .database import database as connection

from .routers import user_router, review_router, movie_router

#Ingresar a documentacion del servicio web con URL/docs

#Crear instancia de FastAPI
app = FastAPI(title = 'Proyecto para reseniar peliculas', #titulo de proyecto
              description = 'En este proyecto, seremos capaces de reseniar peliculas', #description for project
              version = '1' #versionar proyecto
              )

api_v1 = APIRouter(prefix = '/api/v1')

#anadir rutas a app pasando como argumento listado de rutas. Objeto de
api_v1.include_router(user_router)
api_v1.include_router(review_router)
api_v1.include_router(movie_router)

app.include_router(api_v1)

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



