import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

pwm_pin = 17

GPIO.setup(pwm_pin, GPIO.OUT)

pwm = GPIO.PWM(pwm_pin, 1000)

try:
	pwm.start(50)
	start_time_ms = time.perf_counter_ns()/1000000
	end_time_ms = 0
	pwm_value = True
	while True:
		pwm_value = GPIO.input(pwm_pin)
		if(pwm_value == False):
			end_time_ms = time.perf_counter_ns()/1000000
			time_elapsed_ms = end_time_ms - start_time_ms
			if(time_elapsed_ms > 2):
				print(pwm_value)
				print("This is the start of a data Frame, the time elapsed  is", time_elapsed_ms)
				start_time_ms = time.perf_counter_ns()/1000000

except KeyboardInterrupt:
	print("Exiting..")
finally:
	pwm.stop()
	GPIO.cleanup()
