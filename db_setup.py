

# from flask_sqlalchemy import SQLAlchemy

from flask import Flask, request, redirect, url_for, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

from flask_heroku import Heroku

app = Flask(__name__)

import os
import sys
import datetime
import sqlalchemy as sa
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Table, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import create_engine

## long pg uri is heroku hosted, short is local pg
#app.config['SQLALCHEMY_DATABASE_URI'] = ''
engine = create_engine('postgresql://', echo=False)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/evan'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rbikygllddwqic:0b0d4ce5f30bfa9a10a28b5f191246fcf58498312094908e7cbfea24a8de2cab@ec2-54-152-175-141.compute-1.amazonaws.com:5432/d7d9gd9q5q2fpj'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['WHOOSH_BASE'] = 'postgresql://localhost/evan'
#heroku = Heroku(app)
db = SQLAlchemy(app)

Base = declarative_base()


class ThreadsTable(db.Model):
    __tablename__ = 'threads'
    id = Column(Integer, primary_key=True)
    owner = Column(String) 
    title = Column(String) #name of thread
    vis = Column(Boolean, default=True) #false if deleted 
    time_start = Column(DateTime) #when did she start the question
    last_post = Column(DateTime) #when did last post

class ParagraphsTable(db.Model):
    __tablename__ = 'paragraphs'
    id = Column(Integer, primary_key=True) #unique identifter 
    thread_id = Column(Integer, ForeignKey("threads.id"))
    order  = Column(Integer) #order in the thread
    version = Column(Integer) #order for editing
    vis = Column(Boolean, default=True) #is it the current version
    owner = Column(String) 
    text = Column(sa.Text) #name of thread
    thread_title = Column(sa.UnicodeText) #name of thread
    time_start = Column(DateTime) #when did she start the question

class WhoRead(db.Model):
    __tablename__ = 'who_read'
    id = Column(Integer, primary_key=True)
    user = Column(String) 
    thread_id = Column(Integer, ForeignKey("threads.id"))
    read = Column(Boolean, default=False)

class KeyWords(db.Model):
    __tablename__ = 'key_words'
    id = Column(Integer, primary_key=True)
    thread_id = Column(Integer, ForeignKey("threads.id"))
    title = Column(Boolean, default=True)
    word = Column(String)



