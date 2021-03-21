from xpt import ADB, Fastboot, Download, __version__
from os import listdir
from os.path import isfile, join

def main() -> None:
	"""Triggers the guided xtools process, running through both Android Debugging and Fastboot.
	"""

	print("Xperia Play Tools by soup-bowl - Version " + __version__)

	adb      = ADB()
	fastboot = Fastboot()

	adb_devices = adb.get_devices_connected()
	fbt_devices = fastboot.get_devices_connected()

	mode = 0
	if adb_devices != None:
		mode = 1
	elif fbt_devices != None:
		mode = 2

	if mode == 1:
		adb_path( adb, adb_devices[0] )
	elif mode == 2:
		fastboot_path( fastboot, fbt_devices[0] )
	else:
		print("Could not find an Android device in either ADB or Fastboot status.")
		print("- For ADB access, ensure Android Debugging is enabled. The setting can be found (Android 2.3) in Applications > Development > USB Debugging.")
		print("- For fastboot, ensure your device is powered off. Then, plug into USB whilst holding down the magnifying glass button. If done correctly, the power button should illuminate blue.")

def adb_path(adb, device) -> None:
	"""Android Debugging Bridge pathway.

	Args:
		adb (ADB): The active ADB object.
		device (str): The device of operation identifier.
	"""
	adb.set_device( device )
	if adb.device_model == None:
		print("Error: Found device in android debugging mode, but a problem occurred during identification. Check system.log for more details.")
		exit(1)
	print("Detected Xperia Play " + adb.device_model + " on Android " + adb.device_version + " (" + adb.device_build + ") in USB Debugging mode.")
	print("What do you want to do?")
	print("")
	if adb.device_is_rooted():
		print("[-] Device is rooted.")
	elif adb.device_is_rootable():
		print("[1] Root device (zergRush).")
	else:
		print("[-] Root device (fw not supported).")
	print("[2] Install all apps (" + str(adb.get_app_count()) + " found).")
	if adb.device_is_rooted():
		print("[3] Remove recognised bloatware (experimental).")
	print("")
	print("[r] Reboot device ([f] into fastboot).")
	print("[q] Cancel.")
	print("")
	choice = input("[adb] Select one: ")

	if choice == "1":
		if adb.device_is_rooted():
			print("Device is already rooted. Exiting.")
			exit()
		elif adb.device_is_rootable():
			print("Rooting device using the zergRush method.")
			adb.init_zergrush_root()
			print("Done. Rebooting...")
		else:
			print("No root method for " + adb.device_model + " " + adb.device_version + " (" + adb.device_build + ").")
	if choice == "2":
		adb.install_all_apps(True)
		print("Completed - exiting.")
	if choice == "3":
		if not adb.device_is_rooted():
			print("Device must be rooted for this action to be performed. Exiting.")
			exit()
		print("This experimental feature will remove apps determined to be bloatware, or otherwise unnessesary for modern usage.")
		print("Based upon information found here - https://revive.today/xpapk (cellular).")
		print("Further apps can be removed without detrimental effects depending on use, see the document linked above.")
		print("If you encounter issues, please report them at the GitHub tracker - https://github.com/soup-bowl/XperiaPlay-Tools.")
		print("THIS IS REMOVING SYSTEM APPS - BACKUP IMPORTANT DATA BEFORE EXECUTING THIS SCRIPT.")
		print("")
		choice = input("Do you wish to continue? [y/N]: ")
		if choice == "y":
			apps = []
			with open('./resources/removals.txt') as f:
				apps = [line.rstrip() for line in f]
			
			for app in apps:
				print("\rRemoving: " + app, end=" ")
				adb.remove_system_app(app)
			
			print("")
			print("Complete. Rebooting...")
			adb.reboot_device()
			exit()
		else:
			print("Exiting.")
			exit()
	elif choice == "r":
		print("Rebooting...")
		adb.reboot_device()
	elif choice == "f":
		print("Rebooting into bootloader...")
		adb.reboot_device(True)
	else:
		print("Exited.")

def fastboot_path(fastboot, device) -> None:
	"""Fastboot pathway.

	Args:
		fastboot (Fastboot): The active Fastboot object.
		device (str): The device of operation identifier.
	"""
	fastboot.set_device( device )
	if fastboot.device_model == None:
		print("Error: Found device in fastboot mode, but a problem occurred during identification. Check system.log for more details.")
		exit(1)
	print("Detected Xperia Play " + fastboot.device_model + " in fastboot mode.")
	print("What do you want to do?")
	print("")
	print("[1] Flash firmware.")
	print("")
	print("[r] Reboot device.")
	print("[q] Cancel.")
	print("")
	choice = input("[fastboot] Select one: ")

	if choice == "1":
		choice_fw = file_selection("Select firmware?", "./resources/firmwares", 'ftf', {"i": "Download R800i firmware pack."})

		if choice_fw == "i":
			print("Requesting pack from server. This may take some time to download, please wait...")
			success = Download().download_firmware("R800i")
			if success:
				print("Firmware pack downloaded. They should now appear in the firmware selector.")
				exit()
			else:
				print("Error: A problem was encountered. Check the system.log file to see why.")
				exit(1)
		elif choice_fw == "q":
			print("Exited.")
			exit()

		print("What level of flash do you want?")
		print("This tool will not interact with baseband, please use flashtool for a complete flash instead.")
		print("")
		print("[1] Flash kernel.")
		print("[2] Flash system.")
		print("[3] Flash kernel + system.")
		print("[4] Complete flash.")
		print("[q] Cancel.")
		print("")
		choice = input("[" + choice_fw + "] Select one: ")
		if choice == "1" or choice == "2" or choice == "3" or choice == "4":
			print("Flashing device - do not disconnect your phone...")
			try:
				fastboot.flash_ftf( "./resources/firmwares/" + choice_fw, int(choice), True )
			except:
				print("Error: Hit a problem during the firmware flash. Check the system.log to understand why.")
				exit(1)
			print("")
			print("Flash complete - rebooting...")
			fastboot.reboot_device()
		else:
			print("Exited.")
	elif choice == "r":
		fastboot.reboot_device()
	else:
		print("Exited.")
	
def file_selection(label, directory, extension, additionals = {}) -> str:
	"""Generates a file selection CLI dialog.

	Args:
		label (str): Title to show at the top.
		directory (str): Directory to enumerate.
		extension (str): Desired file extension.
		additionals (dict, optional): Any additional options desired.

	Returns:
		str: Either the chosen filename, the additional option, or as a catch-all - (q)uit.
	"""
	print(label)
	print("")
	ftfs = [f for f in listdir(directory) if isfile(join(directory, f))]
	for index, file in enumerate(ftfs, start=0):
		print("[" + str(index) + "] " + file + ".")
	print("")
	for key, additional in additionals.items():
		print("[" + key + "] " + additional)
	print("[q] Quit.")

	selected = input("[Flash] Select one: ")

	try:
		fw = ftfs[int(selected)]
		return fw
	except:
		for key, additional in additionals.items():
			if key == selected:
				return key
		return "q"
