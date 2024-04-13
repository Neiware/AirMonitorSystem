from co2_sensor import Co2_sensor
from pm_sensor import Pm_sensor
import time

# Define the file name to save data
file_name = "sensor_data.txt"

# Create a list of sensors
sensors = [Co2_sensor(), Pm_sensor()]

# Define the duration of the data collection process (in seconds)
duration_hours = 1
#duration_seconds = duration_hours * 3600
duration_seconds = 500

# Record the start time
start_time = time.time()

# Open the file in write mode
with open(file_name, 'w') as file:
    # Continue collecting data until the specified duration is reached
    while (time.time() - start_time) < duration_seconds:
        # Iterate over each sensor
        for sensor in sensors:
            # Read data from the sensor
            sensor.read_data()
            
            # Write sensor type and data to the file
            file.write(f"Sensor Type: {sensor.__class__.__name__}\n")
            for key, value in sensor.data.items():
                file.write(f"{key}: {value}\n")
            
            # Write a separator for readability
            file.write("-" * 20 + "\n")
        
        # Wait for a minute before collecting data again
        time.sleep(60)

# Confirmation message
print(f"Sensor data has been saved to {file_name}")

