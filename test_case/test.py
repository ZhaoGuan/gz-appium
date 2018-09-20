# -*- coding: utf-8 -*-
# __author__ = 'gz'


import os
import time
import unittest
import requests
from appium import webdriver
from golable_function.HTMLTestRunner import HTMLTestRunner
from golable_function.appium_set import AppiumConfig
from golable_function.extend import Appium_Extend
from golable_function.basefunction import BaseFunction
from golable_function.keyboard_function import Keyboard_Operation
from appium.webdriver.common.touch_action import TouchAction
from golable_function.Golable_function import report
from golable_function.kika_keyboard_function import Kika_Function

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
        # desired_caps['deviceName'] = DEVICE_CONFIG
        # desired_caps['udid'] = DEVICE_CONFIG
        desired_caps['deviceName'] = self.device
        desired_caps['udid'] = self.device
        # desired_caps['appPackage'] = 'com.tencent.mm'
        # desired_caps['appActivity'] = 'com.tencent.mm.ui.LauncherUI'
        desired_caps['appPackage'] = 'yuside.cn.numbersonly'
        desired_caps['appActivity'] = 'yuside.cn.numbersonly.MainActivity'
        # desired_caps['appPackage'] = 'com.emoji.ikeyboard'
        # desired_caps['appActivity'] = 'com.qisi.ikeyboarduirestruct.NavigationActivity'
        # 隐藏键盘
        # desired_caps['resetKeyboard'] = 'True'
        # 使用appium键盘
        # desired_caps['unicodeKeyboard'] = 'True'

        self.d = webdriver.Remote('http://%s:%s/wd/hub' % (self.APPIUM_CONFIG[0], self.APPIUM_CONFIG[1]), desired_caps)
        # self.d = webdriver.Remote('http://%s:%s/wd/hub' % ('127.0.0.1', '4711'), desired_caps)
        self.extend = Appium_Extend(self.d)
        self.BF = BaseFunction(self, self.d)
        self.kika = Kika_Function(self, self.d)
        time.sleep(5)
        # self.d.install_app()


    def tearDown(self):
        print('Test end')
        self.d.quit()

    def precast_condition(self):
        # self.d.start_activity('com.emoji.ikeyboard', 'com.android.inputmethod.latin.setup.SetupWizard2Activity')
        # time.sleep(3)
        self.kika.precast_condition('com.emoji.ikeyboard',
                                    '/Users/xm/Downloads/app-ikeyboard-96601-release-news_refactor.apk',
                                    'com.android.inputmethod.latin.setup.SetupWizard2Activity')

    def keyboard(self):
        top_y = self.BF.keyboard_get_ready('com.emoji.ikeyboard/com.android.inputmethod.latin.LatinIME', 'class',
                                           'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.d, top_y)
        time.sleep(5)
        self.BF.click('xpath', '//*[@index="3"]')
        # self.BF.click('name', '01-textAutoComplete')
        # time.sleep(2)
        # keyboard.send_input('system', number=True, select=True)
        time.sleep(2)
        # keyboard.sliding_input('about', number=True)
        # keyboard.main_menu_click('clipboard')
        keyboard.send_input('emoji', number=True, select=True)
        # time.sleep(1)
        # keyboard.send_input('sticker', keyboard_type='emoji', number=True, select=True)
        keyboard.send_input('emoji', keyboard_type='emoji', number=True, select=True)
        # keyboard.send_input('emoticon', keyboard_type='emoji', number=True, select=True)
        # keyboard.select_emoji_class('emoji', 4)
        # keyboard.select_emoji('emoji', 10, 2)
        # keyboard.select_emoji('emoticon', 10, 2)
        # text1 = self.BF.attribute_name('classes', 'android.widget.EditText[3]')
        # print(text1)
        # text = self.BF.attribute_name('classes', 'android.widget.EditText[3]', text1)
        # keyboard.checkpoint('test', 0, top_y, 720, 400, 'test1')
        keyboard.select_emoji('emoji', 3, 2)
        self.BF.checkpoint('test2', 'classes', 'android.widget.EditText[3]', 'EditText[3]')
        # print(text)
        # keyboard.send_input('delete', keyboard_type='emoji', number=True, select=True)
        time.sleep(5)
        # keyboard.send_input('asdfghjkl',number=True, select=True)
        # keyboard.send_input('qwertyuiopasdfghjklzxcvbnm', select=True)
        # keyboard.send_input('number')
        # keyboard.pop_select(')', '}', keyboard_type='normal_number', select=True)
        # text = self.BF.attribute_name('xpath', '//*[@index="3"]', 'about')
        # keyboard.select_select_key('left')
        # keyboard.select_select_key('left')
        # text = self.BF.attribute_name('xpath', '//*[@index="3"]', '1234567890')
        # self.BF.check_assertTrue(text, 'fail')
        # time.sleep(5)

    def theme(self):
        self.kika.app_theme()

    def settings(self):
        self.kika.app_settings()

    def test(self):
        top_y = self.BF.keyboard_get_ready('com.emoji.ikeyboard/com.android.inputmethod.latin.LatinIME', 'class',
                                           'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.d, top_y)
        # keyboard.send_input('system')
        # location = keyboard.main_menu_select('settings')
        # location = keyboard.main_menu_select('theme')
        # keyboard.get_keyboard_picture(location['x'], location['y'], location['width'], location['height'],'theme')
        self.BF.click('xpath', '//*[@index="1"]')
        keyboard.send_input('emoji')
        time.sleep(5)


if __name__ == "__main__":
    # 编辑用例
    # suite = Suit()
    suite = unittest.TestSuite()
    # suite.addTest(Keyboard_Test('precast_condition'))
    # suite.addTest(Keyboard_Test('keyboard'))
    # suite.addTest(Keyboard_Test('theme'))
    # suite.addTest(Keyboard_Test('settings'))
    suite.addTest(Keyboard_Test('test', device=DEVICE_CONFIG))
    # 执行用例
    runner = unittest.TextTestRunner()
    # filename = '%s' % report('gz')
    # fp = open(filename, 'wb')
    # runner = HTMLTestRunner(stream=fp, title='自动化测试报告', description='自动化测试报告')
    runner.run(suite)
