import pandas as pd
import streamlit as st
import time

def read_csv_file(file_path):
    # Use pandas to read the CSV file
    data = pd.read_csv(file_path)
    return data

def main():
    st.title("Real-time CSV Reader")

    # Replace 'flow.csv' with the actual path to your CSV file
    file_path = 'flow.csv'

    while True:
        try:
            # Attempt to read the CSV file
            data = read_csv_file(file_path)
            st.write("Current data:")
            st.write(data)
        except Exception as e:
            st.write("Error reading CSV file:", e)

        time.sleep(5)  # Adjust the refresh rate as needed

if __name__ == "__main__":
    main()
