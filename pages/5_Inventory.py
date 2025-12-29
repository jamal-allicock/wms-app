import sqlite3
import streamlit as st
import pandas as pd

conn = sqlite3.connect('master_data.db', check_same_thread=False)
c = conn.cursor()

df = pd.read_sql_query('SELECT * FROM inventory', conn)
st.write(df)