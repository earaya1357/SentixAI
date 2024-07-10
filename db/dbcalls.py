import sqlite3 as sql
from pydantic import validate_call
from log.logger import log
import streamlit as st
import pandas as pd
from datetime import datetime as dt

#@validate_call
def dbcreate()->None:
    try:
        conn = sql.connect(f'db/Base.db')
        log('Created Database')
        cur = conn.cursor()
        cur.execute('CREATE TABLE  IF NOT EXISTS CompanyInfo(name TEXT, key TEXT)')
        conn.commit()
        cur.execute('CREATE TABLE IF NOT EXISTS Products(id INTEGER PRIMARY KEY AUTOINCREMENT, productname TEXT, comment TEXT)')
        conn.commit()
        cur.execute('CREATE TABLE IF NOT EXISTS SingleSentiment(id INTEGER PRIMARY KEY AUTOINCREMENT, Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, productname TEXT, comment TEXT, sentiment REAL, strength INTEGER, vader_score REAL, explanation TEXT, tasks TEXT)')
        conn.commit()
        conn.close()
        log('Created Tables CompanyInfo, Products, SingleSentiment')
    except Exception as e:
        log(f'Database Creation: {e}')
        print(e)
        return e
    
def dbconnect()->sql.Connection|str:
    try:
        log('Connecting to database')
        conn = sql.connect(f'db/Base.db')
        return conn
    except Exception as e:
        log(e)
        return e

#@validate_call
def recordsentimentscoresingle(conn: sql.Connection, product:str, comment:str, data:pd.DataFrame)->str|None:
    try:
        log('Attempting to record single sentiment analysis.')
        cur = conn.cursor()
        cur.execute('INSERT INTO SingleSentiment(productname, comment, sentiment, strength, vader_score, explanation, tasks) VALUES(?, ?, ?, ?, ?, ?, ?)', (product, comment, data['sentiment'][0], data['strength'][0], data['vader_score'][0], data['explanation'][0], str(data['tasks'][0])))
        conn.commit()
        log('Single sentiment analysis recorded successfully')
        return 'Success'
    except Exception as e:
        log(e)
        return e
    

def readsentimentscorehistory(conn: sql.Connection, product: str)->pd.DataFrame:
    try:
        log('Attmpting to connect and ready sentiment history')
        #cur = conn.cursor()
        q = 'SELECT * from SingleSentiment WHERE productname=TestProduct1'
        df = pd.read_sql_query(q, conn)
        #res = cur.execute('SELECT * from SingleSentiment WHERE productname=?', (product))
        #res.fetchall()
        print(df.head())
    except Exception as e:
        log(e)
        return e
