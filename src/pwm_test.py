import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the PWM pin
pwm_pin = 12  # You may need to change this based on your hardware configuration

# Set up the PWM
GPIO.setup(pwm_pin, GPIO.IN)

try:
	while True:
        	# Read the PWM duty cycle
		start = time.perf_counter_ns()/1000000
		pwm_value = GPIO.input(pwm_pin)
		end = time.perf_counter_ns() /1000000
       		# Print the PWM value
		print(end - start)

        # Wait for a short duration before reading again
		time.sleep(1)

except KeyboardInterrupt:
    # Clean up on keyboard interrupt
    print("Exiting...")

finally:
    # Cleanup GPIO
    GPIO.cleanup()

