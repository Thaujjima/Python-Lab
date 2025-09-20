from utill import print_mult_table 
import pandas
import streamlit as st


st.title ("Dashboard")
st. write ("this application is abount displaying product sales")

upload_file = st.file_uploader("Choose a CSV file", type-"csv")

if upload_file is None:
    st.write("Please upload a CSV file")

else:

    data = pandas.read_csv(upload_file)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Sales", "1,200", "12%")
with col2:
    st.metric("Revenue", "$ 50,000", "5%")
with col3:
    st.metric("User", "$ 15,000", "8%")



st.line_chart(data["sales"])    

if st.checkbox("show table"):
    st.header ("Sales table")
st.subheader ("This is a sales table")
st.write (data)
