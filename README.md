# 📲 Xperia Play Tools
⚠️ **This tool is in active development and is unstable!** There is a high chance it may operate unexpectedly and/or brick your device, so use with caution.

The correct method for this device is to use **[Flashtool](https://github.com/Androxyde/Flashtool)**, older versions work more effectively with the Xperia Play.
[See this Reddit Wiki](https://www.reddit.com/r/xperiaplay/wiki/index#wiki_flashtool) for the best information.

## 💽 Installation
**[Download the latest release version](https://github.com/soup-bowl/XperiaPlay-Tools/releases/latest)**. The tool should work on **Windows, macOS (Intel) and Linux**.

**⚠️ I don't have a macOS or Windows machine to test with. Use with caution - testers welcome.**

**Python 3.X** (tested on 3.8) is required for this tool to work.

### 🪟 Windows
Go to the [Python website][pywin] and download the latest Python 3 **Windows installer** for your copy of Windows (xx-bit doesn't matter). Ensure during installation that **add to PATH is checked**, otherwise xtools will not be able to detect it.

This tool should run on **Windows 7 and higher**, so long as **Python 3** and **Powershell** is available. If Powershell is not available, you can run the tool manually by running `python -m xpt` in the project directory.

### 🍎 OSX/macOS
Recommend installing via Brew using the following command:

`brew install python3`

### 🐧 Linux
Install Python3 using your distributions package manager.

* Debian-based: `sudo apt install python3`
* Fedora-based: `sudo dnf install python3`

You can test the success on all three by opening a Terminal window and running `python3 --version` (no 3 on Windows). 

## 🖥 Usage
Double click on, or open a terminal into the directory and run `./xtools` / `./xtools.ps1` to open the interactive client. This comes pre-rolled with multi-platform **Android Debugging Bridge 1.0.39**, to ensure all development and testing is done with a unified version.

### 🤖 xdb (adb - Android Debugging Bridge)
This provides interactions with the running firmware. Currently you can:
* Root the device using zergRush (exploitable firmwares only - based upon [DooMLoRD implementation](https://forum.xda-developers.com/t/04-jan-rooting-unrooting-doomlords-easy-rooting-toolkit-v4-0-zergrush-exploit.1321582/)).
* Automatically install apps from a folder of apks.
* Remove bloatware apps from the [app removal list][applist] (experimental).

Tested against R800i only.

### 🐞 xfast (fastboot)
The experimental nature is that instead of operating how flashtool does (boot device into flash mode, then sending the payloads), this is instead passing the .sin files via fastboot, as you would an .img file. Rather surprisingly, this has so far been successful on a test R800i device. This dummy device has experienced other problems (unable to correctly flash a custom Recovery and/or ROM), so I am not able to 100% verify this tool. **Use this at your own risk**

Firmwares can be placed in the `firmwares` folder and selected as so.

## ⚠️ Windows Virus Alert
Windows Defender will detect that zergRush as a virus. This is **not a genuine virus** and when prompted, you can safely allow on your computer.

### ❓ Why?
This is because the nature of zergRush is to open up an exploit on Android to allow us to install the root payload. Since this is utilising an exploit on the phone, it can also be leveraged by hackers, thereby classifying it as a security threat.

The script will only use this exploit to install the Superuser capabilities, and will not harm your computer or device.

[pywin]: https://www.python.org/downloads/windows/
[applist]: https://revive.today/xpapk
[adb-win]: https://dl.google.com/android/repository/platform-tools_r26.0.1-windows.zip
[adb-mac]: https://dl.google.com/android/repository/platform-tools_r26.0.1-darwin.zip
[adb-lnx]: https://dl.google.com/android/repository/platform-tools_r26.0.1-linux.zip
