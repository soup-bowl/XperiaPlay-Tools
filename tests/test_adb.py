from xpt import ADB

import unittest


class ADBTestSuite(unittest.TestCase):
	"""Android Debugging Bridge test cases."""

	def test_get_version_returns(self):
		adb = ADB()
		ver = adb.get_version()
		self.assertIsNotNone(ver)


if __name__ == '__main__':
	unittest.main()
