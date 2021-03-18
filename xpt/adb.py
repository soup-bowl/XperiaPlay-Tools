import subprocess
import re
from datetime import datetime
from sys import platform

class ADB(object):
	def __init__(self):
		self.adb = "./resources/platform-tools/adb"

		self.rootdir      = "./resources/root/"
		self.appdir       = "./resources/apps/"
		self.logfile      = "./system.log"
		self.device_id    = None
		self.device_model = None
		vno = self.get_version()
		if vno != None:
			self.available = True
			self.start_server()
			self._log("Initating ADB, using " + self.get_version() + " found at " + self.adb + " on " + platform)
		else:
			self.available = False
	
	def is_available(self):
		"""
		Is the Android debugging package available.
		"""
		return self.available

	def get_version(self):
		"""
		Gets the active platform tools version.

		Returns:
			String: Android Debugging Bridge version string.
			None: No ADB package found.
		"""
		try:
			response = subprocess.run( [self.adb, "version"], capture_output=True, text=True )
		except:
			return None

		return re.findall( "version\s*([\d.]+)", response.stdout )[0]

	def get_devices_connected(self):
		"""
		Gets a list of the connected device serials.

		Returns:
			Array: The connected device serials.
			None: No devices were found/responded. 
		"""
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
		"""
		Set the device to be worked on (get them using get_devices_connected()).

		Args:
			device (String): Device identifier from Fastboot devices.
		"""
		self.device_id = device

		model = subprocess.run( [self.adb, "shell", "getprop", "ro.product.model"], capture_output=True, text=True )
		self.device_model = str.split(model.stdout, "\n")[0]

		self._log("ADB device set as " + self.device_model)

	def start_server(self):
		"""
		Start the adb response server.
		"""
		if self.available == True:
			subprocess.run( [self.adb, "start-server"], capture_output=True )
	
	def init_zergrush_root(self):
		"""
		Root the currently connected Android device with the zergRush exploit.

		This will install busybox, su binary and Superuser.

		Returns:
			Boolean: Success status (false also returned if no device connected).
		"""
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
			if response.stdout != "": self._log(response.stdout)
			if response.stderr != "": self._log(response.stderr)
		
		self.reboot_device()
		
		return True

	def reboot_device(self, into_fastboot = False):
		"""
		Reboots the device.

		Args:
			into_fastboot (bool, optional): Boot into fastboot. Defaults to False.

		Returns:
			None: No return.
		"""
		if self.device_id == None:
			return None
		
		extra = ""
		if into_fastboot:
			extra = "bootloader"

		subprocess.run( [self.adb, "reboot", extra] )
	
	def device_is_rooted(self):
		response = subprocess.run( [self.adb, "shell", "stat", "/system/bin/su"], capture_output=True, text=True )
		#if "Size: 22" in response.stdout:
		#	return True;
		if "No such file or" in response.stdout:
			return False;
		elif "permission denied" in response.stdout:
			return False;
		else:
			return True;

	def _log(self, message):
		"""
		Logs the message to the internally specified file.

		Args:
			message (String): Message.
		"""
		if self.logfile != False and message != "":
			f = open(self.logfile, "a")
			f.write( "\n[" + str(datetime.utcnow()) + "]: " + str(message) )
			f.close()
