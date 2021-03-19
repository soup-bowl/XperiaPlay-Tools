from xpt.com import Com
from datetime import datetime
from sys import platform
import re
import glob

class ADB(Com):
	def __init__(self):
		super().__init__()
		self.adb = self.platform + "/adb"

		self.device_id      = None
		self.device_model   = None
		self.device_build   = None
		self.device_version = None
		self.system_is_rw   = False
		vno = self.get_version()
		if vno != None:
			self.available = True
			self.start_server()
			self._log("Initating ADB, using " + self.get_version() + " found at " + self.adb + " on " + platform)
		else:
			self.available = False

	def get_version(self):
		"""Gets the active platform tools version.

		Returns:
			String: Android Debugging Bridge version string.
			None: No ADB package found.
		"""
		try:
			response = self.run( [self.adb, "version"] )
		except:
			self._log("Get version failed.")
			return None

		return re.findall( "version\s*([\d.]+)", response.stdout )[0]

	def get_devices_connected(self):
		"""Gets a list of the connected device serials.

		Returns:
			Array: The connected device serials.
			None: No devices were found/responded. 
		"""
		devices  = []
		response = str.splitlines( self.run( [self.adb, "devices"] ).stdout )
		if len( response ) == 2:
			self._log("No adb devices found.")
			return None

		for val in response:
			if "device" in val:
				devices.append( str.split(val, '\t')[0] )

		devices.remove('List of devices attached')

		self._log(str(len(devices)) + " adb devices found.")
		return devices

	def get_app_count(self):
		"""Counts the apps in the app directory.

		Returns:
			Int: Count of all files ending with .apk.
		"""
		return len(glob.glob1(self.appdir,"*.apk"))

	def set_device(self, device):
		"""Set the device to be worked on (get them using get_devices_connected()).

		Args:
			device (String): Device identifier from Fastboot devices.
		"""
		self.device_id = device

		model = self.run( [self.adb, "shell", "getprop", "ro.product.model"] )
		self.device_model = str.split(model.stdout, "\n")[0]
		build = self.run( [self.adb, "shell", "getprop", "ro.build.id"] )
		self.device_build = str.split(build.stdout, "\n")[0]
		version = self.run( [self.adb, "shell", "getprop", "ro.build.version.release"] )
		self.device_version = str.split(version.stdout, "\n")[0]

		self._log("ADB device set as " + self.device_model)

	def start_server(self):
		"""Start the adb response server.
		"""
		if self.available == True:
			self.run( [self.adb, "start-server"] )
			self._log("Starting up the Android Debugging Bridge server.")
	
	def init_zergrush_root(self):
		"""Root the currently connected Android device with the zergRush exploit.

		This will install busybox, su binary and Superuser.

		Returns:
			Boolean: Success status (false also returned if no device connected).
		"""
		if self.device_id == None:
			return False
		
		comms = [
			[self.adb, "shell", "mkdir", "/data/local/rootmp"],
			[self.adb, "push", self.rootdir + "zergRush", "/data/local/rootmp/."],
			[self.adb, "shell", "chmod", "777", "/data/local/rootmp/zergRush"],
			[self.adb, "shell", "./data/local/rootmp/zergRush"],
			[self.adb, "wait-for-device"],
			[self.adb, "push", self.rootdir + "busybox", "/data/local/rootmp/."],
			[self.adb, "shell", "chmod", "755", "/data/local/rootmp/busybox"],
			[self.adb, "shell", "/data/local/rootmp/busybox", "mount", "-o", "remount,rw", "/system"],
			[self.adb, "shell", "dd", "if=/data/local/rootmp/busybox", "of=/system/xbin/busybox"],
			[self.adb, "shell", "chmod", "04755", "/system/xbin/busybox"],
			[self.adb, "shell", "/system/xbin/busybox", "--install", "-s", "/system/xbin"],
			[self.adb, "push", self.rootdir + "su", "/system/bin/su"],
			[self.adb, "shell", "chown", "0:0", "/system/bin/su"],
			[self.adb, "shell", "chmod", "06755", "/system/bin/su"],
			[self.adb, "shell", "rm", "/system/xbin/su"],
			[self.adb, "shell", "ln", "-s", "/system/bin/su", "/system/xbin/su"],
			[self.adb, "push", self.rootdir + "Superuser.apk", "/system/app/."],
			[self.adb, "shell", "rm", "-r", "/data/local/rootmp"]
		]

		for command in comms:
			self.run( command )
		
		self.reboot_device()
		
		return True

	def install_all_apps(self):
		"""Installs all apks in the app directory.
		"""
		apks = glob.glob(self.appdir + '*.apk')
		for apk in apks:
			self._log("Installing app: " + apk)
			self.install_apk(apk)
	
	def install_apk(self, file):
		"""Installs the specified APK file.

		Args:
			file (String): Location of the desired apk.

		Returns:
			Boolean: True if successfully installed, False if an error occurred.
		"""
		response = self.run( [self.adb, "install", file] )

		if response.stderr != "":
			return True
		else:
			return False

	def mount_system(self):
		"""Mounts the system directory as rewritable for root operations.

		Returns:
			Boolean: Success status. The self.system_is_rw is modified to reflect.
		"""
		response = self.run( [self.adb, "shell", "su", "-c", "'mount -o remount,rw /system /system'"] )

		if response.stderr == "":
			self.system_is_rw = True
			return True
		else:
			return False
	
	def remove_system_app(self, file):
		"""Removes an app by directly removing it.

		Args:
			file (String): Full filepath to remove.

		Returns:
			Boolean: Always returns true.
		"""
		if self.system_is_rw == False:
			self.mount_system()

		self.run( [self.adb, "shell", "su", "-c", "'rm " + file + "'"] )

		return True

	def reboot_device(self, into_fastboot = False):
		"""Reboots the device.

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

		self.run( [self.adb, "reboot", extra] )
	
	def device_is_rooted(self):
		"""Checks if the device has been rooted.

		Returns:
			Boolean: Whether the device is rooted or not.
		"""
		response = self.run( [self.adb, "shell", "stat", "/system/bin/su"] )

		if "No such file or" in response.stdout:
			return False;
		elif "permission denied" in response.stdout:
			return False;
		else:
			return True;
