import streamlit as st
import pandas as pd
import duckdb

conn = duckdb.connect()



st.title('Use SQL to Search Excel')


hasHeader = st.checkbox('has header', value=True)
headerNames = '' if hasHeader else st.text_input('Header Names')
    
uploaded_file = st.file_uploader('选择文件', ['xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt'])

if uploaded_file is not None:
    dataframes = pd.read_excel(uploaded_file, sheet_name=None, header= 0 if hasHeader else None, names=headerNames.split(',') if headerNames else None)
    tabs = st.tabs(dataframes.keys())
    
    for index, (name, df) in enumerate(dataframes.items()):
        conn.execute(f'CREATE TABLE {name} AS SELECT * FROM df;')
        tabs[index].write(conn.execute(f'SELECT * FROM {name};').df())


query = st.text_area('查询')
if query:
    st.write(conn.execute(query).df())