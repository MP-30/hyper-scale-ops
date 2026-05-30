from fastapi import  APIRouter

v1 = APIRouter()

@v1.get('/hello-aditya')
def hello():
    return  ("Hello-aditay")
