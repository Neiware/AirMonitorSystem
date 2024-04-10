import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.IN)


try:
	while True:
		result = GPIO.input(11)
		print(result, end="")
except KeyBoardInterrupt:
	print("Finish")
finally:
	GPIO.cleanup()

