import sqlite3
import streamlit as st
import pandas as pd

conn_1 = sqlite3.connect('master_data.db', check_same_thread=False)
c_1 = conn_1.cursor()

c_1.execute('''CREATE TABLE IF NOT EXISTS catalogue (
                articlenum TEXT,
                description TEXT,
                ti INTEGER,
                hi INTEGER)''')



c_1.execute('''CREATE TABLE IF NOT EXISTS inbounds (
                asn TEXT,
                expected_article TEXT,
                expected_cases INTEGER,
                expected_pallets INTEGER,
                received_cases INTEGER,
                received_pallets INTEGER,
                expected_receiving DATETIME,
                actual_receiving_date DATETIME)''')

conn_1.commit()
st.write("WM Inventory")