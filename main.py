# import json
# import pickle
# import time  # to simulate a real time data, time loop
#
# import numpy as np  # np mean, np random
# import pandas as pd  # read csv, df manipulation
# import plotly.express as px  # interactive charts
# import requests
# import streamlit as st  # 🎈 data web app development
#
# st.set_page_config(
#     page_title="Real-Time Data Science Dashboard",
#     page_icon="✅",
#     layout="wide",
# )
#
# # read csv from a github repo
# # dataset_url = "https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv"
# dataset_url = "http://127.0.0.1:8000/csv_file?amount=10"
#
#
# # read csv from a URL
# @st.cache_data
# def get_data() -> pd.DataFrame:
#     # return pd.read_csv(dataset_url)
#     # get data from URL
#     # read dataset_url and get json
#     response = requests.get(dataset_url)
#     if response.status_code != 200:
#         raise Exception("Unable to fetch data from API")
#
#     # convert json to dataframe
#     data_json = response.json()
#
#     data_json = json.loads(data_json)
#
#     # check if json is in the right format
#     if not isinstance(data_json, list):
#         raise Exception("Data retrieved is not in JSON format")
#
#     # convert json to dataframe
#     try:
#         data_json = pd.DataFrame(data_json)
#     except Exception as e:
#         raise Exception("Unable to convert JSON to dataframe") from e
#
#     return data_json
#
#
# df = get_data()
#
# # dashboard title
# st.title("Real-Time / Live Data Science Dashboard")
#
# # # top-level filters
# # job_filter = st.selectbox("Select the Job", pd.unique(df["job"]))
#
# # creating a single-element container
# placeholder = st.empty()
#
# # # dataframe filter
# # df = df[df["job"] == job_filter]
#
# # near real-time / live feed simulation
# # for seconds in range(2):
# #
# # df["age_new"] = df["age"] * np.random.choice(range(1, 5))
# # df["balance_new"] = df["balance"] * np.random.choice(range(1, 5))
# #
# # # creating KPIs
# # avg_age = np.mean(df["age_new"])
# #
# # count_married = int(
# #     df[(df["marital"] == "married")]["marital"].count()
# #     + np.random.choice(range(1, 30))
# # )
# #
# # balance = np.mean(df["balance_new"])
#
# with placeholder.container():
#     # # create three columns
#     # kpi1, kpi2, kpi3 = st.columns(3)
#     #
#     # # fill in those three columns with respective metrics or KPIs
#     # kpi1.metric(
#     #     label="Age ⏳",
#     #     value=round(avg_age),
#     #     delta=round(avg_age) - 10,
#     # )
#     #
#     # kpi2.metric(
#     #     label="Married Count 💍",
#     #     value=int(count_married),
#     #     delta=-10 + count_married,
#     # )
#     #
#     # kpi3.metric(
#     #     label="A/C Balance ＄",
#     #     value=f"$ {round(balance,2)} ",
#     #     delta=-round(balance / count_married) * 100,
#     # )
#     #
#     # # create two columns for charts
#     # fig_col1, fig_col2 = st.columns(2)
#     # with fig_col1:
#     #     st.markdown("### First Chart")
#     #     fig = px.density_heatmap(
#     #         data_frame=df, y="age_new", x="marital"
#     #     )
#     #     st.write(fig)
#     #
#     # with fig_col2:
#     #     st.markdown("### Second Chart")
#     #     fig2 = px.histogram(data_frame=df, x="age_new")
#     #     st.write(fig2)
#
#     st.markdown("### Detailed Data View")
#     st.dataframe(df)
#     time.sleep(1)
#
#
# print("The app is running")

import asyncio

import pandas as pd
import streamlit as st
from utils import consumer


st.set_page_config(page_title="stream", layout="wide")

status = st.empty()
connect = st.checkbox("Connect to WS Server")

selected_channels = st.multiselect("Select Channels", ["A", "B", "C"], default=["A"])

columns = [col.empty() for col in st.columns(len(selected_channels))]

window_size = st.number_input("Window Size", min_value=10, max_value=100)

# create a st.dataframe placeholder and send it to consumer
st_df = st.empty()

if connect:
    asyncio.run(consumer(dict(zip(selected_channels, columns)), selected_channels, window_size, status,st_df))
else:
    status.subheader(f"Disconnected.")

print("The app is running -- stream")