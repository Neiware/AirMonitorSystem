import RPi.GPIO as GPIO
import time


def timeMs():
	return time.perf_counter_ns()/1000000
def co2_ppm(time_high, time_low):
	return 2000*((time_high - 2)/(time_high + time_low - 4))
GPIO.setmode(GPIO.BCM)

pwm_pin = 12

GPIO.setup(pwm_pin, GPIO.IN)

try:
	#start_time_ms = elapsedTimeMs()
	#end_time_ms = 0
	pwm_value = True
	while(pwm_value == True):
		pwm_value = GPIO.input(pwm_pin)
	while(pwm_value == False):
		pwm_value = GPIO.input(pwm_pin)
	while True:
		#read the correct val
		start_time = timeMs()
		while(pwm_value == True):
			pwm_value = GPIO.input(pwm_pin)
		high_level_time = timeMs() - start_time
		print("Hight Time",high_level_time)

		start_time = timeMs()
		while(pwm_value == False):
			pwm_value = GPIO.input(pwm_pin)
		low_level_time = timeMs() - start_time
		print("Low Time", low_level_time)

		cycle_time = high_level_time + low_level_time
		print("Full cycle time", cycle_time)
		print(co2_ppm(high_level_time, low_level_time))
		#print(pwm_value, end="")
#		if(pwm_value == False):
#			end_time_ms = time.perf_counter_ns()/1000000
#			time_elapsed_ms = end_time_ms - start_time_ms
#			if(time_elapsed_ms > 2):
#				while(pwm_value == False):
#					pwm_value = GPIO.input(pwm_pin)
#				end_time_ms = time.perf_counter_ns()/1000000
#				time_elapsed_ms = end_time_ms - start_time_ms
#				print("This is the start of a data Frame, the time elapsed  is", time_elapsed_ms)
#				start_time_ms = time.perf_counter_ns()/1000000

except KeyboardInterrupt:
	print("Exiting..")
finally:
	GPIO.cleanup()
