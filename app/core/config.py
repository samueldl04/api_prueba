import json
from pathlib import Path
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "Aplicación de Fichajes"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Parámetros para MySQL
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: str
    MYSQL_DATABASE: str

    # URL de conexión 
    SQLALCHEMY_DATABASE_URL: str = None

    SECRET_KEY: str = "clave"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        case_sensitive = True

    def __init__(self, **data):
        super().__init__(**data)
        if not self.SQLALCHEMY_DATABASE_URL:
            self.SQLALCHEMY_DATABASE_URL = (
                f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
                f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
            )

BASE_DIR = Path(__file__).resolve().parent.parent  # Sube dos niveles

def load_settings_from_file(filename: str) -> Settings:
    filepath = BASE_DIR / filename
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return Settings(**data)

# Carga la configuración desde el fichero config.json y crea una instancia de Settings
settings = load_settings_from_file("config.json")