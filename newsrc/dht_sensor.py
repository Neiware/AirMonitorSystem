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
			dhtDevice = adafruit_dht.DHT22(board.D17)
			self._read_data(dhtDevice)
		except RuntimeError as error:
			#Error happen fairly often, DHT's are hard to read
			print(error.args[0])
			self.data['error'] = True
			dhtDevice.exit()

		except Exception as e:
			print(e)
			self.data['error'] = True
			dhtDevice.exit()

	def _read_data(self, dhtDevice):
		#instance adafruit DHT22 lib
		attempts = 0
		while attempts < 5:
			self._set_humidity(dhtDevice.humidity)
			self._set_temperature(dhtDevice.temperature)
			if self.data['error'] is False:
				break
			attempts = attempts + 1
		dhtDevice.exit()

	def __init__(self):
		print("DHT Initializing...")
		self.alive = True
