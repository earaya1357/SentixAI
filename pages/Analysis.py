import streamlit as st
import pandas as pd
import plotly.express as px
from log.logger import log
from db.dbcalls import *
import os, json
from datetime import datetime as dt
import dateutil.parser as parser
from geminiapi import askgemini, overviewanalysis
import numpy as np
from db.dbcalls import getallparts, sentimentoverview

def createoverview(start_date: str, end_date:str):
    start_date = parser.parse(start_date)
    end_date = parser.parse(end_date)
    success, history = sentimentoverview(client=st.session_state['connection'], company=st.session_state['session_info'].company, productname=st.session_state['product'], start_date=start_date, end_date=end_date)

    try:
        if success:
            if not isinstance(history, str):
                history = pd.DataFrame(history)
                with col2:
                    st.write('Sentiment Topics')
                    df = history['sentiment'].value_counts().reset_index()
                    p1 = px.bar(data_frame=df, x='sentiment', y='count', labels={'sentiment':'Sentiment', 'count':'Count'}, color='sentiment')
                    st.plotly_chart(p1)
                with col3:
                    st.write('Sentiment Topics Over Time')
                    p2 = px.line(history, x='timestamp', y='vader_score', markers=True, labels={'timestamp':'Time Stamp', 'vader_score':'Vader Score'})
                    st.plotly_chart(p2)  
                return history
        else:
            st.write('Query could not complete')
    except Exception as e:
        log(f'Error running sentiment history: {e}')
        st.write('No data found in current date range')


if st.session_state['loggedin']:
    #Setup for the page and database for temporary storage

    st.session_state['startup'] = False
    st.set_page_config(layout="wide")

    st.session_state['datatable'] = False
    st.session_state['edited_data'] = None

    _, product_names = getallparts(st.session_state['connection'], st.session_state['session_info'].company)
    st.text_area(height=150,label='Input Text',key='sentiment_text')    
    st.selectbox(label='Products', options=product_names, key='product')


    #Row to set parameters for the graphs and track progress over time.
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            sub1, sub2 = st.columns(2)
            with sub1:
                st.date_input('Starting Date', value='today', key='start_date')
            with sub2:
                st.date_input('Ending Date', value='today', key='end_date')
            history=None

            #Run Analysis when the button is pressed.
            if st.button('Run Time Sentiment'):
                if st.session_state['sentiment_text']:
                    try:
                        jresponse = askgemini(st.session_state['sentiment_text'])
                        if not jresponse:
                            log('No response from Gemini')
                        log('Response received from Gemini')
                        jresponse = jresponse.replace('`','').replace('json','')
                        data = dict(json.loads(jresponse))
                        data['timestamp'] = dt.now()
                        data['company'] = st.session_state['session_info'].company
                        data['productname'] = st.session_state['product']
                        data['comment'] = st.session_state['sentiment_text']
                        _, success = recordsentiment(st.session_state['connection'], data)
                        st.write(success)
                    except Exception as e:
                        log(e)
                        st.write('Unable to new record data. Continuing to retrieve current data.')
                history = createoverview(str(st.session_state['start_date']), str(st.session_state['end_date']))
                st.session_state['history'] = history
                
        if isinstance(history, pd.DataFrame): 
            flat_list = [
                x
                for x in history['comment'].values
            ]
            st.divider()
            answer = overviewanalysis(flat_list)
            st.session_state['current_answer'] = answer
            st.write(answer)
            st.download_button('Download Analysis Highlights', st.session_state['current_answer'], 'Analysis.txt', mime='text/txt')
            st.divider()
            st.dataframe(st.session_state['history'], width=1800, selection_mode=['multi-column', 'multi-row'])
            
        else:
            st.write('')

else:
    st.write('Please log in to access analysis page')