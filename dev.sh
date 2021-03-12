#! /bin/bash
# For development purposes only. Release versions on GitHub should come pre-rolled with the platform tools, and
# the firmware files can be obtained from the dedicated Reddit/Discord to Xperia PLAY.
# https://www.mediafire.com/folder/729cecjag0n9l/Sony_Xperia_Play
# This only needs to be downloaded once - please do not excessively re-download these files.
curl -o ./xpt-dev.zip https://files.soupbowl.io/xpt-dev.zip
unzip -o xpt-dev.zip
rm xpt-dev.zip
