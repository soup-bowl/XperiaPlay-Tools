import subprocess
import re
import datetime
from sys import platform

class ADB(object):
	def __init__(self):
		self.set_platform_tool()
		self.rootdir      = "./resources/root/"
		self.appdir       = "./resources/apps/"
		self.logfile      = "./system.log"
		self.device_id    = None
		self.device_model = None
		vno = self.get_version()
		if vno != None:
			self.available = True
			self.start_server()
		else:
			self.available = False

	def set_platform_tool(self):
		if platform == "linux" or platform == "linux2":
			self.adb = "./resources/platform-tools/linux/adb"
		elif platform == "darwin":
			self.adb = "./resources/platform-tools/darwin/adb"
		elif platform == "win32":
			self.adb = "./resources/platform-tools/windows/adb"
		else:
			self.adb = "adb"
	
	def is_available(self):
		return self.available

	def get_version(self):
		try:
			response = subprocess.run( [self.adb, "version"], capture_output=True, text=True )
		except:
			return None

		return re.findall( "version\s*([\d.]+)", response.stdout )[0]

	def get_devices_connected(self):
		devices  = []
		response = str.splitlines( subprocess.run( [self.adb, "devices"], capture_output=True, text=True ).stdout )
		if len( response ) == 2:
			return None

		for val in response:
			if "device" in val:
				devices.append( str.split(val, '\t')[0] )

		devices.remove('List of devices attached')
		
		return devices

	def set_device(self, device):
		"""Set the device to be worked on (get them using get_devices_connected()).

		Args:
			device (String): Device identifier from Fastboot devices.
		"""
		self.device_id = device

		model = subprocess.run( [self.adb, "shell", "getprop", "ro.product.model"], capture_output=True, text=True )
		self.device_model = str.split(model.stdout, "\n")[0]

	def start_server(self):
		if self.available == True:
			subprocess.run( [self.adb, "start-server"], capture_output=True )
	
	def init_zergrush_root(self):
		if self.device_id == None:
			return False
		
		comms = [
			[self.adb, "shell", "mkdir /data/local/rootmp"],
			[self.adb, "push", self.rootdir + "zergRush", "/data/local/rootmp/."],
			[self.adb, "shell", "chmod 777 /data/local/rootmp/zergRush"],
			[self.adb, "shell", "./data/local/rootmp/zergRush"],
			[self.adb, "wait-for-device"],
			[self.adb, "push", self.rootdir + "busybox", "/data/local/rootmp/."],
			[self.adb, "shell", "chmod 755 /data/local/rootmp/busybox"],
			[self.adb, "shell", "/data/local/rootmp/busybox mount -o remount,rw /system"],
			[self.adb, "shell", "dd if=/data/local/rootmp/busybox of=/system/xbin/busybox"],
			[self.adb, "shell", "chmod 04755 /system/xbin/busybox"],
			[self.adb, "shell", "/system/xbin/busybox --install -s /system/xbin"],
			[self.adb, "push", self.rootdir + "su", "/system/bin/su"],
			[self.adb, "shell", "chown 0:0 /system/bin/su"],
			[self.adb, "shell", "chmod 06755 /system/bin/su"],
			[self.adb, "shell", "rm /system/xbin/su"],
			[self.adb, "shell", "ln -s /system/bin/su /system/xbin/su"],
			[self.adb, "push", self.rootdir + "Superuser.apk", "/system/app/."],
			[self.adb, "shell", "rm -r /data/local/rootmp"]
		]

		for command in comms:
			response = subprocess.run( command, capture_output=True, text=True )
			if not response.stdout: self._log(response.stdout)
			if not response.stderr: self._log(response.stderr)

	def reboot_device(self, into_fastboot = False):
		if self.device_id == None:
			return False
		
		extra = ""
		if into_fastboot:
			extra = "bootloader"

		subprocess.run( [self.adb, "reboot", extra] )

	def _log(self, message):
		if not self.logfile:
			f = open(self.logfile, "a")
			f.write( "[" + str(datetime.utcnow()) + "]: " + str(message) )
			f.close()
