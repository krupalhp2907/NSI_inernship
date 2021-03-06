import math
import os
import random
import time
from enum import Enum
from os import path
from queue import PriorityQueue

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import util

# Opions for less resource req
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Required

# Setup Chrome Driver
# argument 1 location for webdriver
# argument 2 location for webdriver
try:
    PATH = sys.argv[1]
except:
    PATH = "C:\\Program Files (x86)\\chromedriver.exe"

try:
    INPUT = sys.argv[2]
except:
    INPUT = path.join(os.getcwd(), 'Hangman', 'public', 'index.html')

if not path.exists(INPUT):
    print("No such input file exists {}".format(INPUT))
    exit(1)

if not path.exists(INPUT):
    print("Web driver location incorrect {}".format(INPUT))
    exit(1)


driver = webdriver.Chrome(PATH, options=options)
driver.get(INPUT)

# Tags that will be used by tester
BODY = 'body'
# Classes that will be used by tester
WRONG_LETTER = 'wrong-letter'
LETTERS = 'letter'
FIGURE_PART = 'figure-part'
# IDs that will be used by tester
PLAY_BTN = "play-button"
GAME_STATUS = "game_status"

# Errors Message
TAGS_MISSING_MESSAGE = "{} has been missing. Check documentation for more details."
TEST_CASE_FAILED_MESSAGE = "Test case for input failed. given input ==> '{}' <== | wrong letters ==> '{}' <== | correct letters ==> '{}' <==. Because ==> {}"


# Make sure Test Must have win or loose output
# ['application', 'programming', 'interface', 'wizard', 'frizar']
tests = [
    {
        "test_input": "application",
        "test_output": "win",
        "hangman_level": 0,
        "worng_letters": "",
        "wright_letters": "application"
    },
    {
        "test_input": "zeqvxwuprogramming",
        "test_output": "lose",
        "hangman_level": 6,
        "worng_letters": "zeqvxwu",
        "wright_letters": ""
    },
    {
        "test_input": "qlghinterface",
        "test_output": "win",
        "hangman_level": 4,
        "worng_letters": "qlgh",
        "wright_letters": "interface"
    }
]

# Point class


class Point:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def distance(self, p):
        return math.sqrt(abs(self.x - p.x)**2 + abs(self.y - p.y)**2)

    def cmp_x(self, p, epoch=.5):
        return util.compare(self.x, p, epoch)

    def cmp_y(self, p, epoch=.5):
        return util.compare(self.y, p, epoch)

    def __str__(self):
        return "[{0}, {1}]".format(self.x, self.y)

    def __eq__(self, other):
        ((self.x, self.y) == (other.x, other.y))

    def __ne__(self, other):
        return ((self.x, self.y) != (other.x, other.y))

    def __lt__(self, other):
        return ((self.x, self.y) < (other.x, other.y))

    def __le__(self, other):
        return ((self.x, self.y) <= (other.x, other.y))

    def __gt__(self, other):
        return ((self.x, self.y) > (other.x, other.y))

    def __ge__(self, other):
        return ((self.x, self.y) >= (other.x, other.y))

# Element


class FigureElement:
    def __init__(self, element):
        self.element = element
        self.tag_name = self.element.tag_name

        self.p1, self.p2, self.r, self.slope = None, None, None, None

        try:
            if self.tag_name == "circle":
                self.p1 = Point(self.element.get_attribute("cx"),
                                self.element.get_attribute("cx"))
                self.r = self.element.get_attribute("r")
            elif self.tag_name == "line":
                self.p1 = Point(self.element.get_attribute("x1"),
                                self.element.get_attribute("y1"))
                self.p2 = Point(self.element.get_attribute("x2"),
                                self.element.get_attribute("y2"))
                try:
                    self.slope = float(
                        (self.p2.y-self.p1.y)/(self.p2.x-self.p1.x))
                except ZeroDivisionError:
                    self.slope = None
        except:
            raise Exception("Given Element is not valid selenium Element")

    def __str__(self):
        if self.tag_name == "circle":
            return "<{} c = {} r = {} >".format(self.tag_name, self.p1.__str__(), self.r)
        return "<{} p1 = {} p2 = {} >".format(self.tag_name, self.p1.__str__(), self.p2.__str__())

# hangman element class takes usefull information from hangman


class HangmanElements:
    def __init__(self, *args, **kwargs):
        # All constructor code is wrapped in function so that
        # It would be easy when figure elements changes to update
        # our results using properties
        self.__segrigatte(*args, **kwargs)

    @property
    def elements(self):
        return self.__elements

    @elements.setter
    def elements(self, *args, **kwargs):
        self.__segrigatte(*args, **kwargs)

    @elements.getter
    def elements(self):
        return self.__elements

    def __segrigatte(self, elements):

        # Process Hangman HTML element
        self.__elements = []
        for ele in elements:
            self.__elements.append(FigureElement(ele))

        x_par, y_par, non_par, lines, circles = [], [], [], [], []

        # Loops to all html element for hangman figure
        for ele in self.__elements:

            # If element is lines
            if ele.tag_name == "line":

                # select lines parallel to y-axis
                if ele.slope == None:
                    y_par.append(ele)
                # select lines parallel to x-axis
                elif ele.slope == 0:
                    x_par.append(ele)
                # select lines that are non parallel to x-axis and y-axis
                else:
                    non_par.append(ele)

                lines.append(ele)

            elif ele.tag_name == "circle":
                # select circle probale head
                circles.append(ele)
            else:

                # hangman contain element more then lines and circle
                raise Exception(
                    "Hangman should be constructed using lines and circle svg element only.....")

        self.hang_axis = min(
            y_par, key=lambda param: param.p1.distance(param.p2))
        self.x_par, self.y_par, self.non_par, self.lines, self.circles = x_par, y_par, non_par, lines, circles

    def __str__(self):
        printable = []
        for ele in self.__elements:
            printable.append(ele.__str__())
        return printable.__str__()


# Function to check if two straight
# lines are orthogonal or not
def checkOrtho(p1, p2, p3, p4):

    x1, y1, x2, y2, x3, y3, x4, y4 = p1.x, p1.y, p2.x, p2.y, p3.x, p3.y, p4.x, p4.y

    # Both lines have infinite slope
    if (x2 - x1 == 0 and x4 - x3 == 0):
        return False

    # Only line 1 has infinite slope
    elif (x2 - x1 == 0):
        m2 = (y4 - y3) / (x4 - x3)

        if (m2 == 0):
            return True
        else:
            return False

    # Only line 2 has infinite slope
    elif (x4 - x3 == 0):
        m1 = (y2 - y1) / (x2 - x1)

        if (m1 == 0):
            return True
        else:
            return False

    else:

        # Find slopes of the lines
        m1 = (y2 - y1) / (x2 - x1)
        m2 = (y4 - y3) / (x4 - x3)

        # Check if their product is -1
        if (m1 * m2 == -1):
            return True
        else:
            return False


# Test Actual alignmnent for hangman
# It is done by segrigatting hangman svg with certain strict and non strict parts
# that makes hangman a hangman
# hangman figure has 2 parts structure and hangman
# structure should always be present and must angled 90 deg
# returns what's the level of hangman
def test_hangman_figure(hangman, level):
    x_par, y_par, non_par = hangman.x_par, hangman.y_par, hangman.non_par
    # test for structure for hangman
    if not (2 <= len(x_par) <= 6) or not (2 <= len(y_par) <= 7) or not (0 <= len(non_par) <= 4):
        raise Exception(
            "These is problem is construction of Hangman. Hint :- Check Prallel Lines to x, y axis and non parallel lines")

    def head(hangman, ans):
        if len(hangman.circles) == 1:
            if hangman.circles[0].p1.x == hangman.hang_axis:
                print("Circle has been checked correctly....")
            return hangman, ans + 1
        return hangman, ans

    def torso(hangman, ans):
        if len(hangman.y_par) == 3:
            return hangman, ans + 1
        return hangman, ans

    def left_hand(hangman, ans):
        if len(hangman.non_par) >= 1:
            return hangman, ans + 1
        return hangman, ans

    def right_hand(hangman, ans):
        if len(hangman.non_par) >= 2:
            return hangman, ans + 1
        return hangman, ans

    def left_leg(hangman, ans):
        if len(hangman.non_par) >= 3:
            return hangman, ans + 1
        return hangman, ans

    def right_leg(hangman, ans):
        if len(hangman.non_par) >= 4:
            return hangman, ans + 1
        return hangman, ans

    body_parts_seq = [
        head,
        torso,
        left_hand,
        right_hand,
        left_leg,
        right_leg
    ]

    count = 0
    for body_part_checker_func in body_parts_seq:
        res = body_part_checker_func(hangman, count)
        if res[1] != count + 1:
            break
        count += 1

    if count == level:
        return

    raise Exception("There is an error in hangman body....." +
                    "  " + str(count) + "  " + str(level))

# check ingridients that forms hangman correct
# A complete Hangman should be formed by one arc and rest parallel and non parallel lines
# Counting number of lines and arcs is first level validation for hangman
# here level is parts of hangman that actually be visible


def test_hangman(level):

    figure_elements = get_elements(By.CLASS_NAME, FIGURE_PART)
    hangman = HangmanElements(figure_elements)

    # get head and lines
    circles, lines = len(hangman.circles), len(hangman.lines)
    try:
        # # This is more advanced testing tests actual structure for hangman
        # # Segrigates parallel non parallel lines
        # # Segrigates structure and hangman
        # # It checks the angle between them
        test_hangman_figure(hangman, level)
    except:
        return False

    # Given test case hangman level
    # Given number of wrong letters we can segrigatte number of lines and arcs
    # It checks the above
    # sturcture is formed by atleast 4 lines hence first condition
    # if hangman has level < 7 then level == lines + circles - 4
    # if hangman has level == 7 level == lines + circles - 3
    if (lines + circles >= 4) and (level == lines + circles - 4):
        return True

    return False


# This function will control how scripts exits when code tested successfully
# closing web driver
# Clsoing all existing subprocess we created
def exit_script():
    driver.quit()
    exit(0)


def get_elements(by, name, err_message=""):
    if err_message == "":
        err_message = TAGS_MISSING_MESSAGE.format(name)
    try:
        temp = driver.find_elements(by, name)
    except:
        print("Tester Bug....")
        exit_script()

    # because classes are non unique
    if by != By.CLASS_NAME and temp == []:
        print(err_message)
        exit_script()
    return temp


# Picks the driver
body_element = get_elements(By.TAG_NAME, BODY)[0]

# play btn for restarting game
playBtn = get_elements(By.ID, PLAY_BTN)[0]


total_test_cases = len(tests)
count = 0
for index, test in enumerate(tests):
    test_input, test_output, hangman_level, worng_letters, wright_letters = test['test_input'], test[
        'test_output'], test['hangman_level'], test['worng_letters'], test['wright_letters']

    # Give input to game
    for i, char in enumerate(test_input):
        body_element.send_keys(char)

    # html element where user typed correct letter
    user_letters_element = get_elements(By.CLASS_NAME, LETTERS)
    # html element for user types wrong letters
    user_typed_wrong_letter_element = get_elements(By.CLASS_NAME, WRONG_LETTER)

    # output by the one who takes assig it should a hidden tag id game_status for status in [playing, win, lose]
    test_case_output = get_elements(By.ID, GAME_STATUS)
    test_case_output = test_case_output[0].get_attribute("value")

    # actual wrong letters types by users
    user_typed_wrong_letter = []
    for ele in user_typed_wrong_letter_element:
        user_typed_wrong_letter.append(ele.text)

    # Actual user typed correct letter list
    user_letters = []
    for ele in user_letters_element:
        user_letters.append(ele.text)

    # Actual user typed correct letter string
    user_letters = "".join(user_letters)

    # Tests performend
    # 1 ==> expected output vs output by student
    # 2 ==> the section for user wrong section
    # 3 ==> the setion for user wright section

    if test_case_output == test_output:
        if sorted(user_typed_wrong_letter) == sorted(worng_letters):
            if wright_letters == user_letters:
                try:
                    if test_hangman(hangman_level):
                        print("Test Case {} passed".format(index))
                        count += 1
                    else:
                        print(TEST_CASE_FAILED_MESSAGE.format(
                            test_input, worng_letters, wright_letters, "Hangman construction"))
                        exit_script()
                except:
                    print(TEST_CASE_FAILED_MESSAGE.format(
                        test_input, worng_letters, wright_letters, "Hangman construction"))
                    exit_script()
            else:
                print(TEST_CASE_FAILED_MESSAGE.format(
                    test_input, worng_letters, wright_letters, "user typed correct letters"))
        else:
            print(TEST_CASE_FAILED_MESSAGE.format(test_input,
                                                  worng_letters, wright_letters, "user typed wrong letters"))
    else:
        print(TEST_CASE_FAILED_MESSAGE.format(test_input,
                                              worng_letters, wright_letters, "game status or check user typed correct letters"))

    try:
        playBtn.click()
    except:
        print(TEST_CASE_FAILED_MESSAGE.format(test_input,
                                              worng_letters, wright_letters, "There is some error in project. test case number " + str(index)))


print("{}/{} test cases passed".format(count, total_test_cases))

exit_script()
