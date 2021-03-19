from datetime import datetime
import subprocess

class Com(object):
	def __init__(self):
		self.platform = "./resources/platform-tools/"
		self.firmdir  = "./resources/firmwares/"
		self.rootdir  = "./resources/root/"
		self.appdir   = "./resources/apps/"
		self.logfile  = "./system.log"

	def is_available(self) -> bool:
		"""For checking if the active tool is available on the system.

		Returns:
			bool: Status on the presence in the system.
		"""
		return self.available
	
	def run(self, command, log = True, timeout = 60) -> subprocess.CompletedProcess:
		"""System call handler.

		Args:
			command (array): Command to be run on the system.
			log (bool, optional): Whether the system.log will be in use. Defaults to True.
			timeout (int, optional): Set a higher/lower timeout. Defaults to 60.

		Returns:
			subprocess.CompletedProcess: Contains stdout and stderr information.
		"""
		response = subprocess.run( command, capture_output=True, text=True, timeout=timeout )
		if log:
			if response.stdout != "": self._log("Info: " + response.stdout)
			if response.stderr != "": self._log("Error: " + response.stderr)

		return response

	def _log(self, message) -> None:
		"""Logs the message to the internally specified file.

		Args:
			message (string): Message
		"""
		if self.logfile != False and message != "":
			f = open(self.logfile, "a")
			f.write( "\n[" + str(datetime.utcnow()) + "]: " + str(message).strip() )
			f.close()