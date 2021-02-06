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
if [ -d "./prepared" ]; then
    echo "A previous prepared firmware was found. Removing..."
	rm -r prepared/
fi
unzip -q $file -d ./prepared
echo "Extraction complete."

echo "What level of flash do you want?"
echo ""
echo "[1] Flash kernel."
echo "[2] Flash system."
echo "[3] Flash kernel + system."
#echo "[4] Complete flash."
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

  *)
	rm -r prepared/
	echo "Clean up and exited."
	exit
	;;
esac

echo "Passing instructions over to fastboot."
devchk=`fastboot devices`

for i in "${commands[@]}"
do
	echo "> fastboot flash $i" 
	fastboot flash $i
done

echo "Flashing complete, rebooting..."
fastboot reboot &> /dev/null

exit
