import asyncio

import streamlit as st

from utils import consumer
from utils_anom import consumer_anom, consumer_push, consumer_view_anom

st.set_page_config(page_title="Network Traffic Monitor", layout="wide")


async def run_ws_connection(select_flow, st_df):
    try:
        await consumer(select_flow, st_df)
    except Exception as e:
        print("1:", e)
        st.text(e)


async def run_ws_connection_anom(anomaly_count, non_anomaly_count):
    try:
        await consumer_anom(anomaly_count, non_anomaly_count)
    except Exception as e:
        print("2:", e)
        st.text(e)


async def run_ws_connection_push(push_df):
    try:
        await consumer_push(push_df)
    except Exception as e:
        print("3:", e)


async def run_ws_connection_view_anom(select_anomaly, st_df_anom):
    try:
        await consumer_view_anom(select_anomaly, st_df_anom)
    except Exception as e:
        print("3:", e)


# async def run_ws_connection_interfaces(status, st_df):
#     try:
#         await consumer_interfaces(status, st_df)
#     except Exception as e:
#         print("4:", e)


async def main():
    # center title "Real-time Network Traffic Monitor"
    st.title("Real-time Network Traffic Monitor")

    st.subheader("Push Anomalies : ")
    push_df = st.empty()

    st.subheader("Anomalies : ")
    anomaly_count = st.empty()
    non_anomaly_count = st.empty()

    st.subheader("View Data : ")
    select_flow = st.empty()
    st_df = st.empty()

    st.subheader("View Anomalies : ")
    select_anomaly = st.empty()
    st_df_anom = st.empty()

    # Create two asyncio tasks and gather them to run simultaneously
    ws_task_1 = asyncio.create_task(run_ws_connection_anom(anomaly_count, non_anomaly_count))
    ws_task_2 = asyncio.create_task(run_ws_connection(select_flow, st_df))
    ws_task_3 = asyncio.create_task(run_ws_connection_view_anom(select_anomaly, st_df_anom))
    ws_task_4 = asyncio.create_task(run_ws_connection_push(push_df))

    # Gather both tasks to run simultaneously
    await asyncio.gather(ws_task_1, ws_task_2, ws_task_3)
    # await asyncio.gather(ws_task_1, ws_task_2)

    print("The app is running -- stream")


if __name__ == "__main__":
    print("The app is running")
    asyncio.run(main())
