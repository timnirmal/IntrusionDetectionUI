import json

import aiohttp
import pandas as pd
from loguru import logger

logger.add("debug.log")


async def consumer_anom(anomaly_count, non_anomaly_count):
    WS_CONN = "ws://localhost:8000/anomalities"
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.ws_connect(WS_CONN) as websocket:
            async for message in websocket:
                data = message.json()
                try:
                    if not data:
                        print("No data")
                    else:
                        anomaly_cnt = data["anomalies"]
                        non_anomaly_cnt = data["non_anomalies"]
                        anomaly_count.markdown(
                            f'<p style="color: red; font-size: 20px;">Anomaly count: {anomaly_cnt}</p>',
                            unsafe_allow_html=True)
                        non_anomaly_count.markdown(
                            f'<p style="color: green; font-size: 20px;">Non-Anomaly count: {non_anomaly_cnt}</p>',
                            unsafe_allow_html=True)
                        pass

                except Exception as e:
                    if e != "TypeError: string indices must be integers":
                        print(e, "bb")


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
                        pass

                except Exception as e:
                    if e != "TypeError: string indices must be integers":
                        print(e, "cc")


async def consumer_push(push_df):
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

                        push_df.dataframe(df)

                except Exception as e:
                    if e != "TypeError: string indices must be integers":
                        print(e)


async def consumer_view_anom(select_anomaly, st_df_anom):
    WS_CONN = "ws://localhost:8000/view-anomalies"
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.ws_connect(WS_CONN) as websocket:
            async for message in websocket:
                data = message.json()
                try:
                    if not data:
                        print("No data")
                    else:
                        # print(data)
                        data_json = json.loads(data)
                        df = pd.DataFrame(data_json)

                        df["interface"] = df["interface"].str.split("\\\\").str[1]
                        df["interface"] = df["interface"].str.split("_").str[0]

                        anomaly_types = df["rf"].unique()

                        selected_anom = select_anomaly.selectbox("Select Anomaly Type", anomaly_types)
                        filtered_df = df[df["rf"] == selected_anom]
                        st_df_anom.dataframe(filtered_df.drop(columns=["rf"]))
                        pass

                except Exception as e:
                    if e != "TypeError: string indices must be integers":
                        print(e, "bb")
