from __future__ import division
from flask import Flask, request, redirect, url_for, render_template, jsonify, Markup

import os
import hashlib
import datetime, time, json, requests
from datetime import datetime, timedelta
from os import curdir, sep
from http.server import BaseHTTPRequestHandler, HTTPServer

# from flask_heroku import Heroku

from random import randint
import random
import re

from db_setup import ThreadsTable, ParagraphsTable, WhoRead, KeyWords, db, app

import cgi
import collections, itertools

session = db.session

####
#####
######
####### __init__
######
#####
####
 
userlist = ['suj', 'bean']


####
#####
######
####### LOGIN PAGE
######
#####
####

@app.route('/')
@app.route('/login')
def Login():


    return render_template('login.html', text='Enter user.',
        action='/landing',
        input=True,
        v=True)


@app.route('/landing', methods=['POST', 'GET'])
def Land():

    user=request.form['subject_id'].lower()


    if user in userlist:

        return redirect(url_for('Threads', user=user), code=302)
  
    else:
        
        return render_template('login.html', text='Enter a user.',
            action='/landing',
            input=True,
            v=True)


@app.route('/threads/<user>', methods=['POST', 'GET'])
def Threads(user):

    if user in userlist:

        return render_template('threads.html', user=user,)

    else:
        return render_template('login.html', text='Enter a user.',
            action='/landing',
            input=True,
            v=True)


@app.route('/new/<user>', methods=['POST'])
def New(user,):

    if user in userlist:


        new_thread=request.form['new_thread'].lower()
        keys = new_thread.split()

        nt = ThreadsTable(
                owner = user,
                time_start = datetime.now(),
                last_post = datetime.now(),
                title = new_thread)    
        session.add(nt)
        session.commit()


        #get the current thread id, the one that just got made, for the redirect

        ctid = session.query(ThreadsTable).order_by(ThreadsTable.id.desc()).first().id

        for key in keys:
            nkw = KeyWords(
                thread_id = ctid,
                word = key)    
            session.add(nkw)
            session.commit()

        for user_i in userlist:
            wr = WhoRead(
                user = user_i,
                thread_id = ctid,
                read = False)
            if user_i == user:
                wr.read = True
            session.add(wr)
            session.commit()


 
        return redirect(url_for('Thread', user=user, thread_id=ctid), code=302)

    else:
        
        return redirect(url_for('Threads', user=user), code=302)


@app.route('/thread/<user>/<thread_id>', methods=['POST', 'GET'])
def Thread(user, thread_id):

    if user in userlist:

        t = session.query(ThreadsTable).filter(ThreadsTable.id == thread_id).one()
        r = session.query(WhoRead).filter(WhoRead.thread_id == t.id).filter(WhoRead.user == user).one()

        r.read = True
        session.add(r)
        session.commit()
    
        return render_template('thread.html',
            thread_id=thread_id,
            thread_title=t.title,
            thread_owner=t.owner,
            thread_time_start=t.time_start.strftime("%b %d, %Y; %H:%m"),
            user=user)

    else:
        
        return redirect(url_for('Threads', user=user), code=302)

@app.route('/_get_threads', methods=['POST'])
def GetThreadsJSON():


    #filters=json.loads(request.form['filters'])
    user=request.form['user']

    ts = session.query(ThreadsTable).order_by(ThreadsTable.last_post.desc()).all()

    threads = {}
    thread_index = []
    index = 0
    for t in ts:
        kw_t = session.query(KeyWords).filter(KeyWords.thread_id == t.id) .filter(KeyWords.title == True).all()
        kw_p = session.query(KeyWords).filter(KeyWords.thread_id == t.id).filter(KeyWords.title == False).all()
        kws_t = []
        for k in kw_t:
            kws_t.append(k.word)
        kws_p = []
        for k in kw_p:
            kws_p.append(k.word)
        r = session.query(WhoRead).filter(WhoRead.thread_id == t.id).filter(WhoRead.user == user).one()
        thread_index.append(t.id)
        my_dict = {
            'owner' : t.owner,
            'time_start' : t.time_start.strftime("%b %d, %Y"),
            'last_post' : t.last_post.strftime("%b %d, %Y; %H:%M"),
            'title' : t.title,
            'read' : r.read,
            'keywords_t' : kws_t,
            'keywords_p' : kws_p}
        threads[t.id] = my_dict
    paras = {}
  
    return jsonify(threads = threads,
                   thread_index = thread_index)

@app.route('/_get_paras', methods=['POST'])
def GetParasJSON():

    thread_id=request.form['thread_id']
    ps = session.query(ParagraphsTable).filter(ParagraphsTable.thread_id == thread_id).all()

    paras = {}
    for p in ps:
        my_dict = {
            'owner' : p.owner,
            'order' : p.order,
            'date_start' : p.time_start.strftime("%b %d, %Y"),
            'time_start' : p.time_start.strftime("%H:%M:%S"),
            'text' : p.text}
        paras[p.id] = my_dict
  
    return jsonify(paras = paras)


@app.route('/_post_para', methods=['POST'])
def PostParaJSON():

    #filters=json.loads(request.form['filters'])

    owner=request.form['owner']
    text=request.form['text']
    #find all keywords, hashtaged, make octothorps bold
    kws = re.findall(r"(?<!\\)(?:^|\s)#(\w+)", text)
    text = re.sub(r'(?<!\\)(?:^|\s)#(\w+)', r' <span class=kw>\1</span>', text)
    #create links, of the form [link text](link)
    text = re.sub(r'(?<!\\)\[(.*?)\]\((.*?)\)', create_link, text)
    #create typewritter
    text = re.sub(r'(?<!\\)\^(.*?)\^', r'<span class=ttt>\1</span>', text)
    #create bold
    text = re.sub(r'(?<!\\)\*(.*?)\*', r'<span class=bold>\1</span>', text)
    #create italics
    text = re.sub(r'(?<!\\)\_(.*?)\_', r'<em>\1</em>', text)
    #create display math
    text = re.sub(r'(?<!\\)\$\$(.*?)\$\$', r'<div class=math>\1</div>', text)
    #create inline math
    text = re.sub(r'(?<!\\)\$(.*?)\$', r'<span class=math>\1</span>', text)
    #create escape chars
    text = re.sub(r'\\\#', r'^', text)
    text = re.sub(r'\\\^', r'^', text)
    text = re.sub(r'\\\$', r'$', text)
    text = re.sub(r'\\\*', r'*', text)
    text = re.sub(r'\\\_', r'_', text)
    thread_id=request.form['thread_id']
    next_para = int(request.form['para_num']) + 1

    np = ParagraphsTable(
                thread_id=thread_id,
                owner = owner,
                order = next_para,
                version=0,
                vis=True,
                time_start = datetime.now(),
                text = text)

    session.add(np)
    #session.commit()

    for kw in kws:
        nkw = KeyWords(
            thread_id=thread_id,
            title = False,
            word = kw,
            )
        session.add(nkw)


    t = session.query(ThreadsTable).filter(ThreadsTable.id == thread_id).one()
    t.last_post = datetime.now()

    for user_i in userlist:
        wr = session.query(WhoRead).filter(WhoRead.thread_id == thread_id).filter(WhoRead.user == user_i).one()
        wr.read = False
        if user_i == owner:
            wr.read = True
        session.add(wr)
        session.commit()

    session.add(t)
    session.commit()

    return jsonify(para = 'para')

#### regex functions

def create_link(match):
    match = match.group()
    link = re.search(r'\((.*?)\)', match).group(1)
    link_text = re.search(r'\[(.*?)\]', match).group(1)
    return '<a class=regex_link href='+link+'>'+link_text+'</a>'

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')

 