from xpt import Fastboot

import unittest


class FastbootTestSuite(unittest.TestCase):
	"""Fastboot test cases."""

	def test_get_version_returns(self):
		fbt = Fastboot()
		ver = fbt.get_version()
		self.assertIsNotNone(ver)


if __name__ == '__main__':
	unittest.main()
