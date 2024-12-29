import streamlit as st
import pandas as pd
import duckdb

conn = duckdb.connect()


st.set_page_config(page_title='核新云', layout='centered')


st.title('搜索DCS信息构建PSA图形')

hasHeader = st.checkbox('有表头（无表头则默认列名为0，1，2，3...）', value=True)
    
uploaded_file = st.file_uploader('选择文件', ['xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt'])

if uploaded_file is not None:
    dataframes = pd.read_excel(uploaded_file, sheet_name=None, header= 'a' if hasHeader else None)
    # dataframes = pd.read_excel(uploaded_file, sheet_name=None, header= 0 if hasHeader else None, names=headerNames.split(',') if headerNames else None)
    tabs = st.tabs(dataframes.keys())
    
    for index, (name, df) in enumerate(dataframes.items()):
        conn.execute(f'CREATE TABLE {name} AS SELECT * FROM df;')
        tabs[index].write(conn.execute(f'SELECT * FROM {name};').df())


query = st.text_area('查询')
if query:
    st.write(conn.execute(query).df())


footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>&copy 核新云科技（南京）有限公司</p>
</div>
"""

st.markdown(footer,unsafe_allow_html=True)