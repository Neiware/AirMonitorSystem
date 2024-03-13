import serial

#msb = most significant bits
#lsb = least significat bits
def sum_2Bytes_to_16bits(msb , lsb):
        return (msb << 8) | lsb

#print all PMS5003 values from array
def printAll(arrData):
        print("PM1.0 standard ug/m3:", arrData[0])
        print("PM2.5 standard ug/m3:", arrData[1])
        print("PM10 standard ug/m3:", arrData[2])
        print("PM1.0 atmospheric ug/m3:", arrData[3])
        print("PM2.5 atmospheric ug/m3:", arrData[4])
        print("PM10 atmospheric ug/m3:", arrData[5])
        print("PM1.0  num part >1.0:", arrData[8])
        print("PM2.5  num part >2.5:", arrData[9])
        print("PM10  num part >5.0:", arrData[10])
        print("PM10  num part >10:", arrData[11])



ser = serial.Serial("/dev/ttyS0", baudrate=9600)

try:
        while True:
                start_bytes = ser.read(2)
                if start_bytes == b'\x42\x4d':
                        frame_data = start_bytes + ser.read(30)
                        print("Received Frame Data", frame_data.hex())
                        frame_CheckSum = frame_data[31]
                        checkSum = 0
                        for i in range(30):
                                checkSum += frame_data[i]
                        checkSum = checkSum % 256
                        print("LowBits checkSum:", checkSum)
                        print("dataCheck:", frame_data[31])
                        data = [0] * 13
                        index_data = 4
                        for i in range(13):
                                data[i] = sum_2Bytes_to_16bits(frame_data[index_data],frame_data[index_data + 1])
                                index_data += 2
                        printAll(data)
                else:
                        print("Discardeed", start_bytes.hex())
except KeyboardInterrupt:
        ser.close()
