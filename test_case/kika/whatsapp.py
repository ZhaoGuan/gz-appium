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
from golable_function.whatsapp_function import Whatsapp_Function
from golable_function.ik_keyboard_function import Ikey_Function

appium_config = AppiumConfig()
udid = appium_config.get_device_udid()
appium = appium_config.get_appium_set()
DEVICE_CONFIG = udid[0]
APPIUM_CONFIG = appium[0]


# 因为使用Messenger为载体所以其中选择发送对象需要根据运行的手机做配置
# 脚本维护的时候也要将messenger对应环境准备好(各种权限的允许)
class Whatsapp(unittest.TestCase):
    def __init__(self, methodName='runTest', device=DEVICE_CONFIG):
        unittest.TestCase.__init__(self, methodName)
        self.device = device
        self.APPIUM_CONFIG = appium_config.get_appium_set()[self.device]

    def setUp(self):
        print('Test start')
        desired_caps = {}
        desired_caps['automationName'] = "appium"  # Appium,UiAutomator2,XCUITest,YouiEngine
        desired_caps['platformName'] = 'Android'
        desired_caps['deviceName'] = DEVICE_CONFIG
        desired_caps['udid'] = DEVICE_CONFIG
        # desired_caps['appPackage'] = 'com.tencent.mm'
        # desired_caps['appActivity'] = 'com.tencent.mm.ui.LauncherUI'
        desired_caps['appPackage'] = 'com.whatsapp'
        desired_caps['appActivity'] = 'com.whatsapp.Main'
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
        self.W = Whatsapp_Function(self, self.d, DEVICE_CONFIG)
        time.sleep(5)

    def tearDown(self):
        print('Test end')
        self.d.quit()

    def precast_condition(self):
        # self.d.start_activity('com.emoji.ikeyboard', 'com.android.inputmethod.latin.setup.SetupWizard2Activity')
        # time.sleep(3)
        self.kika.precast_condition('com.emoji.ikeyboard',
                                    '/Users/xm/Downloads/app-kika-197001-release-0cb416d.apk',
                                    'com.emoji.ikeyboard/com.android.inputmethod.latin.LatinIME')

    def sticker2(self):
        top_y = self.W.select_user('com.emoji.ikeyboard/com.android.inputmethod.latin.LatinIME')
        keyboard = Keyboard_Operation(self.d, top_y)
        keyboard.send_input('test', 'normal')
        keyboard.send_input(' ', 'normal')
        keyboard.send_input(' ', 'normal')
        send = self.BF.attribute_name('id', 'com.whatsapp:id/entry', 'Test. ')
        self.BF.check_assertTrue(send, '输入内容错误')
        # keyboard.get_keyboard_picture(location['x'], location['y'], location['width'], location['height'], 'test')
        keyboard.send_input('stop', 'normal')
        keyboard.sticker2_click('sitcker2', 3, 2)
        # self.BF.checkpoint('sticker2', 'id', 'com.whatsapp:id/color_picker_container', 'sticker2')
        sticker2 = self.BF.existence('id', 'com.whatsapp:id/color_picker_container')
        self.BF.check_assertTrue(sticker2, 'sticker2选择失败')
        self.BF.click('id', 'com.whatsapp:id/send')
        time.sleep(5)
        self.BF.result_picture('sticker2')

    def layout(self):
        top_y = self.W.select_user('com.emoji.ikeyboard/com.android.inputmethod.latin.LatinIME')
        keyboard = Keyboard_Operation(self.d, top_y)

    def theme(self):
        self.kika.app_theme()

    def settings(self):
        self.kika.app_settings()

    def test(self):
        top_y = self.BF.keyboard_get_ready('com.emoji.ikeyboard/com.android.inputmethod.latin.LatinIME', 'class',
                                           'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.d, top_y)
        keyboard.send_input('system')
        location = keyboard.main_menu_select('settings')
        # location = keyboard.main_menu_select('theme')
        keyboard.get_keyboard_picture(location['x'], location['y'], location['width'], location['height'], 'theme')


if __name__ == "__main__":
    # 编辑用例
    # suite = Suit()
    suite = unittest.TestSuite()
    suite.addTest(Whatsapp('precast_condition'))
    # suite.addTest(Whatsapp('sticker2'))
    # suite.addTest(Whatsapp('layout'))
    # suite.addTest(Keyboard_Test('theme'))
    # suite.addTest(Keyboard_Test('settings'))
    # suite.addTest(Messenger('test'))
    # 执行用例
    runner = unittest.TextTestRunner()
    # filename = '%s' % report('gz')
    # fp = open(filename, 'wb')
    # runner = HTMLTestRunner(stream=fp, title='自动化测试报告', description='自动化测试报告')
    runner.run(suite)
