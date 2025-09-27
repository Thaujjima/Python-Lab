import streamlit as st
st.title("Rectangle Area Calculator")

width = st.number_input("width")
height = st.number_input("height")
if st.button("calculate area"):
    st.write("area =", width * height)