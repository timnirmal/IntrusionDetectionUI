import json

import aiohttp

import pandas as pd
import streamlit as st


async def consumer(status, st_df):
    WS_CONN = "ws://localhost:8000/retrive_data"
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.ws_connect(WS_CONN) as websocket:
            # status.text(f"Incoming data:")
            async for message in websocket:
                data = message.json()
                try:
                    if not data:
                        print("No data")
                    else:
                        pass
                    data_json = json.loads(data)

                    # check if json is in the right format
                    if not isinstance(data_json, list):
                        raise Exception("Data retrieved is not in JSON format")

                    df = pd.DataFrame(data_json)

                    # save as flow_temp.csv
                    df.to_csv("flow_temp.csv", index=False)
                    df["interface"] = df["interface"].str.split("\\\\").str[1]
                    df["interface"] = df["interface"].str.split("_").str[0]

                    interfaces = df["interface"].unique()

                    selected_interface = st.selectbox("Select Interface", interfaces)
                    filtered_df = df[df["interface"] == selected_interface]

                    st.dataframe(filtered_df.drop(columns=["interface"]))
                except Exception as e:
                    if e != "TypeError: string indices must be integers":
                        print(e)