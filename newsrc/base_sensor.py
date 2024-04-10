from abc import ABC, abstractmethod

class Abc_sensor(ABC):
	@abstractmethod
	def read_data(self):
		pass
