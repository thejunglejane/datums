from sqlalchemy import create_engine, orm
import os

import datums.models


session = orm.sessionmaker(autoflush=True, autocommit=False)
db_session = orm.scoped_session(session)

# Connect to the database
engine = create_engine(os.environ['DATABASE_URL'])

db_session.configure(bind=engine)
session = db_session()

# Set up the database
models.metadata.create_all(engine)