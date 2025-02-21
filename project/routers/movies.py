from fastapi import HTTPException, APIRouter
from ..database import Movie
from ..schemas import MovieRequestModel, MovieResponseModel
from typing import List

router = APIRouter(prefix = '/movies')

@router.post('', response_model = MovieResponseModel)
async def create_movies(movie : MovieRequestModel):

    if Movie.select().where(Movie.title == movie.title).exists():
        #notificar error
        raise HTTPException(409, 'La pelicula ya se encuentra en la BD.')
    
    movie = Movie.create(
        title = movie.title
    )

    return movie

@router.get('', response_model = List[MovieResponseModel])
async def get_movies():

    moviess = Movie.select()

    return [movies for movies in moviess]

@router.get('/{title}', response_model = MovieResponseModel)
async def get_movie(title: str):

    movie = Movie.select().where(Movie.title == title).first()

    if movie is None:
        raise HTTPException(404, detail = 'Movie not found')

    return movie
