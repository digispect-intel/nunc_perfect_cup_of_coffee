import pandas as pd
import matplotlib.pyplot as plt
import ast

import numpy as np


grind_data = pd.read_csv("nlc-grind-data.csv")  # OCR data from coffee labels
brew_data = pd.read_csv("nlc-brew-data.csv")  # OCR data from coffee labels

print(grind_data.info())
print(brew_data.info())

grind_brew_data = pd.merge(grind_data, brew_data, on="eventId", how="inner")
print(grind_brew_data.info())

grind_brew_data = grind_brew_data.rename(columns={"deviceId_x": "deviceId"})
grind_brew_data = grind_brew_data.rename(columns={"recipeId_x": "recipeId"})
grind_brew_data = grind_brew_data.rename(columns={"eventTime_x": "eventTime_grind"})
grind_brew_data = grind_brew_data.rename(columns={"eventTime_y": "eventTime_brew"})

grind_brew_data = grind_brew_data.drop("deviceId_y", axis=1)
grind_brew_data = grind_brew_data.drop("recipeId_y", axis=1)
grind_brew_data = grind_brew_data.drop("eventType_x", axis=1)
grind_brew_data_deviceId = grind_brew_data.drop("eventType_y", axis=1)


grind_brew_data_deviceId["deviceId"] = grind_brew_data_deviceId["deviceId"].replace(
    {
        "18446744072574007284": "10000000812efd14",
        "18446744073136002376": "10000000812efd14",
        "18446744073527372579": "10000000dcdd8d82",
        "18446744072890410450": "10000000dcdd8d82",
        "18446744072773813932": "10000000dcdd8d82",
        "18446744072672130913": "10000000bce3a15f",
        "18446744072802279265": "10000000bce3a15f",
        "18446744072772856228": "100000001bcb62d3",
        "18446744072720600839": "1000000036a2c7bc",
        "18446744072835879765": "1000000036a2c7bc",
        "18446744072818439117": "1000000036a2c7bc",
    }
)

deviceId_counts = grind_brew_data_deviceId["deviceId"].value_counts()

print(grind_brew_data_deviceId.info())

print(deviceId_counts)


# grind_brew_data_deviceId = grind_brew_data_deviceId[:1000].reset_index(drop=True)
grind_brew_data_deviceId = grind_brew_data_deviceId.reset_index(drop=True)


# reformate eventTime_grind and eventTime_brew
grind_brew_data_deviceId["eventTime_grind"] = pd.to_datetime(
    grind_brew_data_deviceId["eventTime_grind"], format="%m/%d/%y %H:%M"
).dt.strftime("%y/%m/%d %H:%M")

grind_brew_data_deviceId["eventTime_brew"] = pd.to_datetime(
    grind_brew_data_deviceId["eventTime_brew"], format="%m/%d/%y %H:%M"
).dt.strftime("%y/%m/%d %H:%M")

df_sorted = grind_brew_data_deviceId.sort_values(by=["recipeId", "eventTime_grind"])

print(df_sorted)

# insight A
grindTime_grindSize_engineTemp = df_sorted[
    ["eventTime_grind", "grindSize", "engineTemperature"]
]
print(grindTime_grindSize_engineTemp)
#

cropped_grind_brew_data = df_sorted[
    [
        "deviceId",
        "eventId",
        "eventTime_grind",
        "grindSize",
        "recipeBeanWeight",
        "recipeId",
        "engineTemperature",
        "consumableId",
        "consumableRoastId",
        "sieveId",
        "totalDosedWeight",
        "continuation",
        "dosedWeights",
        "shutterTimes",
        "measurementTimes",
        "brewerHeadTemperature",
        "flowPump1",
        "flowPump2",
        "pressureCircuit1",
        "volumePump1",
        "peakPressure",
        "avgAmbientTemperature",
        "avgHumidity",
        "brewDuration",
        "initFthHeater1Temperature",
        "initFthHeater2Temperature",
        "initBrewerHeadTemperature",
    ]
]
cropped_grind_brew_data.to_csv("cropped_grind_brew_data.csv", index=False)


cropped_grind_brew_data_analysis = cropped_grind_brew_data[
    (cropped_grind_brew_data["recipeId"] == 31)
    & (cropped_grind_brew_data["deviceId"] == "10000000812efd14")
    & (cropped_grind_brew_data["consumableId"] != 2000000000000011)
    & (cropped_grind_brew_data["totalDosedWeight"] < 50)
]


cropped_grind_brew_data_analysis.to_csv(
    "cropped_grind_brew_data_analysis.csv", index=False
)


# data_31_device =

# ==============
brewerHeadTemperature = cropped_grind_brew_data_analysis["brewerHeadTemperature"].iloc[
    0
]
# Convert to list
brewer_head_temperature = ast.literal_eval(brewerHeadTemperature)


# cropped_grind_brew_data_analysis = cropped_grind_brew_data_analysis[:20]
cropped_grind_brew_data_analysis = cropped_grind_brew_data_analysis


# ==============brewerHeadTemperature
list_of_lists_brewer_head_temp_raw = [
    ast.literal_eval(brew_seqence)
    for brew_seqence in cropped_grind_brew_data_analysis["brewerHeadTemperature"]
]

# list_of_lists_brewer_head_temp = [
#     brew_seq
#     for brew_seq in list_of_lists_brewer_head_temp_raw
#     if 88.6 < brew_seq[0] < 91
# ]

indices_brewer_head_temp = [
    i
    for i, brew_seq in enumerate(list_of_lists_brewer_head_temp_raw)
    if 88.6 < brew_seq[0] < 91 and len(brew_seq) < 180 and brew_seq[-1] > 88
]

cropped_grind_brew_data_analysis = cropped_grind_brew_data_analysis.iloc[
    indices_brewer_head_temp
]

list_of_lists_brewer_head_temp = [
    ast.literal_eval(brew_seqence)
    for brew_seqence in cropped_grind_brew_data_analysis["brewerHeadTemperature"]
]


# Plot the brewerHeadTemperature as a line plot
plt.figure()

for seq in list_of_lists_brewer_head_temp:
    plt.plot(seq, alpha=0.5)  # alpha makes lines a bit transparent


# plt.plot(list_of_lists, label="Brewer Head Temperature")
plt.ylabel("Temperature (°C)")
plt.xlabel("time step")
plt.title("Brewer Head Temperature Over Time")
plt.legend()
plt.grid(True)
plt.savefig("brewer_head_temp_plot.png")


# ==============pressureCircuit1
list_of_lists_pressure_circuit = [
    ast.literal_eval(pressure_sequence)
    for pressure_sequence in cropped_grind_brew_data_analysis["pressureCircuit1"]
]

indices_pressure_circuit = [
    i
    for i, pressure_sequence in enumerate(list_of_lists_pressure_circuit)
    if all(float(x) < 8 for x in pressure_sequence)
]

cropped_grind_brew_data_analysis = cropped_grind_brew_data_analysis.iloc[
    indices_pressure_circuit
]

list_of_lists_pressure_circuit = [
    ast.literal_eval(pressure_sequence)
    for pressure_sequence in cropped_grind_brew_data_analysis["pressureCircuit1"]
]

# Plot the brewerHeadTemperature as a line plot
plt.figure()

for seq in list_of_lists_pressure_circuit:
    plt.plot(seq, alpha=0.5)  # alpha makes lines a bit transparent


# plt.plot(list_of_lists, label="Brewer Head Temperature")
plt.ylabel("pressureCircuit1 (bar)")
plt.xlabel("time step")
plt.title("pressureCircuit1")
plt.legend()
plt.grid(True)
plt.savefig("pressure_circuit_plot.png")


# ==============flowPump1
list_of_lists_flow_pump = [
    ast.literal_eval(brew_seqence)
    for brew_seqence in cropped_grind_brew_data_analysis["flowPump1"]
]

# Plot the brewerHeadTemperature as a line plot
plt.figure()

for seq in list_of_lists_flow_pump:
    plt.plot(seq, alpha=0.5)  # alpha makes lines a bit transparent


# plt.plot(list_of_lists, label="Brewer Head Temperature")
plt.ylabel("flowPump1 (°C)")
plt.xlabel("time step")
plt.title("flowPump1")
plt.legend()
plt.grid(True)
plt.savefig("flow_pump_plot.png")


# ==============volumePump1
list_of_lists_volume_pump = [
    ast.literal_eval(volume_seqence)
    for volume_seqence in cropped_grind_brew_data_analysis["volumePump1"]
]

# Plot the brewerHeadTemperature as a line plot
plt.figure()

for seq in list_of_lists_volume_pump:
    plt.plot(seq, alpha=0.5)  # alpha makes lines a bit transparent


# plt.plot(list_of_lists, label="Brewer Head Temperature")
plt.ylabel("volumePump1 (ml)")
plt.xlabel("time step")
plt.title("volumePump1")
plt.legend()
plt.grid(True)
plt.savefig("volume_pump_plot.png")


# ===============


cropped_grind_brew_data_analysis = cropped_grind_brew_data_analysis[
    [
        "grindSize",
        "recipeBeanWeight",
        "engineTemperature",
        "totalDosedWeight",
        "initFthHeater1Temperature",
        "initFthHeater2Temperature",
        "initBrewerHeadTemperature",
        "peakPressure",
        "avgAmbientTemperature",
        "avgHumidity",
        "brewDuration",
    ]
]


# Calculate correlation matrix
correlation_matrix = cropped_grind_brew_data_analysis.corr()

correlation_matrix.to_csv("correlation_matrix.csv")
pass
