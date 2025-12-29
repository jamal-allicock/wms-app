import sqlite3
import streamlit as st
import pandas as pd
from datetime import datetime

conn = sqlite3.connect('master_data.db', check_same_thread=False)
c=conn.cursor()

st.write("Confirm IB Details")
asn_ib = st.text_input("Enter ASN for Inbound Received")
pallets_received = (st.text_input("Enter # of pallets Received"))

if st.button("Enter Received Inbound"):
    pallets_received = int(pallets_received)
    # Check as if ASN exists
    c.execute("SELECT * FROM inbounds WHERE asn = ? AND status = ?", (asn_ib, "IN TRANSIT"))
    asn_row = c.fetchone()
    if asn_row is None:
        st.write("This ASN does not exist")
    elif pallets_received < 0:
        st.write("Please enter a valid receiving quantity")
    else:
        st.write(asn_row)
        article_received = asn_row[1]
        c.execute("SELECT * FROM catalogue WHERE articlenum = ?", (article_received,))
        article_row=c.fetchone()
        description=article_row[1]
        cases=article_row[2]*article_row[3]
        receiving_date=datetime.now()
        for i in range(pallets_received):

            c.execute('''INSERT INTO inventory (articlenum, description, cases, code_date) VALUES (?, ?, ?, ?)''', 
                      (article_received, description, cases, datetime.now()))
        c.execute("UPDATE inbounds SET status = ? WHERE asn = ?", ("RECEIVED", asn_ib))
        
    conn.commit()
    
st.write("Confirm OB Details")
asn_ob = st.text_input("Enter ASN for Outbound Shipped")