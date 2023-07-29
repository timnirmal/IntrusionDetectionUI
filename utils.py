import json

import aiohttp
from collections import deque, defaultdict
from functools import partial
from os import getenv

import pandas as pd
import streamlit
import streamlit as st


async def consumer(status, st_df):
    # WS_CONN = "ws://localhost:8000/retrive_data?interface=WiFi"
    WS_CONN = "ws://localhost:8000/retrive_data"
    async with aiohttp.ClientSession(trust_env=True) as session:
        status.subheader(f"Connecting to {WS_CONN}")
        async with session.ws_connect(WS_CONN) as websocket:
            print("1 Connected to done: ", WS_CONN)
            status.subheader(f"Connected to: {WS_CONN}")
            print(websocket)
            # data = {"channel": "A", "data": [1, 2, 3]}
            # await websocket.send_json(data)

            async for message in websocket:
                # print("1 Message: ", message)
                data = message.json()
                try:
                    # id data is empty
                    if not data:
                        print("No data")
                    else:
                        # print("Data: ", data)
                        # show in a st.dataframe
                        pass
                    # show st.dataframe with random data
                    # random_df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})
                    # st_df.dataframe(random_df)
                    data_json = json.loads(data)

                    # check if json is in the right format
                    if not isinstance(data_json, list):
                        raise Exception("Data retrieved is not in JSON format")

                    # print(type(data))
                    df = pd.DataFrame(data_json)
                    # print(df)
                    # get unique interfaces from the dataframe
                    interfaces = df["interface"].unique()
                    # multiselect
                    # create a place holder to keep a set of
                    # selected_interfaces = st_df.multiselect("Select interfaces", interfaces, default=interfaces[0])
                    # drop down menu
                    selected_dropdown = st.selectbox("Select interfaces sss", interfaces)
                    print("Selected interface Selected dropdown: ", selected_dropdown)
                    # get the index of the selected interface
                    index = interfaces.index(selected_dropdown)
                    print("Selected interface Index: ", index)
                    # get the selected interface
                    selected_interface = interfaces[index]
                    print("Selected interface: ", selected_interface)
                    st.write(selected_interface)
                    # for interface in interfaces:
                    st_placeholder = st.empty()
                    # if interface not in interfaces:
                    #     continue
                    # filter dataframe by interface
                    df_inf = df[df["interface"] == selected_interface]
                    # remove interface column
                    df_inf = df_inf.drop(columns=["interface"])
                    # show dataframe
                    st_df.dataframe(df_inf)

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


async def consumer_one(status, st_df, interface):
    # windows = defaultdict(partial(deque, [0] * window_size, maxlen=window_size))
    WS_CONN = "ws://localhost:8000/retrive_data?interface=" + interface
    print("consumer_one WS_CONN: ", WS_CONN)
    async with aiohttp.ClientSession(trust_env=True) as session:
        status.subheader(f"consumer_one Connecting to {WS_CONN}")
        st.text("consumer_one Connecting to: " + WS_CONN)
        print("consumer_one Connecting to: ", WS_CONN)
        async with session.ws_connect(WS_CONN) as websocket:
            # send interface to server
            print("consumer_one Connected to done: ", WS_CONN)
            status.subheader(f"consumer_one Connected to: {WS_CONN}")
            print(websocket)
            # data = {"channel": "A", "data": [1, 2, 3]}
            # await websocket.send_json(data)
            print("before consumer_one Sent interface to server ", interface, websocket)
            # await websocket.send_json({"interface": interface})
            print("consumer_one Sent interface to server", interface, websocket)
            async for message in websocket:
                print("consumer_one Message: ", message)
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

                    # print(type(data))
                    df = pd.DataFrame(data_json)

                    st_df.dataframe(df)
                    status.subheader(f"Received: {len(df)} rows")
                except Exception as e:
                    if e != "TypeError: string indices must be integers":
                        print(e)
                    else:
                        print("1 ")
