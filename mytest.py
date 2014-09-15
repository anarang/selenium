#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time
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
			global browser
			browser = self.driver
			self.verificationErrors = []

		def test_list_verification(self):
			browser.get(self.base_url)
			browser.find_element_by_id("myName").send_keys("Ann")
			browser.find_element_by_id("myName").send_keys(Keys.RETURN)
			my_name = browser.find_element_by_id("tell").text
			my_name = my_name.split(' ')[2]
			print my_name
			self.assertEqual("Ann",my_name,"Name not displayed correctly")
			
			browser.find_element_by_id("yourName").send_keys("Zara")
			browser.find_element_by_id("yourName").send_keys(Keys.RETURN)
			your_name = browser.find_element_by_id("yourName").text
			your_name = your_name.split(' ')[1]
			self.assertEqual("Zara",your_name,"Your name is not displayed correctly")

			browser.find_element_by_id("gotoList").click()
			browser.find_element_by_id("showList").click()
			p =  browser.find_element_by_id("pyList")
			frameworks = ["Django","Flask"]
			for f in frameworks:
				self.assertIn(f, p.text.split("\n"), "Desired elements not present in list")

		def test_image_presence(self):
			whoa_url = self.base_url + "/whoa.html"
			browser.get(whoa_url)
			browser.find_element_by_id("showWhoa").click()
			browser.find_element_by_xpath("//p[@id='pyWhoa']/img").is_displayed()
			print browser.find_element_by_xpath("//p[@id='pyWhoa']/img").is_displayed()

		def tearDown(self):
			self.driver.close()

if __name__ == '__main__':
	unittest.main()