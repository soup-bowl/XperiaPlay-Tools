from xpt import Com
from os.path import isfile, join
from sys import platform
from subprocess import TimeoutExpired
from typing import Union
import re
import tempfile
import zipfile

class Fastboot(Com):
	def __init__(self):
		super().__init__()
		self.fastboot = self.platform + "/fastboot"

		self.device_id     = None
		self.device_model  = None
		self.device_secure = True
		vno = self.get_version()
		if vno != None:
			self.available = True
			self._log("Initating Fastboot, using " + self.get_version() + " found at " + self.fastboot + " on " + platform)
		else:
			self.available = False

	def get_version(self) -> Union[str, None]:
		"""Checks the Fastboot version.

		Returns:
			Union[str, None]: The version number, or a problem encountered trying to reach the executable.
		"""
		try:
			response = self.run( [self.fastboot, "--version"] )
		except:
			self._log("Get version failed.")
			return None

		return re.findall( "version\s*(.*)", str.splitlines( response.stdout)[0] )[0]
	
	def get_devices_connected(self) -> Union[list, None]:
		"""Gets the currently connected Android devices in Fastboot.

		Returns:
			Union[list, None]: A list of Fastboot identifiers, or nothing.
		"""
		devices  = []
		response = str.splitlines( self.run( [self.fastboot, "devices"] ).stdout )
		if len( response ) == 0:
			self._log("No fastboot devices found.")
			return None

		for val in response:
			devices.append( str.split(val, '\t')[0] )

		self._log(str(len(devices)) + " fastboot devices found.")
		return devices

	def set_device(self, device) -> None:
		"""Set the device to be worked on (get them using get_devices_connected()).

		Args:
			device (str): Device identifier from Fastboot devices.
		"""
		self.device_id = device

		try:
			model = self.run( [self.fastboot, "getvar", "product"] )
			self.device_model = re.findall( "product:\s*(.*?)\\n", model.stderr)[0]
			secure = self.run( [self.fastboot, "getvar", "secure"] )
			secure = re.findall( "secure:\s*(.*?)\\n", secure.stderr)[0]
			if secure == 'no':
				self.device_secure = False
		except TimeoutExpired:
			self._log("Fastboot connector timeout of 200 seconds hit - try rebooting and/or a different USB port?")
			self.device_model  = None
			self.device_secure = True
			return None

		self._log("Fastboot device set as " + self.device_model)

	def reboot_device(self) -> None:
		"""Reboots the device.
		"""
		if self.device_id == None:
			return None
		
		self.run( [self.fastboot, "reboot"] )

	def flash_ftf(self, file, mode, print_output = False) -> bool:
		"""Flashes a sin file to the active fastboot device.

		Args:
			file (str): Location of sin file (will be extracted to TMP).
			mode (int): 1 for boot, 2 for system, 3 for both, 4 for entire.
			print_output (bool): Print the running comand to screen.

		Returns:
			bool: Success status.
		"""
		if self.device_id == None:
			return False
		
		fmode = []
		if mode == 1:
			fmode.append('boot')
		elif mode == 2:
			fmode.append('system')
		elif mode == 3:
			fmode.append('boot')
			fmode.append('system')
		elif mode == 4:
			fmode.append('boot')
			fmode.append('system')
			fmode.append('userdata')
		else:
			return False

		with tempfile.TemporaryDirectory() as dirpath:
			with zipfile.ZipFile(file, 'r') as zip_ref:
				self._log("Flash executed - File: " + file + "; Mode: " + str(mode))
				
				try:
					zip_ref.extractall(dirpath)
				except:
					self._log("Error: Unexpected error during ftf extraction. Possibly a corrupt firmware?")
					raise

				for partiton in fmode:
					if partiton == 'boot':
						ffile = 'kernel.sin'
					if partiton == 'system':
						ffile = 'system.sin'
					if partiton == 'userdata':
						ffile = 'userdata.sin'

					self._flash_firmware(dirpath + '/' + ffile, partiton, print_output)

		return True


	def _flash_firmware(self, file, partition, print_output = False) -> None:
		"""Flashes the specified file to the partition.

		Args:
			file (str): Path directly to the desired .sin or .img file.
			partition (str): Partition label.
			print_output (bool): Print the running comand to screen.
		"""
		if self.device_id == None:
			return None

		if isfile(file):
			# Timeout is 2 hours. If it goes on longer than this, something is seriously wrong.
			if print_output:
				print("> fastboot flash " + partition + ' ' + file)

			self.run( [self.fastboot, "flash", partition, file], True, 7200 )
		else:
			self._log("Could not find " + file + " for " + str(partition) + " flash - skipping.")
			return None
