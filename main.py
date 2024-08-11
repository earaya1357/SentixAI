import streamlit as st
from db.dbcalls import connection, getuser, createuser
from log.logger import log
from time import sleep
import numpy as np

c1, c2, c3 = st.columns(3)
with c1:
    pass
with c2:
    st.image('material/Sentix AI logo.png', width=300)

with c3:
    pass

st.write('<center><h1>Welcome to Sentix AI</h1></center>', unsafe_allow_html=True)

conn = connection()
st.session_state['connection'] = conn

try:
    if not st.session_state['loggedin']:
        st.session_state['loggedin'] = False
except Exception as e:
    log(f'{e}')
    st.session_state['loggedin'] = False

if not st.session_state['loggedin']:
    with st.expander('Sign In', expanded=True):
        loginform = st.form('Log In')
        username = loginform.text_input('Username')
        password = loginform.text_input('Password', type='password')
        if loginform.form_submit_button('Submit'):
            success, info = getuser(conn, username=username, password=password)
            if success:
                st.session_state['loggedin'] = True
                st.session_state['session_info'] = info
                log(f'User: {st.session_state['session_info'].username}, successfully logged in.')
                st.rerun()
            else:
                log(f'Login failed') 
                st.write(info)

    with st.expander('Sign Up', expanded=False):
        signupform = st.form('Sign Up')
        username = signupform.text_input('Username (Must 5 characters long and contain a number)')
        password = signupform.text_input('Password (Must be 8 characters long and contain at least 1 special character !@#%&)', type='password')
        repassword = signupform.text_input('Re-Password', type='password')
        firstname = signupform.text_input('First Name')
        lastname = signupform.text_input('Last Name')
        email = signupform.text_input('Email')
        age = signupform.text_input('Age')
        company = signupform.text_input('Company')
        if signupform.form_submit_button('Sign Up'):
            try:
                data = {'username': username, 'password': password, 'repassword': repassword, 'firstname': firstname, 'lastname': lastname, 'email': email, 'age': int(age), 'company': company}
                returnval = createuser(client=conn, data=data)
                if isinstance(returnval, bool):
                    st.write('User Successfully Created')
                    sleep(3)
                    st.rerun()
                elif 'User Data Input Error:' in returnval:
                    st.write(returnval)
                
            except Exception as e:
                st.write(e)


if st.session_state['loggedin']:
    st.write(f'<h3>Welcome {st.session_state['session_info'].username}</h3>', unsafe_allow_html=True)

            
