import subprocess
import re

class ADB(object):
	def __init__(self):
		self.adb = "/home/casey/Projects/XperiaPlay-Tools/platform-tools/linux/adb"
		vno = self.get_version()
		if vno != None:
			self.available = True
		else:
			self.available = False
	
	def is_available(self):
		return self.available

	def get_version(self):
		try:
			response = subprocess.run( [self.adb, "version"], capture_output=True, text=True )
		except:
			return None

		return re.findall( "version\s*([\d.]+)", response.stdout )[0]
