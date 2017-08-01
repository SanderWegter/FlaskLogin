import yaml

class Config:
	def __init__(self):
		self.file = "config.yaml"
		self.config = {}

	def getConfig(self):
		f = open(self.file)
		self.config = yaml.safe_load(f)
		f.close()
		return self.config