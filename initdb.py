    

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
import itertools

import db_setup

from db_setup import ThreadsTable, ParagraphsTable, WhoRead, db, app
 

db.drop_all()
db.create_all()

#ThreadsTable.__table__.drop(engine)
#ThreadsTable.__table__.create(engine)

session = db.session




print("db initialized!")   


