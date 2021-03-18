from xpt import ADB, Fastboot
from os import listdir
from os.path import isfile, join

adb      = ADB()
fastboot = Fastboot()

mode = 0
if adb.get_devices_connected() != None:
	mode = 1
elif fastboot.get_devices_connected() != None:
	mode = 2

if mode == 1:
	adb.set_device( adb.get_devices_connected()[0] )
	print("Detected Xperia PLAY " + adb.device_model + " in Android Debugging mode.")
	print("What do you want to do?")
	print("")
	if adb.device_is_rooted():
		print("[-] Device is rooted.")
	else:
		print("[1] Root device.")
	print("[2] Install all apps.")
	print("[3] Remove recognised bloatware (experimental - Requires root).")
	print("")
	print("[r] Reboot device ([f] into fastboot).")
	print("[q] Cancel.")
	print("")
	choice = input("Select one: ")

	if choice == "1":
		if adb.device_is_rooted():
			print("Device is already rooted. Exiting.")
			exit()
		print("Rooting device using the zergRush method.")
		adb.init_zergrush_root()
		print("Done. Rebooting...")
	elif choice == "r":
		print("Rebooting...")
		adb.reboot_device()
	elif choice == "f":
		print("Rebooting into bootloader...")
		adb.reboot_device(True)
	else:
		print("Exited.")
elif mode == 2:
	fastboot.set_device( fastboot.get_devices_connected()[0] )
	print("Detected Xperia PLAY " + fastboot.device_model + " in fastboot mode.")
	print("What do you want to do?")
	print("")
	print("[1] Flash firmware.")
	print("")
	print("[r] Reboot device.")
	print("[q] Cancel.")
	print("")
	choice = input("Select one: ")

	if choice == "1":
		print("Select firmware?")
		print("")
		path = "./resources/firmwares"
		ftfs = [f for f in listdir(path) if isfile(join(path, f))]
		for index, ftf in enumerate(ftfs, start=0):
			print("[" + str(index) + "] " + ftf + ".")
		print("")
		print("[q] Quit.")
		choice_fw = input("Select one: ")
		
		try:
			fw = ftfs[int(choice_fw)]
			print(fw)
		except (IndexError, ValueError) as e:
			print("Firmware invalid or opted to quit - exited.")
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
		choice = input("Select one: ")
		if choice == "1" or choice == "2" or choice == "3" or choice == "4":
			fastboot.flash_ftf( "./resources/firmwares/" + fw, int(choice) )
			fastboot.reboot_device()
		else:
			print("Exited.")
	elif choice == "r":
		fastboot.reboot_device()
	else:
		print("Exited.")
else:
	print("Could not find an Android device in either ADB or Fastboot status. Exited.")
