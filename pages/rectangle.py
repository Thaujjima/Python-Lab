import streamlit as st
name = st.text_input("name")
st.write(name)

width = st.number_input("width")
height = st.number_input("height")
if st.button("calculate area"):
    st.write("area =", width * height)