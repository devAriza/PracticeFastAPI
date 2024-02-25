from fastapi import HTTPException, APIRouter
from ..database import Movie
from ..schemas import MovieRequestModel, MovieResponseModel

router = APIRouter(prefix = '/movies')

@router.post('/movies', response_model = MovieResponseModel)
async def create_movies(movie : MovieRequestModel):

    if Movie.select().where(Movie.title == movie.title).exists():
        #notificar error
        raise HTTPException(409, 'La pelicula ya se encuentra en la BD.')
    
    movie = Movie.create(
        title = movie.title
    )

    return movie