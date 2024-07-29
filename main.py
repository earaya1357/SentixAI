import streamlit as st
from streamlit_option_menu import option_menu
from db.dbcalls import connection, getuser, createuser
from log.logger import log

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
            else:
                log(f'Login failed') 
                st.write(info)

    with st.expander('Sign Up', expanded=False):
        signupform = st.form('Sign Up')
        username = signupform.text_input('Username')
        password = signupform.text_input('Password', type='password')
        repassword = signupform.text_input('Re-Password', type='password')
        firstname = signupform.text_input('First Name')
        lastname = signupform.text_input('Last Name')
        email = signupform.text_input('Email')
        age = signupform.text_input('Age')
        company = signupform.text_input('Company')
        if signupform.form_submit_button('Sign Up'):
            if password == repassword:
                data = {'username': username, 'password': password, 'repassword': repassword, 'firstname': firstname, 'lastname': lastname, 'email': email, 'age': int(age), 'company': company}
                returnval = createuser(client=conn, data=data)
                st.write(returnval)

if st.session_state['loggedin']:
    st.write(f'<h2>Welcome {st.session_state['session_info'].username}</h2>', unsafe_allow_html=True)

            
