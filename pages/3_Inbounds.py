import sqlite3
import streamlit as st
import pandas as pd

conn = sqlite3.connect('master_data.db', check_same_thread=False)
c = conn.cursor()

asn = st.text_input('Enter ASN: ')
expected_article = st.text_input('Enter Article Number ')
expected_cases = st.text_input('Enter Expected Number of Cases: ')
expected_receiving = st.text_input('Enter Expected Receiving Date: ')

if st.button("Enter Inbound Details"):
    c.execute("SELECT 1 FROM catalogue WHERE articlenum = ?",
              (expected_article,))
    
    if c.fetchone() is None:
        st.write("This article does not exist. Please enter an existing article.")
    else:
        c.execute('''INSERT INTO inbounds (asn, expected_article, expected_cases, expected_receiving) VALUES (?, ?, ?, ?)''',
                (asn, expected_article, expected_cases, expected_receiving))
    conn.commit()
    
st.write("View All Inbounds Below")
df = pd.read_sql_query('SELECT * FROM inbounds', conn)
st.write(df)