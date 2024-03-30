from sqlalchemy import *
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import ( scoped_session, sessionmaker, declarative_base )

url = URL(
    drivername='postgresql+psycopg2',
    host='localhost',
    database='pizzashop',
    password='docker',
    username='docker',
    port='5432',
    query={}
)

engine = create_engine(url=url)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
# We will need this for querying
Base.query = db_session.query_property()

def init_db(engine=engine):
  db_session.configure(bind=engine)
  Base.metadata.bind = engine
  Base.metadata.create_all(bind=engine)