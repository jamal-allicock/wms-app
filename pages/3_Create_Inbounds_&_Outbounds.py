import sqlite3
import streamlit as st
import pandas as pd
from datetime import datetime

conn = sqlite3.connect('master_data.db', check_same_thread=False)
c = conn.cursor()

## Inbound
st.write("Inbound Form")
asn = st.text_input('Enter ASN: ')
expected_article = st.text_input('Enter Article Number ')
expected_pallets = st.text_input('Enter Expected Number of Pallets: ')
expected_receiving = st.date_input('Enter Expected Receiving Date: ', value=datetime.now())

if st.button("Enter Inbound Details"):

    c.execute("SELECT 1 FROM catalogue WHERE articlenum = ?",
              (expected_article,))
    article_check = c.fetchone()
    c.execute("SELECT 1 FROM inbounds WHERE asn = ?",
              (asn,))
    asn_check = c.fetchone()
    
    # Check if article exists
    if article_check is None:
        st.write("This article does not exist. Please enter an existing article.")
    elif asn_check is not None:
        st.write("This ASN already exists, please enter a new one.")
    else:
        c.execute('''INSERT INTO inbounds (asn, expected_article, expected_pallets, expected_receiving, status) VALUES (?, ?, ?, ?, ?)''',
                (asn, expected_article, expected_pallets, expected_receiving, "IN TRANSIT"))
    conn.commit()
    
## Outbound
st.write("Outbound Form")
asn_ob = st.text_input('Enter OB ASN: ')
expected_article_ob = st.text_input('Enter OB Article Number ')
expected_pallets_ob = st.text_input('Enter Requested Number of OB Pallets: ')
expected_shipping_ob = st.date_input('Enter Expected Shipping Date: ', value=datetime.now())


if st.button("Enter Outbound Details"):

    c.execute("SELECT 1 FROM catalogue WHERE articlenum = ?",
              (expected_article_ob ,))
    article_check = c.fetchone()
    c.execute("SELECT 1 FROM inbounds WHERE asn = ?",
              (asn_ob,))
    asn_check = c.fetchone()
    
    # Check if article exists
    if article_check is None:
        st.write("This article does not exist. Please enter an existing article.")
    elif asn_check is not None:
        st.write("This ASN already exists, please enter a new one.")
    else:
        c.execute('''INSERT INTO outbounds (asn, expected_article, expected_pallets, expected_ship_date, status) VALUES (?, ?, ?, ?, ?)''',
                (asn_ob, expected_article_ob, expected_pallets_ob, expected_shipping_ob, "PENDING"))
    conn.commit()
    
    
st.write("View All Inbounds Below")
df = pd.read_sql_query('''SELECT * FROM inbounds
                            WHERE STATUS = "IN TRANSIT"
                            ORDER BY expected_receiving''', conn)
st.write(df)

st.write("View All Outbounds Below")
df = pd.read_sql_query('''SELECT * FROM outbounds
                       WHERE STATUS = "PENDING"
                       ORDER BY expected_ship_date''', conn)
st.write(df)