from utill import print_mult_table 
import pandas
import streamlit as st

data = pandas.read_csv("Products.csv")

st.title ("Dashboard")
st. write ("this application is abount displaying product sales")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Sales", "1,200", "12%")
with col2:
    st.metric("Revenue", "$ 50,000", "5%")
with col3:
    st.metric("User", "$ 15,000", "8%")

st.header ("Sales table")
st.subheader ("This is a sales table")
st.write (data)
