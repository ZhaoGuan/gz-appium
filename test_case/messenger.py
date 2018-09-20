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
from golable_function.image_recognition import ocr_text
from golable_function.messager_function import Messager_Function

appium_config = AppiumConfig()
udid = appium_config.get_device_udid()
appium = appium_config.get_appium_set()
DEVICE_CONFIG = udid[0]
APPIUM_CONFIG = appium[0]


# 因为使用Messenger为载体所以其中选择发送对象需要根据运行的手机做配置
# 脚本维护的时候也要将messenger对应环境准备好(各种权限的允许)
class Messenger(unittest.TestCase):
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
        desired_caps['appPackage'] = 'com.facebook.orca'
        desired_caps['appActivity'] = '.auth.StartScreenActivity'
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
        self.M = Messager_Function(self, self.d, DEVICE_CONFIG)
        self.BF.keyboard_select('com.qisiemoji.inputmethod/com.android.inputmethod.latin.LatinIME')
        time.sleep(5)

    def tearDown(self):
        print('Test end')
        self.d.quit()

    def precast_condition(self):
        # self.d.start_activity('com.emoji.ikeyboard', 'com.android.inputmethod.latin.setup.SetupWizard2Activity')
        # time.sleep(3)
        self.kika.precast_condition('com.qisiemoji.inputmethod',
                                    '/Users/xm/Downloads/app-ikeyboard-96601-release-news_refactor.apk')

    def en_input(self):
        top_y = self.M.select_user('com.qisiemoji.inputmethod/com.android.inputmethod.latin.LatinIME')
        keyboard = Keyboard_Operation(self.d, top_y)
        keyboard.send_input('copy')
        keyboard.send_input(' ')
        copy = self.BF.attribute_name('id', 'com.facebook.orca:id/text_input_bar', 'Copy ')
        self.BF.check_assertTrue(copy, '上屏内容错误')
        self.BF.check_find_element('id', 'com.facebook.orca:id/text_input_bar').clear()
        keyboard.sliding_input('about')
        # 这个滑动输入的检查点需要重新明确
        # about = self.BF.attribute_name('id', 'com.facebook.orca:id/text_input_bar', 'About')
        # self.BF.check_assertTrue(about, '上屏内容错误')
        self.BF.check_find_element('id', 'com.facebook.orca:id/text_input_bar').clear()
        keyboard.send_input('emoji')
        Messenger_emoji = self.BF.element_picture('id', 'com.facebook.orca:id/text_input_bar', 'Messenger_emoji')
        keyboard.send_input('emoji', 'emoji')
        keyboard.select_emoji('emoji', 1, 3)
        sendout = self.BF.attribute_name('id', 'com.facebook.orca:id/text_input_bar', '😂')
        self.BF.check_assertTrue(sendout, '表情选择错误')
        emoji = self.BF.cintrast_element_picture('id', 'com.facebook.orca:id/text_input_bar', Messenger_emoji)
        self.BF.check_assertFalse(emoji, '选择的emoji未上屏')
        # 检查点表格'Messenger_emoji'
        self.BF.checkpoint('Messenger_emoji', 'id', 'com.facebook.orca:id/text_input_bar', 'Messenger_emoji')
        self.BF.check_find_element('id', 'com.facebook.orca:id/text_input_bar').clear()
        keyboard.send_input('emoji')
        keyboard.send_input('sticker', 'emoji')
        keyboard.select_emoji('sticker', 1, 2)
        time.sleep(5)
        # self.BF.click('name', '确定')
        self.BF.checkpoint('Messenger_sticker', 'id', 'com.facebook.orca:id/message_container', 'Messenger_sticker')
        keyboard.send_input('gif', 'emoji')
        time.sleep(10)
        keyboard.select_emoji('gif', 1, 2)
        time.sleep(5)
        # self.BF.click('name', '确定')
        self.BF.checkpoint('Messenger_gif', 'id', 'com.facebook.orca:id/message_container', 'Messenger_gif')
        keyboard.send_input('emoticon', 'emoji')
        keyboard.select_emoji('gif', 1, 2)
        emoticon = self.BF.attribute_name('id', 'com.facebook.orca:id/text_input_bar', '(^～^)')
        self.BF.check_assertTrue(emoticon, 'emoticon选择错误')
        self.BF.checkpoint('Messenger_emoticon', 'id', 'com.facebook.orca:id/text_input_bar', 'Messenger_emoticon')

    def es_input(self):
        top_y = self.M.select_user('com.qisiemoji.inputmethod/com.android.inputmethod.latin.LatinIME')
        keyboard = Keyboard_Operation(self.d, top_y)
        # 切换输入法至西班牙语
        while True:
            location = keyboard.keyboard_reader(' ')
            orc = keyboard.orc_location_text(location['x'], location['y'], location['width'], location['height'])
            print(orc)
            if 'Es' in orc:
                break
            else:
                keyboard.swip_location(location['x'], location['y'], location['width'], location['height'])
        keyboard.send_input('espa')
        orc_select = keyboard.orc_location_text(0, top_y, keyboard.phone_width, 40 * keyboard.density()['density'],
                                                set_lang='epo')
        # print(orc_select)
        if 'Espaĥol' in orc_select:
            orc_result = True
        else:
            orc_result = False
        self.BF.check_assertTrue(orc_result, '没有纠正')

    def por_input(self):
        top_y = self.M.select_user('com.qisiemoji.inputmethod/com.android.inputmethod.latin.LatinIME')
        keyboard = Keyboard_Operation(self.d, top_y)
        # 切换输入法至葡萄牙语
        while True:
            location = keyboard.keyboard_reader(' ')
            orc = keyboard.orc_location(location['x'], location['y'], location['width'], location['height'])
            print(orc)
            if 'Po' in orc:
                break
            else:
                keyboard.swip_location(location['x'], location['y'], location['width'], location['height'])
        keyboard.send_input('portug')
        orc_select = keyboard.orc_location(0, top_y, keyboard.phone_width, 40 * keyboard.density()['density'],
                                           set_lang='por')
        print(orc_select)
        if 'Português' in orc_select:
            orc_result = True
        else:
            orc_result = False
        self.BF.check_assertTrue(orc_result, '没有纠正')


if __name__ == "__main__":
    # 编辑用例
    # suite = Suit()
    suite = unittest.TestSuite()
    # suite.addTest(Messenger('precast_condition'))
    suite.addTest(Messenger('en_input'))
    # suite.addTest(Messenger('es_input'))
    # suite.addTest(Messenger('por_input'))
    # 执行用例
    runner = unittest.TextTestRunner()
    # filename = '%s' % report('gz')
    # fp = open(filename, 'wb')
    # runner = HTMLTestRunner(stream=fp, title='自动化测试报告', description='自动化测试报告')
    runner.run(suite)
