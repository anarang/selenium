## Sample test scripts

### Selenium with Python:

#### Pre-requisites:
<pre>
- Python 2.7
- Firefox browser
- Selenium Python bindings
</pre>

### Setup:
1. Python and Selenium setup:

<pre>
$ sudo yum install python       #Installs Python

$ sudo yum install pip-python   
$ pip-pyton install -U selenium     #Install Selenium Python bindings
</pre>

2.Configurations:
<pre>
$ mv config/config.conf.sample config/config.conf
# Replace www.example.com with a suitable URL where against which you want to run your tests

### Execution:
1. To run the test suite:

<pre>
$ python mytest.py --all
</pre>

2.To run individual test case:

<pre>
$ python mytest.py -t list_verification
$ python mytest.py -t image_verification
</pre>

3. HTML reports are generated and available in ./reports or at the user specified path as per the config.conf file.

4. Basic Selenium script outline is available in basic_str.py








