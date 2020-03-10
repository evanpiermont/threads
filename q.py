    

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import flask_whooshalchemyplus

 
import itertools

import db_setup

from db_setup import ThreadsTable, ParagraphsTable, WhoRead, KeyWords, db, app
session = db.session

kw = session.query(KeyWords).all()

kws = []
for k in kw:
    kws.append(k.word)

print(kws)
