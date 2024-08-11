import streamlit as st
import plotly.express as px
from log.logger import log
from db.dbcalls import *
from db.dbcalls import createpart

if st.session_state['loggedin']:
    with st.expander('Add Product to Portfolio', expanded=True):
        newProdForm =  st.form('NewProductForm')
        productname = newProdForm.text_input('Product Name: ')
        description = newProdForm.text_area('Description: ')
        if newProdForm.form_submit_button('Submit'):
            data = {'company': st.session_state['session_info'].company,'productname': productname, 'description': description}
            success = createpart(st.session_state['connection'], data)
            if success == True:
                st.write('Part Created')
            else:
                st.write(success)

    #with st.expander('General Settings'):
    #    apiKeyForm =  st.form('API Key Information')
    #    apiKeyForm.text_input('Gemini API Key: ', type='password')
    #    apiKeyForm.form_submit_button('Submit')

else:
    st.write('Please log in to access setup page')