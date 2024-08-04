import streamlit as st
import pandas as pd
import plotly.express as px
from log.logger import log
from db.dbcalls import *
import os, json
from datetime import datetime as dt
from geminiapi import askgemini, overviewanalysis
import numpy as np
from db.dbcalls import getallparts, sentimentoverview

def createoverview():
    success, history = sentimentoverview(client=st.session_state['connection'], company=st.session_state['session_info'].company, productname=st.session_state['product'])
                
    if success:
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


@st.experimental_fragment
@st.cache_data
def filtersentimentdata(data: pd.DataFrame)->pd.DataFrame:
    data = data.loc[['sentiment', 'strength', 'vader_score', 'explanation']]
    return data


if st.session_state['loggedin']:
    #Setup for the page and database for temporary storage

    st.session_state['startup'] = False
    st.set_page_config(layout="wide")

    st.session_state['datatable'] = False
    st.session_state['edited_data'] = None


    _, product_names = getallparts(st.session_state['connection'], st.session_state['session_info'].company)
    st.text_area(height=150,label='Input Text',key='sentiment_text')    
    st.selectbox(label='Products', options=product_names, key='product')


    if st.button('Analyze Sentiment'):
        log('Starting sentiment analysis')
        try:
            jresponse = askgemini(st.session_state['sentiment_text'])
            if not jresponse:
                log('No response from Gemini')
            log('Response received from Gemini')
            jresponse = jresponse.replace('`','').replace('json','')
            data = dict(json.loads(jresponse))
            alldata = pd.DataFrame.from_dict(data, orient='index')
            st.session_state['datatable'] = True
            log('Sentiment analysis successfully completed')
            analysisdata = alldata.transpose()
            tasks = analysisdata['tasks'][0]

            data['timestamp'] = dt.now()
            data['company'] = st.session_state['session_info'].company
            data['productname'] = st.session_state['product']
            data['comment'] = st.session_state['sentiment_text']

            _, success = recordsentiment(st.session_state['connection'], data)
            st.write(success)
        except Exception as e:
            log(e)
            print(e)

    if st.session_state['datatable']:
        col4, col5 = st.columns(2)
        with col4:
            st.write('Results')
            scores = filtersentimentdata(data=alldata)
            if st.session_state['edited_data']:
                st.session_state['edited_data'] = st.data_editor(st.session_state['edited_data'], 
                            column_config={
                                '': 'Metric',
                                '0': 'Score',
                            },
                            disabled=['Score'])
            else:
                st.session_state['edited_data'] = st.data_editor(scores, 
                            column_config={
                                '': 'Metric',
                                '0': 'Score',
                            },
                            disabled=['Score'])
            log('Generated sentiment score table')
        with col5:
            st.write('Reommended Tasks')
            if st.session_state['datatable']:
                tasksdf = pd.DataFrame({
                    'Complete': False * len(tasks),
                    'Tasks': tasks,
                    'Due Date': [dt.today() ]* len(tasks),
                })
                st.data_editor(tasksdf, 
                            column_config={
                                "Complete": st.column_config.CheckboxColumn("Complete"),
                                'Due Date': st.column_config.DateColumn('Due Date'),
                                },
                            hide_index=True,
                            disabled=['Tasks'])
                log('Generated tasks table')




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
            if st.button('Run Time Sentiment'):
                history = createoverview()
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
            flat_list = [
                x
                for x in history['comment'].values
            ]
        else:
            st.write('')

else:
    st.write('Please log in to access analysis page')