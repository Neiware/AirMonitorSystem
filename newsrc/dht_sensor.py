import time
import board
import adafruit_dht

class Dht_sensor():

	#properties
	alive = False

	data = {
		'Temperature':0,
		'Humidity':0,
		'error':True
	}


	def _set_temperature(self, value):
		if value > 0 and self.data['Temperature'] != value:
			self.data['Temperature'] = value
			self._error_validation()

	def _set_humidity(self, value):
		if value > 0 and self.data['Humidity'] != value:
			self.data['Humidity'] = value
			self._error_validation()

	def _error_validation(self):
		if self.data['Temperature'] <= 0 or self.data['Humidity'] <= 0:
			self.data['error'] = True
		else:
			self.data['error'] = False

	def read_data(self):
		try:
			self._read_data()
		except RuntimeError as error:
			#Error happen fairly often, DHT's are hard to read
			print(error.args[0])

		except Exception as e:
			#Any type error
			print("Error dht:")
			print(e)

	def _read_data(self):
		#instance adafruit DHT22 lib
		dhtDevice = adafruit_dht.DHT22(board.D17)
		attempts = 0
		while attempts < 5:
			self.data['Temperature'] = dhtDevice.temperature
			self.data['Humidity'] = dhtDevice.humidity
			if self.data['error'] is False:
				break
			attempts = attempts + 1


	def __init__(self):
		self.alive = True
