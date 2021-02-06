# Xperia PLAY - Sin Flasher
**Do not use this tool** this is largely experimental, there is a high chance it may operate unexpectedly and/or brick your device.

The experimental nature is that instead of operating how flashtool does (boot device into flash mode, then sending the payloads), this is instead passing the .sin files via fastboot, as you would an .img file. Rather surprisngly, this has so far been successful on a test R800i device. This dummy device has experienced other problems (unable to correctly flash a custom Recovery and/or ROM), so I am not able to 100% verify this tool. **Use this at your own risk**

The correct method for this device is to use **[Flashtool](https://github.com/Androxyde/Flashtool)**, older versions work more effectively with the Xperia PLAY.
[See this Reddit Wiki](https://www.reddit.com/r/xperiaplay/wiki/index#wiki_flashtool) for the best information.