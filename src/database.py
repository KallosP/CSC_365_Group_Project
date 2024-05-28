import os
import dotenv
from sqlalchemy import create_engine, MetaData, Table

# Establishes a connection to the database setup in Supabase
def database_connection_url():
    dotenv.load_dotenv("../../.env")

    return os.environ.get("POSTGRES_URI")

engine = create_engine(database_connection_url(), pool_pre_ping=True)
metadata = MetaData()

tasks_table = Table('tasks', metadata, autoload_with=engine)
tags_table = Table('tags', metadata, autoload_with=engine)
users_table = Table('users', metadata, autoload_with=engine)