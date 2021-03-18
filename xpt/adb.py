import subprocess
import re
import datetime

class ADB(object):
	def __init__(self):
		self.adb          = "./resources/platform-tools/linux/adb"
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
		
		a = subprocess.run( [self.adb, "shell", "mkdir /data/local/rootmp"], capture_output=True )
		b = subprocess.run( [self.adb, "push", self.rootdir + "zergRush", "/data/local/rootmp/."], capture_output=True )
		c = subprocess.run( [self.adb, "shell", "chmod 777 /data/local/rootmp/zergRush"], capture_output=True )
		d = subprocess.run( [self.adb, "shell", "./data/local/rootmp/zergRush"], capture_output=True )

		e = subprocess.run( [self.adb, "shell", "wait-for-device"], capture_output=True )

		f = subprocess.run( [self.adb, "push", self.rootdir + "busybox", "/data/local/rootmp/."], capture_output=True )
		g = subprocess.run( [self.adb, "shell", "chmod 755 /data/local/rootmp/busybox"], capture_output=True )
		i = subprocess.run( [self.adb, "shell", "/data/local/rootmp/busybox mount -o remount,rw /system"], capture_output=True )
		j = subprocess.run( [self.adb, "shell", "dd if=/data/local/rootmp/busybox of=/system/xbin/busybox"], capture_output=True )
		k = subprocess.run( [self.adb, "shell", "chmod 04755 /system/xbin/busybox"], capture_output=True )
		l = subprocess.run( [self.adb, "shell", "/system/xbin/busybox --install -s /system/xbin"], capture_output=True )
		
		m = subprocess.run( [self.adb, "push", self.rootdir + "su", "/system/bin/su"], capture_output=True )
		n = subprocess.run( [self.adb, "shell", "chown 0:0 /system/bin/su"], capture_output=True )
		o = subprocess.run( [self.adb, "shell", "chmod 06755 /system/bin/su"], capture_output=True )
		p = subprocess.run( [self.adb, "shell", "rm /system/xbin/su"], capture_output=True )
		q = subprocess.run( [self.adb, "shell", "ln -s /system/bin/su /system/xbin/su"], capture_output=True )

		r = subprocess.run( [self.adb, "push", self.rootdir + "Superuser.apk", "/system/app/."], capture_output=True )
		s = subprocess.run( [self.adb, "shell", "rm -r /data/local/rootmp"], capture_output=True )

		self.reboot_device()

	def reboot_device(self, into_fastboot = False):
		if self.device_id == None:
			return False
		
		extra = ""
		if into_fastboot:
			extra = "bootloader"

		subprocess.run( [self.adb, "reboot", extra] )

	def _log(self, message):
		f = open(self.logfile, "a")
		f.write( "[" + str(datetime.utcnow()) + "]: " + str(message) )
		f.close()
