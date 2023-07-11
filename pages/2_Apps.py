import streamlit_authenticator as stauth
import streamlit as st
import yaml
from yaml.loader import SafeLoader

with open('credentials.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)


name, authentication_status, username = authenticator.login('Login', 'main')


def sidebar_menu():
    with st.sidebar:
        st.write(f'Welcome *{name}*')
        authenticator.logout('Logout', 'main')

if authentication_status:
    st.title('Some content')
    sidebar_menu()
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
