# -*- coding: utf-8 -*-
# __author__ = 'Gz'

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
from golable_function.ik_keyboard_function import Ikey_Function
from golable_function.image_recognition import ocr_text

appium_config = AppiumConfig()
udid = appium_config.get_device_udid()
appium = appium_config.get_appium_set()
DEVICE_CONFIG = udid[0]
APPIUM_CONFIG = appium[0]


# 因为使用Messenger为载体所以其中选择发送对象需要根据运行的手机做配置
# 脚本维护的时候也要将messenger对应环境准备好(各种权限的允许)
class InputApp(unittest.TestCase):
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
        # 超时时间设置
        desired_caps['newCommandTimeout'] = 180
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
        self.Ik = Ikey_Function(self, self.d)
        time.sleep(5)
        self.d.get_window_size()

    def input(self):
        top_y = self.BF.keyboard_get_ready('com.qisiemoji.inputmethod/com.android.inputmethod.latin.LatinIME', 'class',
                                           'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.d, top_y)
        default = keyboard.get_keyboard_picture(0, top_y, keyboard.phone_width, 40 * keyboard.density()['density'],
                                                'indian_default')
        self.BF.click('xpath', '//android.widget.EditText[@index="1"]')
        wrong = []
        with open('./vocab_hinglish', 'r') as word_list:
            for line in word_list:
                print(line)
                print(line.split('\n')[0])
                keyboard.send_input(line.split('\n')[0].lower(), number=True)
                keyboard.send_input(' ', number=True)
                same = keyboard.keyboard_same(0, top_y, keyboard.phone_width, 40 * keyboard.density()['density'],
                                              default, diff=2)
                print(same)
                key = self.BF.attribute_name('xpath', '//android.widget.EditText[@index="1"]')
                if line.split('\n')[0] in key:
                    key = True
                else:
                    key = False
                print(key)
                # self.BF.check_find_element('xpath', '//android.widget.EditText[@index="1"]').clear()
                count = 0
                while True:
                    keyboard.send_input('delete')
                    count += 1
                    if count > 8:
                        break
                if key is True and same is False:
                    pass
                else:
                    wrong.append(line.split('\n')[0])
                print(wrong)
        print(wrong)

    def input_io(self):
        top_y = self.BF.keyboard_get_ready('com.qisiemoji.inputmethod/com.android.inputmethod.latin.LatinIME', 'class',
                                           'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.d, top_y)
        # default = keyboard.get_keyboard_picture(0, top_y, keyboard.phone_width, 40 * keyboard.density()['density'],
        #                                         'indian_default')
        self.BF.click('xpath', '//android.widget.EditText[@index="1"]')
        wrong = []
        with open('./hinglish_hindi_pair', 'r') as word_list:
            for line in word_list:
                i = line.split('\t')[0].lower()
                o = line.split('\t')[1].split('\n')[0]
                # i = 'kya'
                # o = 'क्या'
                print(i, o)
                keyboard.send_input(i, number=True)
                # keyboard.send_input(' ', number=True)
                self.d.tap([(keyboard.phone_width / 4, top_y + 20 * keyboard.density()['density'])])
                # same = keyboard.orc_location_text(0, top_y, keyboard.phone_width, 40 * keyboard.density()['density'],
                #                                   set_lang='eng')
                same = self.BF.attribute_name('xpath', '//android.widget.EditText[@index="1"]')
                print(same)
                if o in same:
                    same = True
                else:
                    same = False
                # print(same)
                # key = self.BF.attribute_name('xpath', '//android.widget.EditText[@index="1"]')
                # if i in key:
                #     key = True
                # else:
                #     key = False
                # print(key)
                # self.BF.check_find_element('xpath', '//android.widget.EditText[@index="1"]').clear()
                count = 0
                while True:
                    keyboard.send_input('delete')
                    count += 1
                    if count > 8:
                        break
                if same is True:
                    pass
                else:
                    wrong.append(line.split('\n')[0])
                print(wrong)
        print(wrong)


if __name__ == "__main__":
    # 编辑用例
    # suite = Suit()
    suite = unittest.TestSuite()
    suite.addTest(InputApp('input'))
    # suite.addTest(InputApp('input_io'))
    # 执行用例
    runner = unittest.TextTestRunner()
    # filename = '%s' % report('gz')
    # fp = open(filename, 'wb')
    # runner = HTMLTestRunner(stream=fp, title='自动化测试报告', description='自动化测试报告')
    runner.run(suite)
