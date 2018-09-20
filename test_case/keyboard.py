# -*- coding: utf-8 -*-
# __author__ = 'Gz'


import os
import time
import unittest

from appium import webdriver
from golable_function.HTMLTestRunner import HTMLTestRunner
from golable_function.appium_set import AppiumConfig
from golable_function.extend import Appium_Extend
from golable_function.basefunction import BaseFunction
from golable_function.keyboard_function import Keyboard_Operation
from appium.webdriver.common.touch_action import TouchAction
from golable_function.Golable_function import report

appium_config = AppiumConfig()
udid = appium_config.get_device_udid()
appium = appium_config.get_appium_set()
DEVICE_CONFIG = udid[0]
APPIUM_CONFIG = appium[0]


class Keyboard_Test(unittest.TestCase):
    def __init__(self, methodName='runTest', device=DEVICE_CONFIG):
        unittest.TestCase.__init__(self, methodName)
        self.device = device
        self.APPIUM_CONFIG = appium_config.get_appium_set()[self.device]

    def setUp(self):
        print('Test start')
        desired_caps = {}
        desired_caps['automationName'] = "appium"  # Appium,UiAutomator2,XCUITest,YouiEngine
        desired_caps['platformName'] = 'Android'
        desired_caps['deviceName'] = self.device
        desired_caps['udid'] = self.device
        # desired_caps['appPackage'] = 'com.tencent.mm'
        # desired_caps['appActivity'] = 'com.tencent.mm.ui.LauncherUI'
        desired_caps['appPackage'] = 'yuside.cn.numbersonly'
        desired_caps['appActivity'] = 'yuside.cn.numbersonly.MainActivity'
        # 隐藏键盘
        # desired_caps['resetKeyboard'] = 'True'
        # 使用appium键盘
        # desired_caps['unicodeKeyboard'] = 'True'

        self.d = webdriver.Remote('http://%s:%s/wd/hub' % (self.APPIUM_CONFIG[0], self.APPIUM_CONFIG[1]), desired_caps)
        # self.d = webdriver.Remote('http://%s:%s/wd/hub' % ('127.0.0.1', '4711'), desired_caps)
        self.extend = Appium_Extend(self.d)
        self.BF = BaseFunction(self, self.d)
        time.sleep(5)

    def tearDown(self):
        print('Test end')
        self.d.quit()

    def eninput(self):
        top_y = self.BF.keyboard_get_ready('com.emoji.ikeyboard/com.android.inputmethod.latin.LatinIME', 'class',
                                           'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.d, top_y)
        # 用例内容
        self.BF.click('xpath', '//*[@index="3"]')
        # self.BF.click('name', '01-textAutoComplete')
        time.sleep(2)
        keyboard.send_input('cppy')
        keyboard.send_input(' ')
        text = self.BF.attribute_name('xpath', '//*[@index="3"]', 'copy ')
        self.BF.check_assertTrue(text, 'fail')
        # text = keyboard.select_word_check('copy')
        # self.BF.check_assertTrue(text, '需要的词没有在选词栏中')
        # select = \
        #     keyboard.ocr_location(0, top_y, int(self.d.get_window_size()['width']),
        #                           int(keyboard.density()['density']) * 40)[0]
        # print(select)
        # keyboard.location_click(select['x'], select['y'])
        # click = self.BF.attribute_name('id', 'yuside.cn.numbersonly:id/search_btn', 'copy')
        # self.BF.check_assertTrue(click, '选词上屏fail')
        # self.BF.result_picture('eninput1')
        # self.BF.check_find_element('id', 'yuside.cn.numbersonly:id/search_btn').clear()
        # keyboard.sliding_input('about')
        # sliding = self.BF.attribute_name('id', 'yuside.cn.numbersonly:id/search_btn', 'about')
        # self.BF.check_assertTrue(sliding, '滑动上屏fail')
        # self.BF.result_picture('eninput2')

    def emoji(self):
        top_y = self.BF.keyboard_get_ready('com.emoji.ikeyboard/com.android.inputmethod.latin.LatinIME', 'class',
                                           'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.d, top_y)
        self.BF.click('name', '02-search')
        search = self.BF.element_picture('id', 'yuside.cn.numbersonly:id/search_btn', 'search')
        keyboard.send_input('emoji')
        time.sleep(2)
        keyboard.send_input('emoji', keyboard_type='emoji')
        keyboard.select_emoji_class('emoji', 3)
        keyboard.select_emoji('emoji', 3, 5)
        emoji = self.BF.cintrast_element_picture('id', 'yuside.cn.numbersonly:id/search_btn', search)
        self.BF.check_assertFalse(emoji, 'emoji未上屏')
        self.BF.result_picture('emoji')

    def emoji_style(self):
        top_y = self.BF.keyboard_get_ready('com.emoji.ikeyboard/com.android.inputmethod.latin.LatinIME', 'class',
                                           'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.d, top_y)
        keyboard.send_input('emoji')
        keyboard.send_input('emoji', keyboard_type='emoji')
        height = (keyboard.phone_height - top_y)
        width = keyboard.phone_width
        load = keyboard.get_keyboard_picture(0, top_y, width, height - 40 * int(keyboard.density()['density']), 'emojy')
        keyboard.send_input('normal_key', keyboard_type='emoji')
        keyboard.send_input('system')
        keyboard.main_menu_click('style')
        keyboard.select_theme(1, 2)
        time.sleep(5)
        keyboard.send_input('emoji')
        same = keyboard.keyboard_same(0, top_y, width, height - 40 * int(keyboard.density()['density']), load)
        self.BF.check_assertFalse(same, '表情风格更换失败')
        self.BF.result_picture('emoji_style')

    def nubmer_decimal(self):
        top_y = self.BF.keyboard_get_ready('com.emoji.ikeyboard/com.android.inputmethod.latin.LatinIME', 'class',
                                           'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.d, top_y)
        self.BF.reach_element_click(200, 'name', '24-numberDecimal')
        keyboard.send_input('1234567890', keyboard_type='number_decimal')
        input = self.BF.attribute_name('xpath', '//*[@index="23"]', '1234567890')
        self.BF.check_assertTrue(input, '输入内容正确显示正确')
        # location = keyboard.keyboard_reader('1', keyboard_type='number_decimal')
        # keyboard.get_keyboard_picture(location['x'], location['y'], location['width'], location['height'], '1')
        # location = keyboard.keyboard_reader('2', keyboard_type='number_decimal')
        # keyboard.get_keyboard_picture(location['x'], location['y'], location['width'], location['height'], '2')
        # location = keyboard.keyboard_reader('3', keyboard_type='number_decimal')
        # keyboard.get_keyboard_picture(location['x'], location['y'], location['width'], location['height'], '3')
        # location = keyboard.keyboard_reader('-', keyboard_type='number_decimal')
        # keyboard.get_keyboard_picture(location['x'], location['y'], location['width'], location['height'], '-')
        # location = keyboard.keyboard_reader(' ', keyboard_type='number_decimal')
        # keyboard.get_keyboard_picture(location['x'], location['y'], location['width'], location['height'], 'space')
        self.BF.result_picture('nubmer_decimal')

    def number_password(self):
        top_y = self.BF.keyboard_get_ready('com.emoji.ikeyboard/com.android.inputmethod.latin.LatinIME', 'class',
                                           'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.d, top_y)
        self.BF.reach_element_click(200, 'xpath', '//*[@index="24"]')
        keyboard.send_input('1234567890', keyboard_type='number_password')
        # location = keyboard.keyboard_reader('1', keyboard_type='number_password')
        # keyboard.get_keyboard_picture(location['x'], location['y'], location['width'], location['height'], '1')
        # location = keyboard.keyboard_reader('2', keyboard_type='number_password')
        # keyboard.get_keyboard_picture(location['x'], location['y'], location['width'], location['height'], '2')
        # location = keyboard.keyboard_reader('3', keyboard_type='number_password')
        # keyboard.get_keyboard_picture(location['x'], location['y'], location['width'], location['height'], '3')
        self.BF.result_picture('number_passworf')

    def chang_theme(self):
        top_y = self.BF.keyboard_get_ready('com.emoji.ikeyboard/com.android.inputmethod.latin.LatinIME', 'class',
                                           'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.d, top_y)
        height = (keyboard.phone_height - top_y)
        width = keyboard.phone_width
        load = keyboard.get_keyboard_picture(0, top_y, width, height - 40 * int(keyboard.density()['density']),
                                             'keyboard')
        keyboard.send_input('system')
        keyboard.main_menu_click('theme')
        keyboard.select_theme(1, 2)
        # 判断是否回到了键盘主页
        text = keyboard.word_in_pic(0, top_y + int(keyboard.density()['density']) * 40, keyboard.phone_width, (
            int(keyboard.density()['app']) - top_y - int(keyboard.density()['density']) * 40) / 4, 'q')
        self.BF.check_assertTrue(text, '返回qwerty键盘失败，可能没有选择主题')
        time.sleep(5)
        same = keyboard.keyboard_same(0, top_y, width, height - 40 * int(keyboard.density()['density']), load)
        self.BF.check_assertFalse(same, '主题风格更换失败')
        self.BF.result_picture('emoji_style')

    def normal_number(self):
        top_y = self.BF.keyboard_get_ready('com.emoji.ikeyboard/com.android.inputmethod.latin.LatinIME', 'class',
                                           'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.d, top_y)
        self.BF.click('name', '02-search')
        # self.BF.click('name', '01-textAutoComplete')
        time.sleep(2)
        keyboard.send_input('number')
        keyboard.send_input('1234567890', keyboard_type='normal_number')
        # keyboard.send_input('qwertyuiopasdfghjklzxcvbnm')
        self.BF.result_picture('normal_number')

    def normal_symbol(self):
        top_y = self.BF.keyboard_get_ready('com.emoji.ikeyboard/com.android.inputmethod.latin.LatinIME', 'class',
                                           'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.d, top_y)
        self.BF.click('name', '02-search')
        # self.BF.click('name', '01-textAutoComplete')
        time.sleep(2)
        keyboard.send_input('number')
        keyboard.send_input('symbol', keyboard_type='normal_number')
        keyboard.send_input('•√Π÷×¶∆£¢€¥^°©®™℅', keyboard_type='normal_symbol')
        keyboard.send_input('number', keyboard_type='normal_symbol')
        # keyboard.send_input('qwertyuiopasdfghjklzxcvbnm')
        self.BF.result_picture('normal_symbol')


if __name__ == "__main__":
    # 编辑用例
    # suite = Suit()
    suite = unittest.TestSuite()
    suite.addTest(Keyboard_Test('eninput'))
    # suite.addTest(Keyboard_Test('emoji'))
    # suite.addTest(Keyboard_Test('emoji_style'))
    # suite.addTest(Keyboard_Test('nubmer_decimal'))
    # suite.addTest(Keyboard_Test('number_password'))
    # suite.addTest(Keyboard_Test('chang_theme'))
    # suite.addTest(Keyboard_Test('normal_number'))
    # suite.addTest(Keyboard_Test('normal_symbol'))
    # 执行用例
    runner = unittest.TextTestRunner()
    # filename = '%s' % report('gz')
    # fp = open(filename, 'wb')
    # runner = HTMLTestRunner(stream=fp, title='自动化测试报告', description='自动化测试报告')
    runner.run(suite)
