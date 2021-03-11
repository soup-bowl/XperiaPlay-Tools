#! /bin/bash
echo "XPlayADB by soup-bowl - Version 0.1-Alpha"
echo "Works with R800i on Linux-based commands with fastboot."
echo "-----------------------------"

# Trims response from adb shell.
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

isplugged=`adb get-state`
if [[ $isplugged == "" ]]
then
	echo ""
	echo "Unable to get an Android Debugging response from phone."
	echo "Make sure that your phone:"
	echo "1) Is plugged in to a USB port with a cable that supports data transmission."
	echo "2) USB Debugging is enabled in settings > Applications > Development > USB debugging."
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

isrootcmd=$(adb shell stat /system/bin/su 2>&1)
if [[ $isrootcmd == *"No such file or"* || $isrootcmd == *"permission den"* ]]
then
	echo "Xperia is not rooted (no su detected or permission denied)."
else
	echo "Xperia appears to be rooted (su detected)."
fi

echo "" >> ./system.log
echo "Starting xdb for $device" >> ./system.log
date >> ./system.log
echo "---------------" >> ./system.log

# --- Identify user desires ---
echo "What do you want to do?"
echo ""
echo "[1] Root device."
echo "[2] Install apps."
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

		trim $(adb shell echo true) 'resp'
		if [[ $resp != "true" ]]
		then
			echo "Error: Unable to run commands on device. Ensure ONLY the Xperia PLAY is plugged in, and Android Debugging is enabled."
			exit 1
		fi

		echo "> Preparing for exploit."
		adb shell "mkdir /data/local/rootmp" >> ./system.log
		adb push root/zergRush /data/local/rootmp/. >> ./system.log
		adb shell "chmod 777 /data/local/rootmp/zergRush" >> ./system.log
		echo "> Running zergRush exploit."
		adb shell "./data/local/rootmp/zergRush" >> ./system.log
		echo "> Exploit complete, waiting for device to re-appear."
		adb wait-for-device
		echo "> Installing BusyBox."
		adb push root/busybox /data/local/rootmp/. >> ./system.log
		adb shell "chmod 755 /data/local/rootmp/busybox" >> ./system.log
		adb shell "/data/local/rootmp/busybox mount -o remount,rw /system" >> ./system.log
		adb shell "dd if=/data/local/rootmp/busybox of=/system/xbin/busybox" >> ./system.log
		adb shell "chmod 04755 /system/xbin/busybox" >> ./system.log
		adb shell "/system/xbin/busybox --install -s /system/xbin" >> ./system.log
		echo "> Enabling the su (superuser) command."
		adb push root/su /system/bin/su >> ./system.log
		adb shell "chown 0:0 /system/bin/su" >> ./system.log
		adb shell "chmod 06755 /system/bin/su" >> ./system.log
		adb shell "rm /system/xbin/su" >> ./system.log
		adb shell "ln -s /system/bin/su /system/xbin/su" >> ./system.log
		echo "> Installing Superuser."
		adb push root/Superuser.apk /system/app/. >> ./system.log
		adb shell "rm -r /data/local/rootmp" >> ./system.log
		echo ""
		echo "Device rooted. Rebooting..."
		adb reboot
		exit
		;;
	
	"2")
		apks=($( ls apps/*.apk ))
		for ((i=0; i<${#apks[@]}; i++))
		do
			adb install ${apks[$i]} >> ./system.log
		done
		exit
		;;
	
	"r")
		echo "Rebooting. xfast command will work in fastboot mode."
		adb reboot bootloader >> ./system.log
		exit
		;;

	*)
		echo "Exited."
		exit
		;;
esac
