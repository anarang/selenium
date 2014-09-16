#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time, os
from time import strftime
from ConfigParser import ConfigParser
from lib.HTMLTestRunner import HTMLTestRunner
conf_file = open('config/config.conf')
config = ConfigParser()
config.readfp(conf_file)


class TestSample(unittest.TestCase):
		def setUp(self):
			self.driver = webdriver.Firefox()
			#self.driver = webdriver.PhantomJS()
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
			print my_name
			my_name = my_name.split(' ')[2]
			print my_name
			self.assertEqual("Ann",my_name,"Name not displayed correctly")
			
			browser.find_element_by_id("yourName").send_keys("Zara")
			browser.find_element_by_id("yourName").send_keys(Keys.RETURN)
			your_name = browser.find_element_by_id("yourName").text
			print your_name
			your_name = your_name.split(' ')[1]
			self.assertEqual("Zara",your_name,"Your name is not displayed correctly")

			browser.find_element_by_id("gotoList").click()
			browser.find_element_by_id("showList").click()
			frameworks = ["Django","Flask", "Pylons", "Pyramid"]
			list_elements = browser.find_elements_by_class_name("list")
			for ele in list_elements:
				print ele.text
				self.assertIn(ele.text, frameworks, "Desired elements not present in list")

			#How to use find_element_by_id for verification of the list items:
			# p =  browser.find_element_by_id("pyList")
			# frameworks = ["Django","Flask"]
			# for f in frameworks:
			# 	self.assertIn(f, p.text.split("\n"), "Desired elements not present in list")

		#How to skip any test -> @unittest.skip("demonstrating skipping")
		def test_image_presence(self):
			whoa_url = self.base_url + "/whoa.html"
			browser.get(whoa_url)
			browser.find_element_by_id("showWhoa").click()
			browser.find_element_by_xpath("//p[@id='pyWhoa']/img").is_displayed()
			print browser.find_element_by_xpath("//p[@id='pyWhoa']/img").is_displayed()

		def tearDown(self):
			browser.close()

image_verification = unittest.TestSuite()
image_verification.addTest(TestSample('test_image_presence'))

list_verification = unittest.TestSuite()
list_verification.addTest(TestSample('test_list_verification'))

all_tests = unittest.TestSuite([image_verification, list_verification])
        
report_format = strftime("%Y%m%d%H%M")       
reports_path = config.get("set_reports_path",'report_folder')
if not os.path.exists(reports_path):
    os.makedirs(reports_path)
outfile = open(os.path.join(reports_path,"report_%s.html" % (report_format)), 'w')

runner = HTMLTestRunner(stream= outfile, title='Test Report',description="Tests for Sample Application")

try:
    if __name__ == "__main__":
        runner.run(all_tests)
except KeyboardInterrupt:
    print("\nKeyboard Interrupt! No reports generated.")