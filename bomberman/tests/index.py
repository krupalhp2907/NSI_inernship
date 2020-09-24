import math
import os
import random
import time
from enum import Enum
from os import path
from queue import PriorityQueue
import getpass

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.chrome.options import Options

# Opions for less resource req
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Required

try:
    INPUT = sys.argv[2]
except:
    INPUT = "/home/pk/dev/NSI/projects/bomberman/public/index.html"


if not path.exists(INPUT):
    print("No such input file exists {}".format(INPUT))
    exit(1)

print(path.join(os.getcwd(), '../', 'vendor', 'chromedriver'))
driver = webdriver.Chrome(
    "/home/pk/dev/NSI/projects/vendor/chromedriver", options=options)
driver.get('file://' + INPUT)

test_cases = [
    {
        "bomb_locations": [[0, 1], [0, 2], [0, 3], [1, 3], [3, 5], [7, 7], [5, 3], [3, 6], [5, 1], [1, 3]],
        "inputs": [[4, 3], [6, 3], [4, 2], [3, 5]],
        "output": "lose",
        "total_point": 3
    }
]


# Tags

# classes
CELL = "cell"
CELL_LOCATION = "{}_{}"

# IDS
GAME_STATUS = "game-status"  # should be in ['playing', 'win', 'lose']
PLAY_BTN = "play-again"


# Erros messages
TAGS_MISSING_MESSAGE = "{} has been missing. Check documentation for more details."
NOT_CLICKABLE = "{} not clickable"

# Colors
GREEN = ['rgb(73, 188, 7)', 'rgba(73, 188, 7, 1)']
RED = ['rgb(228, 70, 70)', 'rgba(228, 70, 70, 1)']


def exit_script(msg="", code=0):
    print(msg)
    driver.quit()
    exit(code)


def get_elements(by, name, err_message=""):
    if err_message == "":
        err_message = TAGS_MISSING_MESSAGE.format(name)

    temp = driver.find_elements(by, name)

    # because classes are non unique
    if by != By.CLASS_NAME and temp == []:
        print(err_message)
        exit_script()
    return temp


def test_grid():
    for i in range(9):
        for j in range(9):
            get_elements(By.ID, CELL_LOCATION.format(i, j))


def gen_hash(bomb_locations):
    dic = {}
    for loc in bomb_locations:
        key = CELL_LOCATION.format(loc[0], loc[1])
        dic[key] = True
    return dic


def identifier_to_num(cell_identifier):
    i, j = list(map(int, cell_identifier.split("_")))
    return i*9 + j


def check_clicked_on_bomb(bomb_locations):

    for bomb in bomb_locations:
        cell_identifier = CELL_LOCATION.format(bomb[0], bomb[1])
        cell_element = get_elements(By.ID, cell_identifier)[0]
        if cell_element.value_of_css_property("background-color") not in RED:
            return False
        # return False
    return True


def check_clicked_safe(cell_element, cell_number):
    if cell_element.text == str(cell_number):
        if cell_element.value_of_css_property("background-color") in GREEN:
            return True
        else:
            return False
    else:
        return False


def main():
    total_test_cases = len(test_cases)

    count = 0
    for test in test_cases:

        # It will exit script if something went wrong
        test_grid()

        bomb_locations, inputs, output, total_point = test[
            "bomb_locations"], test["inputs"], test["output"], test["total_point"]

        bomb_locations_hash = gen_hash(bomb_locations)

        for i, inp in enumerate(inputs):
            cell_identifier = CELL_LOCATION.format(inp[0], inp[1])
            cell_element = get_elements(By.ID, cell_identifier)[0]

            try:
                cell_element.click()
            except:
                exit_script(NOT_CLICKABLE.format(cell_identifier))

            if cell_identifier in bomb_locations_hash:
                # check changes in application
                out_ = check_clicked_on_bomb(bomb_locations)
            else:
                # check changes in application
                out_ = check_clicked_safe(cell_element, i)

            if not out_:
                print("Test case failed:- ", str(count))
                break
        else:
            print("Test case passed:- ", str(count))
            count += 1

    exit_script("{}/{} test cases passed".format(count, total_test_cases))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        exit_script("Server Error " + e)
