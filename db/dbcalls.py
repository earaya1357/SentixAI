import sqlite3 as sql
from pydantic import validate_call
from log.logger import log
import streamlit as st
import pandas as pd

#@validate_call
def dbcreate(dbname:str)->None:
    try:
        conn = sql.connect(f'db/{dbname}.db')
        log('Created Database')
        cur = conn.cursor()
        cur.execute('CREATE TABLE CompanyInfo(name, key)')
        cur.execute('CREATE TABLE Products(id, productname, comment)')
        cur.execute('CREATE TABLE SingleSentiment(id, productname, comment, sentiment, strength, vader_score, explanation, tasks)')
        conn.commit()
        conn.close()
    except Exception as e:
        log(e)
        return e
    
def dbconnect(dbname:str)->sql.Connection|str:
    try:
        log('Connecting to database')
        conn = sql.connect(f'db/{dbname}.db')
        return conn
    except Exception as e:
        log(e)
        return e

#@validate_call
def recordsentimentscoresingle(conn: sql.Connection, data:pd.DataFrame)->str|None:
    try:
        log('Attempting to record single sentiment analysis.')
        cur = conn.cursor()
        cur.execute('')
        conn.commit()
        log('Single sentiment analysis recorded successfully')
        return None
    except Exception as e:
        log(e)
        return e
    
@st.experimental_dialog("Database Setup")
def dbsetup():
    st.write(f"Please create a name for your database")
    dbname = st.text_input(label='Database Name')
    if st.button("Submit"):
        dbcreate(f'{dbname}')
        st.rerun()
