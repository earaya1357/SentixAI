import sqlite3 as sql
from pydantic import validate_call
from log.logger import log
import streamlit as st
import pandas as pd
from datetime import datetime as dt
from typing import Union
from sqlalchemy import create_engine 


#@validate_call
def dbcreate() -> Union[None, str]:
    try:
        with sql.connect('db/Base.db') as conn:
            log('Created Database')
            cur = conn.cursor()
            
            cur.execute('CREATE TABLE IF NOT EXISTS CompanyInfo(name TEXT, key TEXT)')
            log('Created Table: CompanyInfo')
            
            cur.execute('CREATE TABLE IF NOT EXISTS Products(id INTEGER PRIMARY KEY AUTOINCREMENT, productname TEXT, comment TEXT)')
            log('Created Table: Products')
            
            cur.execute('CREATE TABLE IF NOT EXISTS SingleSentiment(id INTEGER PRIMARY KEY AUTOINCREMENT, Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, productname TEXT, comment TEXT, sentiment TEXT, strength INTEGER, vader_score REAL, explanation TEXT, tasks TEXT)')
            log('Created Table: SingleSentiment')
            
            conn.commit()
            
    except Exception as e:
        log(f'Database Creation Error: {e}')
        return str(e)

    return None
    
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
    

def readsentimentscorehistory(product: str) -> Union[pd.DataFrame, str]:
    try:
        log('Attempting to connect and read sentiment history')
        engine = create_engine('sqlite:///db/Base.db')
        df = pd.read_sql(f"SELECT productname, Timestamp, comment, sentiment, strength, vader_score FROM SingleSentiment WHERE productname='{product}'", 
                         engine)
        df = df.rename({'productname': 'Name', 'Timestamp': 'TimeStamp', 'comment':'Comment', 'sentiment':'Sentiment', 'strength': 'Strength', 'vader_score': 'VaderScore'})
        return df
    except Exception as e:
        log(f"An error occurred: {e}")
        return str(e)

def addproduct(conn: sql.Connection, product_name: str)->str|None:
    try:
        log('Attempting to record product name.')
        cur = conn.cursor()
        cur.execute(f"INSERT INTO Products(productname) VALUES('{product_name}')")
        conn.commit()
        log('Product recorded successfully')
    except Exception as e:
        log(e)
        return e
    
def getproductnames(conn: sql.Connection)->list[str]|str:
    try:
        log('Attempting to get product names.')
        conn.row_factory = lambda cursor, row: row[0]
        cur = conn.cursor()
        cur.execute("SELECT productname FROM Products")
        data = cur.fetchall()
        conn.commit()
        log('Product recordeds successfully retrieved')
        return data
    except Exception as e:
        log(e)
        return e