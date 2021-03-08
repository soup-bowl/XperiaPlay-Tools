#! /bin/bash
echo "XPlayFlash by soup-bowl - Version 0.1-Alpha"
echo "Works with R800i on Linux-based commands with fastboot."
echo "-----------------------------"

# --- Pre-run tests ---
# Test for ADB.
if ! command -v fastboot > /dev/null 2>&1
then
	echo "Error: ADB package (specifically fastboot) not found."
	exit 1
fi

if [[ -z "$1" ]]
then
	echo "Error: No flash file (.ftf) specified."
	exit
fi
file=`realpath $1`

# Test file input.
if [[ ${file: -4} != ".ftf" ]]
then
	echo "Error: Input is not an .ftf file (spaces in the path can cause problems too)."
	exit 1
fi

isplugged=`fastboot devices 2>&1`
if [[ $isplugged == "" ]]
then
	echo "Fastboot on your system was found, but has detected no connected devices. Please connect your Xperia in fastboot mode first."
	echo "Fastboot is achieved by turning off your Xperia PLAY, and holding the magnifying glass button down whilst plugging in."
	exit
fi

# Remove leftover firmware files.
echo "Preparing $1 for flashing."
if [ -d "./prepared" ]
then
	echo "A previous prepared firmware was found. Removing..."
	rm -r prepared/
fi
unzip -q $file -d ./prepared
echo "Extraction complete."

# --- Identify user desires ---
echo "What level of flash do you want?."
echo "This tool will not interact with baseband, please use flashtool for a complete flash instead."
echo ""
echo "[1] Flash kernel."
echo "[2] Flash system."
echo "[3] Flash kernel + system."
echo "[4] Complete flash."
echo "[q] Cancel."
echo ""
read -p 'choose [q]: ' choice

commands=()
case "$choice" in
	"1")
		if test -f "./prepared/kernel.sin"; then cominpt=`realpath ./prepared/kernel.sin`; commands+=( "boot $cominpt" ); fi
		;;

	"2")
		if test -f "./prepared/system.sin"; then cominpt=`realpath ./prepared/system.sin`; commands+=( "system $cominpt" ); fi
		;;

	"3")
		if test -f "./prepared/kernel.sin"; then cominpt=`realpath ./prepared/kernel.sin`; commands+=( "boot $cominpt" ); fi
		if test -f "./prepared/system.sin"; then cominpt=`realpath ./prepared/system.sin`; commands+=( "system $cominpt" ); fi
		;;

	"4")
		if test -f "./prepared/kernel.sin"; then cominpt=`realpath ./prepared/kernel.sin`; commands+=( "boot $cominpt" ); fi
		if test -f "./prepared/system.sin"; then cominpt=`realpath ./prepared/system.sin`; commands+=( "system $cominpt" ); fi
		if test -f "./prepared/userdata.sin"; then cominpt=`realpath ./prepared/userdata.sin`; commands+=( "userdata $cominpt" ); fi
		;;

	*)
		rm -r prepared/
		echo "Clean up and exited."
		exit
		;;
esac

# --- Detect Device ---
devindt=`fastboot getvar product 2>&1` # FB writes the response to stderr
devindt=`echo $devindt | cut -f2 -d ":" | cut -f2 -d " "`

# --- Fastboot Command Execution ---
if [[ $devindt == "R800i" || $devindt == "R800x" ]]
then
	echo "Xperia PLAY $devindt detected - Passing instructions over to fastboot."
	for i in "${commands[@]}"
	do
		echo "> fastboot flash $i" 
		fastboot flash $i
	done

	echo "Flashing complete, rebooting..."
	fastboot reboot &> /dev/null
else
	echo "Device identifer was incorrect. Discovered '$devindt'. Expecting R800i, or R800x."
fi

rm -r prepared/
echo "Clean up and exited."
exit
