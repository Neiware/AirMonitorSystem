import serial
import json

#msb = most significant bits
#lsb = least significat bits
def sum_2Bytes_to_16bits(msb , lsb):
        return (msb << 8) | lsb


def get_PMs_data():
	#define Data Dictonary
	dataJson = {
		'PM1.0':0,
		'PM2.5':0,
		'PM10':0,
		'error': False
	}
	try:
		ser = serial.Serial("/dev/ttyS0", baudrate=9600)
		while True:
			start_bytes = ser.read(2)
			if start_bytes == b'\x42\x4d':
				frame_data = start_bytes + ser.read(30)
				#print("Received Frame Data", frame_data.hex())
				frame_CheckSum = frame_data[31]
				checkSum = 0
				for i in range(30):
					checkSum += frame_data[i]
				checkSum = checkSum % 256
				#print("kLowBits checkSum:", checkSum)
				dataCheck = frame_data[31]
				#print("dataCheck =", dataCheck)
				#check if checkSum equals
				if checkSum != dataCheck:
					print("data is corrupted PMS5003")
					continue

				data = [0] * 13
				index_data = 4
				for i in range(13):
					data[i] = sum_2Bytes_to_16bits(frame_data[index_data],frame_data[index_data + 1])
					index_data += 2
				#Data is ready to work
				dataJson['PM1.0'] = data[0]
				dataJson['PM2.5'] = data[1]
				dataJson['PM10'] = data[2]
				return
	except:
		print("big error")
		dataJson['PM1.0'] = 0
		dataJson['PM2.5'] = 0
		dataJson['PM10'] = 0
		dataJson['error'] = True
	finally:
		ser.close()
		return dataJson


if __name__ == "__main__":
	pms_data = get_PMs_data()
	print(json.dumps(pms_data, indent= 4))
