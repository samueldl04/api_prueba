from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Importa la variable Base desde tu modelo
from app.db.base import Base
from app.core.config import settings

# Importa todos tus modelos para que Alembic los reconozca
import app.models

# Esta es la configuración de Alembic que se usa cuando los archivos de revisión
# son ejecutados de forma automática.
config = context.config

# Interpreta el archivo de configuración para el registro de Python
fileConfig(config.config_file_name)

# Añade aquí los metadatos de tu modelo
target_metadata = Base.metadata

# Otros valores de context.configure
config.set_main_option("sqlalchemy.url", settings.SQLALCHEMY_DATABASE_URL)

def run_migrations_offline():
    """Ejecuta migraciones en modo 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Ejecuta migraciones en modo 'online'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            compare_type=True,  # Compara tipos para migración
            compare_server_default=True  # Compara defaults para migración
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()