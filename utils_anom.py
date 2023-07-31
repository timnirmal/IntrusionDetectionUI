import json

import aiohttp
import pandas as pd
import streamlit as st
from loguru import logger

logger.add("debug.log")


async def consumer_anom(st_df, st_df_1_1):
    WS_CONN = "ws://localhost:8000/anomalities"
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.ws_connect(WS_CONN) as websocket:
            async for message in websocket:
                data = message.json()
                try:
                    if not data:
                        print("No data")
                    else:
                        anomaly_count = data["anomalies"]
                        non_anomaly_count = data["non_anomalies"]
                        st_df.markdown(f'<p style="color: red; font-size: 20px;">Anomaly count: {anomaly_count}</p>',
                                       unsafe_allow_html=True)
                        st_df_1_1.markdown(
                            f'<p style="color: green; font-size: 20px;">Non-Anomaly count: {non_anomaly_count}</p>',
                            unsafe_allow_html=True)
                        pass

                except Exception as e:
                    if e != "TypeError: string indices must be integers":
                        print(e)


async def consumer_interfaces(status, st_df):
    WS_CONN = "ws://localhost:8000/interfaces"
    async with aiohttp.ClientSession(trust_env=True) as session:
        status.subheader(f"Connecting to {WS_CONN}")
        async with session.ws_connect(WS_CONN) as websocket:
            status.subheader(f"Connected to: {WS_CONN}")
            async for message in websocket:
                data = message.json()
                try:
                    if not data:
                        print("No data")
                    else:
                        st.write(data)

                except Exception as e:
                    if e != "TypeError: string indices must be integers":
                        print(e)


async def consumer_push(status, st_df):
    WS_CONN = "ws://localhost:8000/anomaly_push"
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.ws_connect(WS_CONN) as websocket:
            async for message in websocket:
                data = message.json()
                try:
                    if not data:
                        print("No data")
                    else:
                        data_json = json.loads(data)
                        df = pd.DataFrame(data_json)
                        st_df.dataframe(df)  # <====== This is where data comes

                        # if data is not empty list
                        if data != []:
                            logger.info("Data: ", data)
                        pass

                except Exception as e:
                    if e != "TypeError: string indices must be integers":
                        print(e)
