import streamlit as st

name = st.text_input('name')
if st.button("set name"):
    st.write(name)
    st.session_state['username'] = name