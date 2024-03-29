from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()


USERNAME=os.getenv("DB_USERNAME")
PASSWORD=os.getenv("DB_PASSWORD")
HOST=os.getenv("DB_HOST")
PORT=os.getenv("DB_PORT")
DBNAME=os.getenv("DB_DBNAME")

DB_URL = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"

class engineconn:

    def __init__(self):
        self.engine = create_engine(DB_URL, pool_recycle = 500)

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn