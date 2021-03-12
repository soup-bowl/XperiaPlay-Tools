# 📲 Xperia PLAY Tools
⚠️ **This tool is in active development and is unstable!** There is a high chance it may operate unexpectedly and/or brick your device, so use with caution.

The correct method for this device is to use **[Flashtool](https://github.com/Androxyde/Flashtool)**, older versions work more effectively with the Xperia PLAY.
[See this Reddit Wiki](https://www.reddit.com/r/xperiaplay/wiki/index#wiki_flashtool) for the best information.

To begin, open a terminal into the directory and run `./xtools`. This comes pre-rolled with multi-platform **Android Debugging Bridge 1.0.39**.

To get a starter subset of files in the development version, run `./dev.sh`. This will grab a selection of R800i firmwares, apps and platform tools.

## 🤖 xdb (adb - Android Debugging Bridge)
This provides interactions with the running firmware. Currently you can:
* Root the device using zergRush (exploitable firmwares only - based upon [DooMLoRD implementation](https://forum.xda-developers.com/t/04-jan-rooting-unrooting-doomlords-easy-rooting-toolkit-v4-0-zergrush-exploit.1321582/)).
* Automatically install apps from a folder of apks.

Tested against R800i only.

## 🐞 xfast (fastboot)
The experimental nature is that instead of operating how flashtool does (boot device into flash mode, then sending the payloads), this is instead passing the .sin files via fastboot, as you would an .img file. Rather surprisingly, this has so far been successful on a test R800i device. This dummy device has experienced other problems (unable to correctly flash a custom Recovery and/or ROM), so I am not able to 100% verify this tool. **Use this at your own risk**

Firmwares can be placed in the `firmwares` folder and selected as so.

[adb-win]: https://dl.google.com/android/repository/platform-tools_r26.0.1-windows.zip
[adb-mac]: https://dl.google.com/android/repository/platform-tools_r26.0.1-darwin.zip
[adb-lnx]: https://dl.google.com/android/repository/platform-tools_r26.0.1-linux.zip
