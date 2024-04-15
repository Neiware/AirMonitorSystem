import serial
import json
from base_sensor import Abc_sensor

class Pm_sensor(Abc_sensor):
	#properties
	alive = False

	data = {
		'PM1.0':0,
		'PM2.5':0,
		'PM10':0,
		'error':False
	}
	#Serial configuration
	PORT = "/dev/ttyS0"
	BAUDRATE = 9600
	TIMEOUT = 3

	#values from datasheet
	START_BYTES = b'\x42\x4d'
	data_frame = [0] * 31
	valid_frame = False

	#get and setter
	def _set_PM1_0(self, value):
		if value <= 0 or value != self.data['PM1.0']:
			self.data['PM1.0'] = value
			self._error_validation()

	def _set_PM2_5(self, value):
		if value <= 0 or value != self.data['PM2.5']:
			self.data['PM2.5'] = value
			self._error_validation()

	def _set_PM10(self, value):
		if value < 0 or value != self.data['PM10']:
			self.data['PM10'] = value
			self._error_validation()

	def _error_validation(self):
		if self.data['PM1.0'] <= 0 or self.data['PM2.5'] <= 0 or self.data['PM10'] < 0:
			self.data['error'] = True
		else:
			self.data['error'] = False

	def _set_error(self, value):
		if value != self.data['error']:
			self.data['error'] = value
	def read_data(self):
		if self.alive is False:
			return

		self._read_data()


	def _read_data(self):
		try:
			self._get_valid_data_frame()
			self._process_data_frame()
		except Exception as e:
			print("Erorr reading data")
			print(e)

	def _get_valid_data_frame(self):
		self._set_error(True)
		with serial.Serial(self.PORT, self.BAUDRATE, timeout= self.TIMEOUT) as sensor_serial:
			attempts = 0
			while attempts < 8:
				#attempt to get the corresponding start bytes
				start_bytes = sensor_serial.read(2)
				if start_bytes != self.START_BYTES:
					attempts = attempts + 1
					continue
				#get the rest of data frame
				self.data_frame = start_bytes + sensor_serial.read(30)

				#validate uncurropted data with checksum
				checksum = self.data_frame[31]
				current_checksum = self._calculate_new_checksum()
				if checksum == current_checksum:
					self._set_error(False)
					break

				attempts = attempts + 1


	def _calculate_new_checksum(self):
		current_checksum = 0
		for i in range(30):
			current_checksum += self.data_frame[i]
		return current_checksum % 256

	def _process_data_frame(self):
		processed_data = [0] * 13
		index_data = 4
		for i in range(13):
			processed_data[i] = self._sum_2Bytes_to_16bits(self.data_frame[index_data], self.data_frame[index_data + 1])
			index_data += 2
		self._set_PM1_0(processed_data[0])
		self._set_PM2_5(processed_data[1])
		self._set_PM10(processed_data[2])

	def _sum_2Bytes_to_16bits(self, msb, lsb): return (msb << 8) | lsb

	#init or contructor
	def __init__(self):
		try:
			test_serial = serial.Serial(self.PORT, self.BAUDRATE, timeout= self.TIMEOUT)
			if test_serial.is_open:
				print("PM5003 Initializing..")
			self.alive = True
			test_serial.close()

		except Exception as e:
			self.alive = False
			print(e)
