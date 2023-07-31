import asyncio
import json
from time import sleep

import loguru

import aiohttp
from collections import deque, defaultdict
from functools import partial
from os import getenv

import pandas as pd
import streamlit
import streamlit as st

from utils import consumer

from loguru import logger

logger.add("debug.log")


async def consumer_anom(status, st_df, st_df_1_1):
    WS_CONN = "ws://localhost:8000/anomalities"

    async with aiohttp.ClientSession(trust_env=True) as session:
        # status.subheader(f"Connecting to {WS_CONN}")
        async with session.ws_connect(WS_CONN) as websocket:
            # status.subheader(f"Connected to: {WS_CONN}")
            # print("2 Connected to: ", WS_CONN)
            async for message in websocket:
                data = message.json()
                try:
                    # id data is empty
                    if not data:
                        print("No data")
                    else:
                        # data is {"anomalies": an_count, "non_anomalies": non_an_count}
                        anomaly_count = data["anomalies"]
                        non_anomaly_count = data["non_anomalies"]
                        # style red, font size 20
                        st_df.markdown(f'<p style="color: red; font-size: 20px;">Anomaly count: {anomaly_count}</p>', unsafe_allow_html=True)
                        st_df_1_1.markdown(f'<p style="color: green; font-size: 20px;">Non-Anomaly count: {non_anomaly_count}</p>', unsafe_allow_html=True)
                        pass

                except Exception as e:
                    if e != "TypeError: string indices must be integers":
                        print(e)
                    else:
                        print("1 ")


async def consumer_interfaces(status, st_df):
    WS_CONN = "ws://localhost:8000/interfaces"
    # windows = defaultdict(partial(deque, [0]*window_size, maxlen=window_size))
    async with aiohttp.ClientSession(trust_env=True) as session:
        status.subheader(f"Connecting to {WS_CONN}")
        async with session.ws_connect(WS_CONN) as websocket:
            status.subheader(f"Connected to: {WS_CONN}")
            print("3 Connected to: ", WS_CONN)
            print(websocket)
            async for message in websocket:
                print("3 Message: ", message)
                data = message.json()
                try:
                    if not data:
                        print("No data")
                    else:
                        print("3 Data: ", data)
                        selected_interfaces = st_df.multiselect("Select interfaces", data, default=data[0])
                        # drop down menu
                        selected_dropdown = st.selectbox("Select interfaces", data)
                        # get the index of the selected interface
                        index = data.index(selected_dropdown)
                        # get the selected interface
                        selected_interface = data[index]
                        # Update session state when a new item is selected
                        if selected_dropdown != st.session_state.selected_interface:
                            st.session_state.selected_interface = selected_dropdown

                        # add selected interfaces to the st.session_state
                        st.session_state.selected_interfaces = selected_interfaces
                        st.write("Selected interfaces: ", selected_interfaces)
                        st.write("Selected interfaces: ", st.session_state.selected_interfaces)
                        columns = [col.empty() for col in st.columns(len(selected_interfaces))]
                        # print(st.session_state.selected_interfaces)
                        button = st.button("Start")




                except Exception as e:
                    if e != "TypeError: string indices must be integers":
                        print(e)
                    else:
                        print("1 ")



async def consumer_push(status, st_df):
    WS_CONN = "ws://localhost:8000/anomaly_push"

    async with aiohttp.ClientSession(trust_env=True) as session:
        # status.subheader(f"Connecting to {WS_CONN}")
        async with session.ws_connect(WS_CONN) as websocket:
            # status.subheader(f"Connected to: {WS_CONN}")
            print("2 Connected to: ", websocket)
            async for message in websocket:
                data = message.json()
                try:
                    # id data is empty
                    if not data:
                        print("No data")
                    else:
                        data_json = json.loads(data)
                        df = pd.DataFrame(data_json)
                        st_df.dataframe(df)                   # <====== This is where data comes

                        # if data is not empty list
                        if data != []:
                            logger.info("Data: ", data)
                        pass

                except Exception as e:
                    if e != "TypeError: string indices must be integers":
                        print(e)
                    else:
                        print("1 ")