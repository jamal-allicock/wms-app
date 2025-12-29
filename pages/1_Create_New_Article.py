import sqlite3
import streamlit as st
import pandas as pd

conn = sqlite3.connect('master_data.db', check_same_thread=False)
c = conn.cursor()

st.write("WM Inventory")




article_num = st.text_input("Enter the new Article Number: ", placeholder="Type...")
ti = st.text_input("Enter the Ti for this article: ", placeholder="Type...")
hi = st.text_input("Enter the Hi for this article: ", placeholder="Type...")
descr = st.text_input("Enter the description for this article: ", placeholder="Type...")



if st.button("Create New Article:"):
    ti, hi = int(ti), int(hi)
    c.execute("SELECT 1 FROM catalogue WHERE articlenum = ?",
              (article_num,))
    # Ti Hi Check
    if ti<1 or hi<1:
        st.write("Please enter a valid Ti Hi")
    
    # Check if article already exists
    elif c.fetchone() is None:
        c.execute("INSERT INTO catalogue (articlenum, ti, hi, description) VALUES (?, ?, ?, ?)",
                (article_num, ti, hi, descr))
    else:
        st.write("This article already exists. Please enter a new article.")

    conn.commit()

if st.button("Display all Articles"):
    df = pd.read_sql_query("SELECT * FROM catalogue", conn)
    st.write(df.head())