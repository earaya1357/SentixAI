import streamlit as st
from sentimentapi import basicsentiment
import requests
import pandas as pd
import plotly.express as px
import numpy as np

#COLUMNS = ['Sentiment', 'Strength', 'Vader Score', 'Explanation', 'Tasks']
st.set_page_config(layout="wide")

with st.container(height=375):    
    st.text_area(height=150,label='Input Text',key='sentiment_text', value='This is a phenomenal amazing app! The price is a bit high though')    

    st.text_input(label='Industry')

    if st.button('Analyze Sentiment'):
        params = {'comment': st.session_state.sentiment_text}
        response = requests.get(f'http://127.0.0.1:8000/basicsentiment/company/product', params=params)
        
        if response.status_code != 200:
            st.write(response.status_code)
        
        jresponse = response.json()
        alldata = pd.DataFrame.from_dict(jresponse['answer'], orient='index')
        #alldata = alldata.transpose()
        st.table(alldata)

with st.expander('Progress Tracking'):
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
        df = pd.DataFrame({'Products':['Prod 1', 'Prod 2', 'Prod 3'], '($) Earnings': [20, 30, 25]})
        p1 = px.bar(df, x='Products', y='($) Earnings')
        st.plotly_chart(p1)
    with col3:
        st.write('Sentiment Topics Over Time')
        df = pd.DataFrame({'Month':['Jan', 'Feb', 'Mar', 'Apr', 'May'], 'Change': [20, 30, 35, 35, 40]})
        p2 = px.line(df, x='Month', y='Change')
        st.plotly_chart(p2)

with st.expander('Results and Actions'):
    col4, col5 = st.columns(2)
    with col4:
        st.text_area(label='Results', value='Results of the sentiment')

    with col5:
        st.text_area(label='Reommended Tasks', value='Tasks to try from sentment')
