from pydantic import BaseModel

class Notification(BaseModel):
    message: str
    title: str | None = None
    priority: int | None = 0

class Data_room(BaseModel):
    room: int
    flor: int
    bed: str
    id_room: int

class Espesific_room(BaseModel):
    espesific_room: int