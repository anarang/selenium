#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time, os, argparse, textwrap
from time import strftime
from ConfigParser import ConfigParser
from lib.HTMLTestRunner import HTMLTestRunner
from lib.report_description import description
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
			print your_name
			your_name = your_name.split(' ')[1]
			self.assertEqual("Zara",your_name,"Your name is not displayed correctly")

			browser.find_element_by_id("gotoList").click()
			browser.find_element_by_id("showList").click()
			frameworks = ["Hello","Hola", "Konnichiwa", "Bonjour"]
			list_elements = browser.find_elements_by_class_name("list")
			print "\nList of elements:"
			for ele in list_elements:
				print ele.text
				self.assertIn(ele.text, frameworks, "Desired elements not present in list")

			#How to use find_element_by_id for verification of the list items:
			# p =  browser.find_element_by_id("pyList")
			# frameworks = ["Django","Flask"]
			# for f in frameworks:
			# 	self.assertIn(f, p.text.split("\n"), "Desired elements not present in list")

		#How to skip any test -> @unittest.skip("demonstrating skipping")
		def test_picture_presence(self):
			whoa_url = self.base_url + "/whoa.html"
			browser.get(whoa_url)
			browser.find_element_by_id("showWhoa").click()
			browser.find_element_by_xpath("//p[@id='pyWhoa']/img").is_displayed()
			print browser.find_element_by_xpath("//p[@id='pyWhoa']/img").is_displayed()
			print "The image is present on the webpage"

		def tearDown(self):
			browser.close()

image_verification = unittest.TestSuite()
image_verification.addTest(TestSample('test_picture_presence'))

list_verification = unittest.TestSuite()
list_verification.addTest(TestSample('test_list_verification'))

all_tests = unittest.TestSuite([list_verification, image_verification])
        
parser = argparse.ArgumentParser(
    prog='main',
    version='PyCon workshop 1.0',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description = textwrap.dedent('''\
         Sample test cases for list_verification and image_verification
         Options: list_verification, image_verification
         '''),
    add_help = True)

group = parser.add_mutually_exclusive_group(required=False)
group.add_argument('-t','--testcase',metavar='',help= "Execute individual Scripts based on the options mentioned above", choices=['list_verification','image_verification'])
group.add_argument('-a','--all',action='store_true', help= "Run all the test scripts simultaneously")
suite = parser.parse_args()

if suite.all:
    suite.all='all_tests'
    print " Running all test cases as a suite"
    TESTCASE = suite.all
elif suite.testcase:
    print("Running %s test case "%suite.testcase)
    TESTCASE= suite.testcase
else:
    print("Please refer help")
    parser.print_version()
    parser.print_help()
    sys.exit(1)

report_format = strftime("%Y%m%d%H%M")       
reports_path = config.get("set_reports_path",'report_folder')
if not os.path.exists(reports_path):
    os.makedirs(reports_path)
outfile = open(os.path.join(reports_path,"report_%s_%s.html" % (TESTCASE, report_format)), 'w')

runner = HTMLTestRunner(stream= outfile, title='Test Report',description=description[TESTCASE])

try:
    if __name__ == "__main__":
        runner.run(eval(TESTCASE))
except KeyboardInterrupt:
    print("\nKeyboard Interrupt! No reports generated.")