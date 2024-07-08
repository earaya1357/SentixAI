import streamlit as st
from sentimentapi import basicsentiment
import requests
import pandas as pd
import plotly.express as px

#COLUMNS = ['Sentiment', 'Strength', 'Vader Score', 'Explanation', 'Tasks']
st.set_page_config(layout="wide")
inputcol, graphcol1, graphcol2 = st.columns(3)

with st.sidebar:
    company = st.selectbox('Company', ['Company A', 'Company B'], )
    products = st.selectbox('Products', ['Item 1', 'Item 2', 'Item 3', 'Item 4'])

with inputcol:    
    st.text_area(height=200,label='Text to Analyze',key='sentiment_text', value='This is a phenomenal amazing app! The price is a bit high though')    

    if st.button('Run sentiment'):
        params = {'comment': st.session_state.sentiment_text}
        response = requests.get(f'http://127.0.0.1:8000/basicsentiment/company/product', params=params)
        
        if response.status_code != 200:
            st.write(response.status_code)
        
        jresponse = response.json()
        alldata = pd.DataFrame.from_dict(jresponse['answer'], orient='index')
        #alldata = alldata.transpose()
        st.table(alldata)

with graphcol1:
    st.button('test')

with graphcol2:
    st.button('test2')
