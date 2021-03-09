#! /bin/bash
echo "XPlayADB by soup-bowl - Version 0.1-Alpha"
echo "Works with R800i on Linux-based commands with fastboot."
echo "-----------------------------"

# Trims $1
# If $2 supplied, assigns result to variable named $2
# If $2 not present, echoes the value to stdout
# Modified from https://stackoverflow.com/a/43432097
trim()
{
	if [[ $1 =~ ^[[:space:]]*(.*[^[:space:]])[[:space:]]*$ ]]
	then
		local result="${BASH_REMATCH[1]}"
	else
		local result="$1"
	fi
	eval $2=$result
}

# --- Pre-run tests ---
# Test for ADB.
if ! command -v adb > /dev/null 2>&1
then
	echo "Error: ADB package not found."
	exit 1
fi

trim $(adb shell getprop ro.product.model) 'device'
if [[ $device == "R800i" ]]
then
	echo "Xperia PLAY $device detected!"
else
	echo "Device identifer was incorrect. Discovered '$device'. Expecting R800i."
	exit 1
fi

# --- Identify user desires ---
echo "What do you want to do?"
echo ""
echo "[1] Root device."
echo ""
echo "[r] Reboot into fastboot."
echo "[q] Cancel."
echo ""
read -p 'choose [q]: ' choice

commands=()
case "$choice" in
	"1")
		# Thanks to DooMLoRD for the original impelementations.
		# Based upon:
		# https://forum.xda-developers.com/t/04-jan-rooting-unrooting-doomlords-easy-rooting-toolkit-v4-0-zergrush-exploit.1321582/
		# https://forum.xda-developers.com/t/how-to-zergrush-root-root-w-v2-2-x-2-3-x-not-ics-4-x-or-gb-after-11-2011.1312859/

		#resp=`adb shell echo true`
		#if [[ $resp != true ]]
		#then
		#	echo "Error: Unable to run commands on device. Ensure ONLY the Xperia PLAY is plugged in, and Android Debugging is enabled."
		#	exit 1

		echo "Preparing for exploit."
		adb shell "mkdir /data/local/rootmp"
		adb push root/zergRush /data/local/rootmp/.
		adb shell "chmod 777 /data/local/rootmp/zergRush"
		echo "Running zergRush exploit."
		adb shell "./data/local/rootmp/zergRush"
		echo ""
		echo "Exploit complete, waiting for device to re-appear."
		adb wait-for-device
		echo "Installing BusyBox."
		adb push root/busybox /data/local/rootmp/.
		adb shell "chmod 755 /data/local/rootmp/busybox"
		adb shell "/data/local/rootmp/busybox mount -o remount,rw /system"
		adb shell "dd if=/data/local/rootmp/busybox of=/system/xbin/busybox"
		adb shell "chmod 04755 /system/xbin/busybox"
		adb shell "/system/xbin/busybox --install -s /system/xbin"
		echo ""
		echo "Enabling the su (superuser) command."
		adb push root/su /system/bin/su
		adb shell "chown 0:0 /system/bin/su"
		adb shell "chmod 06755 /system/bin/su"
		adb shell "rm /system/xbin/su"
		adb shell "ln -s /system/bin/su /system/xbin/su"
		echo ""
		echo "Installing Superuser."
		adb push root/Superuser.apk /system/app/.
		adb shell "rm -r /data/local/rootmp"
		echo ""
		echo "Device rooted. Rebooting..."
		adb reboot
		exit
		;;
	
	"r")
		echo "Rebooting. xfast command will work in fastboot mode."
		adb reboot bootloader
		exit
		;;

	*)
		echo "Exited."
		exit
		;;
esac
