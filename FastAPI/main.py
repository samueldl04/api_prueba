from fastapi import FastAPI
from pydantic import BaseModel


class Libro(BaseModel):
    id: int
    title: str
    descriptions: dict
    nro_paginas: int

lista_libros = [Libro(id=1, title= "titulo1", descriptions={"descripcion1": "descripcion libro 1"}, nro_paginas=100), 
                Libro(id=2, title="titulo2", descriptions= {"descripcion2": "descripcion libro 2"}, nro_paginas=200)]
app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/libro/{item_id}")
async def read_item(item_id: int):
    resultado = buscar_libro(item_id)

def buscar_libro(item_id):
    libro = filter(lambda Libro: Libro.id == item_id, lista_libros)
    return list(libro)