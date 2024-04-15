from co2_sensor import Co2_sensor
from pm_sensor import Pm_sensor
from  dht_sensor import Dht_sensor
from sensor_database import SensorDatabase
import time

# Define the file name to save data
file_name = "sensor_data.txt"

# Create a list of sensors
sensors = [Co2_sensor(), Pm_sensor(), Dht_sensor()]
db = SensorDatabase()

# Define the duration of the data collection process (in seconds)
duration_hours = 5
#duration_seconds = duration_hours * 3600
duration_seconds = duration_hours * 3600

read_interval_time = 60

#private methods
def _save_data(dbContext, sensor_type, data):

	if sensor_type == Co2_sensor:
		dbContext.insert_co2_data(data['Co2'])

	elif sensor_type == Pm_sensor:
		dbContext.insert_pm5003_data(data['PM1.0'], data['PM2.5'], data['PM10'])

	elif sensor_type == Dht_sensor:
		dbContext.insert_dht_data(data['Humidity'], data['Temperature'])
	else:
		print("Error saving object type Sensor")

	#dbContext.close_connection()

def _print_info(sensor, data):
	sensor_type = type(sensor)
	sensor_type_str = str(sensor_type)

	# Convert dictionary items to a string
	data_str = ', '.join([f"{key}: {value}" for key, value in data.items()])

	# Concatenate strings
	print(sensor_type_str + " saving " + data_str)

# Record the start time
start_time = time.time()

while (time.time() - start_time) < duration_seconds:
	try:
		for sensor in sensors:
			sensor.read_data()
			#store valid data only
			_print_info(sensor, sensor.data)
			if(sensor.data['error'] is False):
				_save_data( db, type(sensor), sensor.data)
	except Exception as e:
		print(e)
	except RuntimeError as error:
		print(error.args[0])
	finally:
		time.sleep(read_interval_time)
