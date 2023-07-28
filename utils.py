import json

import aiohttp
from collections import deque, defaultdict
from functools import partial
from os import getenv

import pandas as pd
import streamlit
import streamlit as st

WS_CONN = "ws://localhost:8000/sample"
async def consumer(graphs, selected_channels, window_size, status, st_df):
    windows = defaultdict(partial(deque, [0]*window_size, maxlen=window_size))

    async with aiohttp.ClientSession(trust_env = True) as session:
        print("1")
        status.subheader(f"Connecting to {WS_CONN}")
        print("1 Connecting to: ", WS_CONN)
        async with session.ws_connect(WS_CONN) as websocket:
            print("1 Connected to done: ", WS_CONN)
            status.subheader(f"Connected to: {WS_CONN}")
            print(websocket)
            async for message in websocket:
                print("1 Message: ", message)
                data = message.json()
                print("1 Data: ", data)

                try:
                    # id data is empty
                    if not data:
                        print("No data")
                    else:
                        # print("Data: ", data)
                        # show in a st.dataframe
                        pass
                    # show st.dataframe with random data
                    random_df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})
                    # st_df.dataframe(random_df)
                    data_json = json.loads(data)

                    # check if json is in the right format
                    if not isinstance(data_json, list):
                        raise Exception("Data retrieved is not in JSON format")

                    # print(type(data))
                    df = pd.DataFrame(data_json)
                    print(df)

                    st_df.dataframe(df)
                    status.subheader(f"Received: {len(df)} rows")
                except Exception as e:
                    if e != "TypeError: string indices must be integers":
                        print(e)
                    else:
                        print("1 ")

                # windows[data["channel"]].append(data["data"])
                #
                # for channel, graph in graphs.items():
                #     channel_data = {channel: windows[channel]}
                #     if channel == "A":
                #         graph.line_chart(channel_data)
                #     elif channel == "B":
                #         graph.area_chart(channel_data)
                #     elif channel == "C":
                #         graph.bar_chart(channel_data)