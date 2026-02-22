import paho.mqtt.client as mqtt
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import json
import time

# 1. Setup global data list
data = []

# 2. Define the message handler (This only collects data)
def on_message(client, userdata, message):
    try:
        payload = message.payload.decode("utf-8")
        # Using json.loads is safer than eval()
        sensor_values = json.loads(payload) 
        data.append((datetime.now(), sensor_values))
        
        # Keep the list from getting too long
        if len(data) > 50:
            data.pop(0)
    except Exception as e:
        print(f"Error receiving data: {e}")

# 3. Setup the MQTT Client
# Note: Using CallbackAPIVersion.VERSION1 to stop the DeprecationWarning
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.connect("localhost", 1883)
client.subscribe("sensor/data")
client.on_message = on_message

# 4. Initialize Plotting
plt.ion()  # Turn on Interactive Mode
fig, ax = plt.subplots()
client.loop_start()

print("Visualization started. Press Ctrl+C in terminal to stop.")

# 5. The Main Loop (This keeps the window alive and draws the graph)
try:
    while True:
        if len(data) > 0:
            # Create DataFrame from our growing list
            df = pd.DataFrame(data, columns=["timestamp", "sensor_data"])
            
            # Extract temp and humidity into their own columns
            df["temperature"] = df["sensor_data"].apply(lambda x: x["temperature"])
            df["humidity"] = df["sensor_data"].apply(lambda x: x["humidity"])

            # Clear and redraw
            ax.clear()
            ax.plot(df["timestamp"], df["temperature"], label="Temperature (°C)", color='red', marker='o')
            ax.plot(df["timestamp"], df["humidity"], label="Humidity (%)", color='blue', marker='s')
            
            ax.set_title("Real-Time IIoT Sensor Data (MQTT)")
            ax.set_xlabel("Time")
            ax.set_ylabel("Value")
            ax.legend(loc="upper right")
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Draw the update
            plt.draw()
        
        # This keeps the GUI responsive and prevents the "one second" exit
        plt.pause(1) 

except KeyboardInterrupt:
    print("\nStopping visualization...")
finally:
    client.loop_stop()
    plt.close()