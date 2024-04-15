
import sqlite3

class SensorDatabase:
	def __init__(self, db_name='sensor_data.db'):
		self.db_name = db_name
		self.conn = sqlite3.connect(db_name)
		self.create_tables()
		print("Database initializing...")

	def create_tables(self):
		cursor = self.conn.cursor()

		# Create table for CO2 sensor
		cursor.execute('''CREATE TABLE IF NOT EXISTS co2_data (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				co2_data REAL,
				timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
				)''')

		# Create table for DHT sensor
		cursor.execute('''CREATE TABLE IF NOT EXISTS dht_data (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				humidity REAL,
				temperature REAL,
				timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
				)''')

		# Create table for PM5003 sensor
		cursor.execute('''CREATE TABLE IF NOT EXISTS pm5003_data (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				pm1_0 INTEGER,
				pm2_5 INTEGER,
				pm10 INTEGER,
				timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
				)''')

		self.conn.commit()

	def insert_co2_data(self, co2_data):
		cursor = self.conn.cursor()
		cursor.execute("""INSERT INTO co2_data (co2_data) VALUES (?);""", (co2_data,))
		self.conn.commit()
		print("co2_data saved")

	def insert_dht_data(self, humidity, temperature):
		cursor = self.conn.cursor()
		cursor.execute('''INSERT INTO dht_data (humidity, temperature) VALUES (?, ?)''', (humidity, temperature,))
		self.conn.commit()
		print("dht_data saved")

	def insert_pm5003_data(self, pm1_0, pm2_5, pm10):
		cursor = self.conn.cursor()
		cursor.execute('''INSERT INTO pm5003_data (pm1_0, pm2_5, pm10) VALUES (?, ?, ?)''', (pm1_0, pm2_5, pm10,))
		self.conn.commit()
		print("pm5003_data saved")

	def close_connection(self):
		self.conn.close()

