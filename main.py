import asyncio

import streamlit as st

from utils import consumer
from utils_anom import consumer_anom, consumer_push

st.set_page_config(page_title="Network Traffic Monitor", layout="wide")


async def run_ws_connection(status, st_df):
    try:
        await consumer(status, st_df)
    except Exception as e:
        print("1:", e)
        st.text(e)


async def run_ws_connection_anom(st_df, st_df_1_1):
    try:
        await consumer_anom(st_df, st_df_1_1)
    except Exception as e:
        print("2:", e)
        st.text(e)


async def run_ws_connection_push(status, st_df):
    try:
        await consumer_push(status, st_df)
    except Exception as e:
        print("3:", e)


# async def run_ws_connection_interfaces(status, st_df):
#     try:
#         await consumer_interfaces(status, st_df)
#     except Exception as e:
#         print("4:", e)


async def main():
    st.title("Real-time Network Traffic Monitor")

    st.subheader("Anomalies : ")
    status_2 = st.empty()
    st_df_2 = st.empty()
    st_df_2_1 = st.empty()

    st.subheader("Interfaces : ")
    status_1 = st.empty()
    st_df_1 = st.empty()

    status_3 = st.empty()
    st_df_3 = st.empty()

    # Create two asyncio tasks and gather them to run simultaneously
    # ws_task_1 = asyncio.create_task(run_ws_connection(selected_channels_1, columns_1, window_size_1, status_1, st_df_1))
    ws_task_2 = asyncio.create_task(run_ws_connection_anom(st_df_2, st_df_2_1))
    ws_task_1 = asyncio.create_task(run_ws_connection(status_1, st_df_1))
    # ws_task_3 = asyncio.create_task(run_ws_connection_push(status_3, st_df_3))

    # Gather both tasks to run simultaneously
    # await asyncio.gather(ws_task_1, ws_task_2, ws_task_3)
    await asyncio.gather(ws_task_1, ws_task_2)

    print("The app is running -- stream")


if __name__ == "__main__":
    print("The app is running")
    asyncio.run(main())
