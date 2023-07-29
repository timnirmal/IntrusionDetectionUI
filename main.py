import asyncio
import pandas as pd
import streamlit as st
from utils import consumer
from utils_anom import consumer_anom, consumer_interfaces

st.set_page_config(page_title="stream", layout="wide")


async def run_ws_connection(status, st_df):
    try:
        await consumer(status, st_df)
    except Exception as e:
        print("1:", e)


async def run_ws_connection_anom(status, st_df):
    try:
        await consumer_anom(status, st_df)
    except Exception as e:
        print("2:", e)

async def run_ws_connection_interfaces(status, st_df):
    try:
        await consumer_interfaces(status, st_df)
    except Exception as e:
        print("3:", e)

async def main():
    status_1 = st.empty()
    status_2 = st.empty()
    status_3 = st.empty()

    # selected_channels_1 = st.multiselect("Select Channels (Server 1)", ["A", "B", "C"], default=["A"])
    # columns_1 = [col.empty() for col in st.columns(len(selected_channels_1))]
    # window_size_1 = st.number_input("Window Size (Server 1)", min_value=10, max_value=100)
    st_df_1 = st.empty()

    # selected_channels_2 = st.multiselect("Select Channels (Server 2)", ["X", "Y", "Z"], default=["X"])
    # columns_2 = [col.empty() for col in st.columns(len(selected_channels_2))]
    # window_size_2 = st.number_input("Window Size (Server 2)", min_value=10, max_value=100)
    st_df_2 = st.empty()

    # if "selected_interfaces" not in st.session_state:
    #     st.session_state.selected_interfaces = ["None"]
    # selected_channels_3 = st.multiselect("Select Channels (Server 3)", ["None"], default=["None"])
    # else:
    #     print("selected_interfaces: ", st.session_state.selected_interfaces)
    #     selected_channels_3 = st.multiselect("Selected Interfaces", st.session_state.selected_interfaces)
    # columns_3 = [col.empty() for col in st.columns(len(selected_channels_3))]
    # window_size_3 = st.number_input("Window Size (Server 3)", min_value=10, max_value=100)
    st_df_3 = st.empty()

    if "selected_interface" not in st.session_state:
        st.session_state.selected_interface = ""

    if "all_interface" not in st.session_state:
        st.session_state.all_interface = ""

    # Create two asyncio tasks and gather them to run simultaneously
    # ws_task_1 = asyncio.create_task(run_ws_connection(selected_channels_1, columns_1, window_size_1, status_1, st_df_1))
    ws_task_1 = asyncio.create_task(run_ws_connection(status_1, st_df_1))
    # ws_task_2 = asyncio.create_task(run_ws_connection_anom(status_2, st_df_2))
    # ws_task_3 = asyncio.create_task(run_ws_connection_interfaces(status_3, st_df_3))

    # Gather both tasks to run simultaneously
    # await asyncio.gather(ws_task_1, ws_task_2, ws_task_3)
    await asyncio.gather(ws_task_1)

    print("The app is running -- stream")


if __name__ == "__main__":
    asyncio.run(main())
