from fastapi import FastAPI, HTTPException #importar clase FastAPI
from database import User, Movie, UserReview
from database import database as connection
from schemas import UserRequestModel, UserResponseModel, ReviewRequestModel, ReviewResponseModel, MovieRequestModel, MovieResponseModel

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

#indicar tipo de respuesta = objeto serializado
@app.post('/users', response_model = UserResponseModel)
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

@app.post('/reviews', response_model = ReviewResponseModel)
async def create_reviews(user_review : ReviewRequestModel):
    
    #Validar llaves foraneas
    #Validar id de usuario exista
    if User.select().where(User.id == user_review.user_id).first() is None:
        raise HTTPException(status_code = 404, detail = 'User not found')

    #Validar que el id de pelicula exista
    if Movie.select().where(Movie.id == user_review.movie_id).first() is None:
        raise HTTPException(status_code = 404, detail = 'Movie not found')

    #Crear a partir de los datos que envie el cliente
    user_review = UserReview.create(
        user_id = user_review.user_id,
        movie_id = user_review.movie_id,
        review = user_review.review,
        score = user_review.score
    )

    return user_review

@app.post('/movies', response_model = MovieResponseModel)
async def create_movies(movie : MovieRequestModel):

    if Movie.select().where(Movie.title == movie.title).exists():
        #notificar error
        raise HTTPException(409, 'La pelicula ya se encuentra en la BD.')
    
    movie = Movie.create(
        title = movie.title
    )

    return movie