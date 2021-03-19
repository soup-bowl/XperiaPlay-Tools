from xpt import Com
import tempfile
import zipfile
import urllib.request
import shutil

class Download(Com):
	def __init__(self):
		super().__init__()

	def download_firmware(self, model) -> bool:
		"""Downloads firmware from soupbowl.io.

		Args:
			model (string): Device model.

		Returns:
			bool: Success status.
		"""
		if model == "R800i":
			with tempfile.TemporaryDirectory() as dirpath:
				url = "https://files.soupbowl.io/xperia/firmwares/R800i.zip"
				req = urllib.request.Request(url, headers={'User-Agent': 'XPlaytools/1.0'})

				try:
					with urllib.request.urlopen(req) as response, open(dirpath + "/R800i.zip", 'wb') as out_file:
						shutil.copyfileobj(response, out_file)
						with zipfile.ZipFile(dirpath + "/R800i.zip", 'r') as zip_ref:
							zip_ref.extractall(self.firmdir)
				except:
					self._log("Error: A HTTP error occurred during request.")

			return True
		else:
			return False

