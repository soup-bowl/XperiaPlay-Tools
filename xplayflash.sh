#! /bin/bash

file=`realpath $1`

# Check if Android ADB has been installed.
if ! command -v fastboot &> /dev/null
then
	echo "Error: ADB package (specifically fastboot) not found."
	exit
fi

if [ ${file: -4} != ".ftf" ]
then
	echo "Error: Input is not an .ftf file."
	exit
fi

echo "Preparing $1 for flashing."
unzip -q $file -d ./prepared
echo "Extraction complete."

echo "What level of flash do you want?"
echo ""
echo "[1] Flash kernel."
echo "[2] Flash system."
echo "[3] Flash kernel + system."
echo "[4] Complete flash (TBD)."
echo "[q] Cancel."
echo ""
read -p 'choose [q]: ' choice

commands=()
case "$choice" in

  "1")
	if test -f "./prepared/kernel.sin"; then commands+=( 'boot' `realpath ./prepared/kernel.sin` ); fi
	;;

  "2")
	if test -f "./prepared/system.sin"; then commands+=( 'system' `realpath ./prepared/system.sin` ); fi
	;;

  "3")
	if test -f "./prepared/kernel.sin"; then commands+=( 'boot' `realpath ./prepared/kernel.sin` ); fi
	if test -f "./prepared/system.sin"; then commands+=( 'system' `realpath ./prepared/system.sin` ); fi
	;;

  *)
	rm -r prepared/
	echo "Clean up and exited."
	exit
	;;
esac

echo ${commands[*]}
exit
