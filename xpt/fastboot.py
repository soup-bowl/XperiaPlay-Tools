import subprocess
import re

class Fastboot(object):
	def __init__(self):
		self.fastboot = "/home/casey/Projects/XperiaPlay-Tools/platform-tools/linux/fastboot"
		vno = self.get_version()
		if vno != None:
			self.available = True
		else:
			self.available = False
	
	def is_available(self):
		return self.available

	def get_version(self):
		try:
			response = subprocess.run( [self.fastboot, "--version"], capture_output=True, text=True )
		except:
			return None

		return re.findall( "version\s*(.*)", str.splitlines( response.stdout)[0] )[0]
