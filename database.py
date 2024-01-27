from peewee import *

#nameBD
#user = 'user'
#password = ''
#host = 'localhost'
#port = 3306 #Puerto por default utilizado por MySQL

database = MySQLDatabase('fastapi_project', user = 'root', password = '', host = 'localhost', port = 3306)