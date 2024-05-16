import pymssql
import os

class AwsDatabase:
	def __init__(self):
		self.server = os.environ['DB_SERVER']
		self.user = os.environ['DB_USER']
		self.password= os.environ['DB_PASSWORD']
		self.database= 'AirQuality_db'
		self.conn = None
		print("AWS pymssql Client initializing...")

	def connect(self):
		self.conn = pymssql.connect(
			server= self.server,
	 		user=self.user,
		    	password=self.password,
	    		database=self.database,
	    		as_dict=True
		)

	def insert_co2_data(self, co2_data):
		cursor = self.conn.cursor()
		cursor.execute("INSERT INTO co2_data (co2_data) VALUES (%s);", (co2_data))
		self.conn.commit()
		print("AWS: co2_data saved")

	def insert_dht_data(self, humidity, temperature):
		cursor = self.conn.cursor()
		cursor.execute("INSERT INTO dht_data (humidity, temperature) VALUES (%s, %s)", (humidity, temperature,))
		self.conn.commit()
		print("AWS: dht_data saved")

	def insert_pm5003_data(self, pm1_0, pm2_5, pm10):
		cursor = self.conn.cursor()
		cursor.execute("INSERT INTO pm5003_data (pm1_0, pm2_5, pm10) VALUES (%s, %s, %s)", (pm1_0, pm2_5, pm10,))
		self.conn.commit()
		print("AWS: pm5003_data saved")

	def close_connection(self):
		self.conn.close()

	def get_co2(self):
		cursor = self.conn.cursor()
		response = cursor.execute('''SELECT * FROM co2_data''')
		print(type(response.fetchall()))
		self.conn.commit()
