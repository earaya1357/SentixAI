import streamlit as st
import pandas as pd
import plotly.express as px
from log.logger import log
from db.dbcalls import dbconnect, dbcreate, recordsentimentscoresingle, readsentimentscorehistory
import os, json
from datetime import datetime as dt
from geminiapi import askgemini



#Setup for the page and database for temporary storage

def main(state=False):
    st.set_page_config(layout="wide")
    log('Starting Application')
    if st.session_state.startup == False:
        log('Logging Started.')
        if not os.path.isfile('db/Base.db'):
            log('Starting database')
            dbcreate()
            st.session_state.startup = True
        else:
            log('Database found attempting to connect')
            conn = dbconnect()
            if conn:
                st.session_state.startup = True
                log('Connected to database')
        
    datatable = False
    #Top row in the UI for general text analysis
    with st.container(height=375):    
        
        st.text_area(height=150,label='Input Text',key='sentiment_text', value='This is a phenomenal amazing app! The price is a bit high though')    

        st.text_input(label='Industry')

        if st.button('Analyze Sentiment'):
            log('Starting sentiment analysis')
            try:
                
                jresponse = askgemini(st.session_state.sentiment_text)
                
                if not jresponse:
                    log('No response from Gemini')
                    return
                
                log('Response received from Gemini')
                jresponse = jresponse.replace('`','').replace('json','')
                jresponse = json.loads(jresponse)
                alldata = pd.DataFrame.from_dict(jresponse, orient='index')
                datatable = True

                log('Sentiment analysis successfully completed')
                analysisdata = alldata.transpose()
                tasks = analysisdata['tasks'][0]


                recordsentimentscoresingle(conn, 'TestProduct2', st.session_state.sentiment_text, analysisdata)
            except Exception as e:
                log(e)
                st.write(e)


    #Row to set parameters for the graphs and track progress over time.
    with st.expander('Progress Tracking', expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sub1, sub2 = st.columns(2)
            with sub1:
                st.date_input('Starting Date', value='today', key='start_date')
            with sub2:
                st.date_input('Ending Date', value='today', key='end_date')
            st.text_area(label='Industry Section')
            st.text_area(label='Text Sample Selection', value='Sample information')
        with col2:
            st.write('Sentiment Topics')
            #SAMPLE DATA
            df = pd.DataFrame({'Products':['Prod 1', 'Prod 2', 'Prod 3'], '($) Earnings': [20, 30, 25]})
            p1 = px.bar(df, x='Products', y='($) Earnings')
            st.plotly_chart(p1)
        with col3:
            st.write('Sentiment Topics Over Time')
            #SAMPLE DATA
            df = pd.DataFrame({'Month':['Jan', 'Feb', 'Mar', 'Apr', 'May'], 'Change': [20, 30, 35, 35, 40]})
            p2 = px.line(df, x='Month', y='Change')
            st.plotly_chart(p2)                


    #Row to show the results and actions that should be taken.
    with st.expander('Results and Actions', expanded=True, icon='🔥'):
        col4, col5 = st.columns(2)
        with col4:
            st.write('Results')
            if datatable:
                scores = alldata.loc[['sentiment', 'strength', 'vader_score', 'explanation']]
                st.data_editor(scores, 
                               column_config={
                                   '': 'Metric',
                                   '0': 'Score',
                               },
                               disabled=['Score'])
                log('Generated sentiment score table')
                readsentimentscorehistory(conn=conn, product='TestProduct1')
            else: 
                st.write('Run Sentiment Analysis to display results')

        with col5:
            st.write('Reommended Tasks')
            if datatable:
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



#if __name__ == '__main__':
st.session_state.startup = False
main(st.session_state.startup)

