from sqlalchemy import create_engine
from database_service.settings import Settings

engine = create_engine(Settings.CONNECTION_STRING)
