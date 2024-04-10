from co2_sensor import Co2_sensor

co2 = Co2_sensor()

co2.read_data()
print(co2.data)
