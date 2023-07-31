import pandas as pd

df = pd.read_csv("flow_temp.csv")

# get interface column
interfaces = df["interface"].unique()
print("interfaces: ", interfaces)

# flow_data\\Ethernet_flow.csv
# from df keep only Ethernet part
# Extract the "Ethernet" part from the "interface" column
df["interface"] = df["interface"].str.split("\\\\").str[1]
# remove _flow.csv
df["interface"] = df["interface"].str.split("_").str[0]

# get unique interfaces
interfaces = df["interface"].unique()
print("interfaces: ", interfaces)
