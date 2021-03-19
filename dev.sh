#! /bin/bash
# For development purposes only. Release versions on GitHub should come pre-rolled with the platform tools, and
# the firmware files can be obtained from the dedicated Reddit/Discord to Xperia Play.
# https://www.mediafire.com/folder/729cecjag0n9l/Sony_Xperia_Play
# This only needs to be downloaded once - please do not excessively re-download these files.

case "$OSTYPE" in
	"linux"*)
		curl -o ./resources/pt.zip https://files.soupbowl.io/xperia/platform-tools/platform-tools_r26.0.1-linux.zip
		unzip -o ./resources/pt.zip -d ./resources
		rm ./resources/pt.zip
		;;

	"darwin"*)
		curl -o ./resources/pt.zip https://files.soupbowl.io/xperia/platform-tools/platform-tools_r26.0.1-darwin.zip
		unzip -o ./resources/pt.zip -d ./resources
		rm ./resources/pt.zip
		;;

	*)
		echo "Unexpected platform: ${OSTYPE} - expecting 'linux*' or 'darwin*'."
		;;
esac