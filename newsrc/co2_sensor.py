from base_sensor import Abc_sensor
import RPi.GPIO as GPIO
import time

class Co2_sensor(Abc_sensor):
	#properties
	data = {
		'Co2': 0,
		'error':True
		}
	alive = False
	pwm_pin = None
	#set by datasheet
	MIN_CYCLE_TIME = 1000
	MAX_CYCLE_TIME = 1200

	#get and setter
	def _alive(self):
		return self.alive

	def _set_alive(self, value):
		if value != self.alive:
			self.alive = value
			if value is False:
				self._set_data_co2(0)

	def _data_co2(self):
		return self.data['Co2']

	#co2 cannot be 0
	def _set_data_co2(self, value):
		if  value > 0 and value != self._data_co2():
			self.data['Co2'] = round(value,2)

			self.data['error'] = False
		else:
			self.data['Co2'] = 0
			self.data['error'] = True


	def timeMs(self):
		return time.perf_counter_ns()/1000000

	def _calculate_co2_ppm(self,time_high, time_low):
		return 2000*((time_high - 2)/(time_high + time_low - 4))

	#define which time state to obtain
	# state = False (Low state)
	# state = True (High state)
	def _get_timeMs_state(self, state):
		start_time = self.timeMs()
		pwm_value = state
		threshold_Ms = 1000
		time_state_ms = 0

		while(pwm_value == state and time_state_ms < threshold_Ms):
			pwm_value = GPIO.input(self.pwm_pin)
			#to prevent infinte loop, pwm reading cannot exced 1000 ms
			time_state_ms = self.timeMs() - start_time
		return time_state_ms

	def read_data(self):
		if self.alive is False:
			return

		cycle_time = 0
		attepmts_reading = 0
		while attepmts_reading < 5:

			high_time = self._get_timeMs_state(True)
			low_time =  self._get_timeMs_state(False)

			cycle_time = high_time + low_time
			attepmts_reading = attepmts_reading + 1
			#print(cycle_time)

			if cycle_time > self.MAX_CYCLE_TIME or cycle_time < self.MIN_CYCLE_TIME:
				self.data['error'] = True
				continue
			else:
				co2_data = self._calculate_co2_ppm(high_time, low_time)
				self._set_data_co2(co2_data)
				break

	def __init__ (self):
		try:
			self.pwm_pin = 12
			GPIO.setmode(GPIO.BCM)
			GPIO.setup(self.pwm_pin, GPIO.IN)
			print("Co2 sensor Initializing...")
			self._set_alive(True)

		except:
			print("Co2 sensor: Error Initializing")
			#log for GPIO error
			print("Fatal Error")
			self._set_alive(False)

