import asyncio
import pandas as pd
import streamlit as st
from utils import consumer
from utils_anom import consumer_anom

st.set_page_config(page_title="stream", layout="wide")

def run_ws_connection(selected_channels, columns, window_size, status, st_df):
    try:
        asyncio.run(consumer(dict(zip(selected_channels, columns)), selected_channels, window_size, status, st_df))
    except Exception as e:
        print("1:", e)

def run_ws_connection_2(selected_channels, columns, window_size, status, st_df):
    try:
        asyncio.run(consumer_anom(dict(zip(selected_channels, columns)), selected_channels, window_size, status, st_df))
    except Exception as e:
        print("2:", e)

status_1 = st.empty()
status_2 = st.empty()

connect_1 = st.checkbox("Connect to WS Server 1")
connect_2 = st.checkbox("Connect to WS Server 2")

if connect_1 or connect_2:
    selected_channels_1 = []
    columns_1 = []
    selected_channels_2 = []
    columns_2 = []

    if connect_1:
        selected_channels_1 = st.multiselect("Select Channels (Server 1)", ["A", "B", "C"], default=["A"])
        columns_1 = [col.empty() for col in st.columns(len(selected_channels_1))]
        window_size_1 = st.number_input("Window Size (Server 1)", min_value=10, max_value=100)
        st_df_1 = st.empty()

    if connect_2:
        selected_channels_2 = st.multiselect("Select Channels (Server 2)", ["X", "Y", "Z"], default=["X"])
        columns_2 = [col.empty() for col in st.columns(len(selected_channels_2))]
        window_size_2 = st.number_input("Window Size (Server 2)", min_value=10, max_value=100)
        st_df_2 = st.empty()

    if connect_1:
        ws_task_1 = asyncio.create_task(run_ws_connection(selected_channels_1, columns_1, window_size_1, status_1, st_df_1))
    else:
        status_1.subheader("Disconnected.")

    if connect_2:
        ws_task_2 = asyncio.create_task(run_ws_connection_2(selected_channels_2, columns_2, window_size_2, status_2, st_df_2))
    else:
        status_2.subheader("Disconnected.")
else:
    status_1.subheader("Disconnected.")
    status_2.subheader("Disconnected.")

print("The app is running -- stream")
