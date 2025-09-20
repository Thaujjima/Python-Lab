import streamlit as st




st.title ("Dashboard")
st.write("This application is about displaying product sales")

if 'unername' in st.session_state:
    st.write(f'Hello", {st.session_state ['username']}')
else:
    st.info("Please register at setting page")
    