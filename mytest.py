#!/usr/bin/env python
from selenium import webdriver
import unittest
from ConfigParser import ConfigParser
conf_file = open('config/config.conf')
config = ConfigParser()
config.readfp(conf_file)

class TestSample(unittest.TestCase):
		def setUp(self):
				self.driver = webdriver.Firefox()
				self.driver.implicitly_wait(30)
				self.driver.maximize_window()        
				set_base_url = config.get("set_url",'url')
				self.base_url = set_base_url
				print self.base_url
				self.verificationErrors = []

		def test_name_verification(self):
				print "Test my first feature"

		def tearDown(self):
				self.driver.close()

if __name__ == '__main__':
	unittest.main()