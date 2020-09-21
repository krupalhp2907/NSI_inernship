import os
import time
from os import path
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# argument 1 location for webdriver
# argument 2 location for webdriver
try:
    PATH = sys.argv[1]
except:
    PATH = "C:\\Program Files (x86)\\chromedriver.exe"

try:
    INPUT = sys.argv[2]
except:
    INPUT = path.join(os.getcwd(), 'Addition', 'public', 'index.html')

if not path.exists(INPUT):
    print("No such input file exists {}".format(INPUT))
    exit(1)

if not path.exists(INPUT):
    print("Web driver location incorrect {}".format(INPUT))
    exit(1)

NUMBER1_TAG = "number-1"
NUMBER2_TAG = "number-2"
ADD_TAG = "add"
RESULT_TAG = "result"

test_case = [[1, 3], [4, 3], [9, 10], [14, 19], [2423321, 3423432432]]

# Chrome drive headless mode donot use gpu graphics gui buffer resource
driver = webdriver.Chrome(PATH)
driver.get(INPUT)

total_test_cases = test_case.__len__()
passed_tests = 0

for i, test in enumerate(test_case):

    # Initialise state machine for NUMBER1_TAG
    num1Tag = driver.find_element_by_id(NUMBER1_TAG)
    num1Tag.clear()
    num1Tag.send_keys(str(test[0]))
    # END

    # Initialise state machine for NUMBER2_TAG
    num2Tag = driver.find_element_by_id(NUMBER2_TAG)
    num2Tag.clear()
    num2Tag.send_keys(str(test[1]))
    # END

    # Initialise state machine for ADD_TAG
    addTag = driver.find_element_by_name(ADD_TAG)
    addTag.click()
    # END

    # Initialise state machine for RESULT_TAG
    resultTag = driver.find_element_by_id(RESULT_TAG)
    result = resultTag.text

    if result == str(test[0] + test[1]):
        print("Test Case Passed", i, "[", test[0], "+", test[1], "]")
        passed_tests += 1
    else:
        break


if total_test_cases == passed_tests:
    print("All test case passed")
else:
    print(passed_tests, "passed")


driver.quit()
