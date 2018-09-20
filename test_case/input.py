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


# APPIUM_CONFIG = appium[0]


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

    def tearDown(self):
        print('Test end')
        self.d.quit()

    def precast_condition(self):
        self.kika.precast_condition('com.emoji.ikeyboard',
                                    '/Users/xm/Downloads/app-ikeyboard-96601-release-news_refactor.apk',
                                    'com.qisiemoji.inputmethod/com.android.inputmethod.latin.LatinIME')

    def theme(self):
        top_y = self.BF.keyboard_get_ready('com.qisiemoji.inputmethod/com.android.inputmethod.latin.LatinIME', 'class',
                                           'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.d, top_y)
        k = keyboard.get_keyboard_picture(0, top_y, keyboard.phone_width, (keyboard.density()['app'] - top_y),
                                          'keyboard')
        keyboard.send_input('system')
        keyboard.main_menu_click('theme')
        keyboard.select_theme(2, 1)
        pic_text = keyboard.get_keyboard_picture(0, top_y, keyboard.phone_width, (keyboard.density()['app'] - top_y),
                                                 'keyboard_back')
        pic_text = keyboard.pic_text(pic_text)
        if 'q' in pic_text:
            pass
        else:
            assert 1 + 1 > 2, '没有回到键盘'
        k_s = keyboard.keyboard_same(0, top_y, keyboard.phone_width, (keyboard.density()['app'] - top_y), k)
        self.BF.check_assertFalse(k_s, '主题更换失败')
        # 回选到默认主题
        keyboard.send_input('system')
        keyboard.main_menu_click('theme')
        keyboard.select_theme(1, 2)
        pic_text = keyboard.get_keyboard_picture(0, top_y, keyboard.phone_width, (keyboard.density()['app'] - top_y),
                                                 'keyboard_back')
        pic_text = keyboard.pic_text(pic_text)
        if 'q' in pic_text:
            pass
        else:
            assert 1 + 1 > 2, '没有回到键盘'
        k_s = keyboard.keyboard_same(0, top_y, keyboard.phone_width, (keyboard.density()['app'] - top_y), k)
        self.BF.check_assertTrue(k_s, '主题更换失败')

    def old_new_app1(self):
        self.kika.old_new_app_custom_keyboard('com.qisiemoji.inputmethod',
                                              'com.qisiemoji.inputmethod/com.android.inputmethod.latin.LatinIME',
                                              '/Users/xm/Downloads/app-kika-188401-release-2a6f330.apk',
                                              '/Users/xm/Downloads/app-kika-190101-release-34a7aff.apk')

    def old_new_app2(self):
        run_result = []
        false_result = []
        for i in range(3, 12):
            # for i in range(5, 7):
            result = self.kika.old_new_app_theme(i, 'com.qisiemoji.inputmethod',
                                                 'com.qisiemoji.inputmethod/com.android.inputmethod.latin.LatinIME',
                                                 '/Users/xm/Downloads/app-kika-190101-release-34a7aff.apk',
                                                 '/Users/xm/Downloads/app-kika-190201-release-35ae3d4.apk')
            run_result.append(result)
        print(run_result)
        for g in range(0, len(run_result)):
            for f in run_result[g]:
                key = f
            if run_result[g][f] == False:
                false_result.append(key)
        if len(false_result) > 0:
            assert 1 + 1 > 2, '以下主题前后不一致%s' % str(false_result)

    def old_new_app3(self):
        run_result = []
        false_result = []
        for i in range(0, 5):
            result = self.kika.old_new_app_font(i, 'com.qisiemoji.inputmethod',
                                                'com.qisiemoji.inputmethod/com.android.inputmethod.latin.LatinIME',
                                                '/Users/xm/Downloads/app-kika-188401-release-2a6f330.apk',
                                                '/Users/xm/Downloads/app-kika-190201-release-35ae3d4.apk')
            run_result.append(result)
        print(run_result)
        for g in range(0, len(run_result)):
            for f in run_result[g]:
                key = f
            if run_result[g][f] == False:
                false_result.append(key)
        if len(false_result) > 0:
            assert 1 + 1 > 2, '以下字体前后不一致%s' % str(false_result)

    # 自定义键盘
    def change(self):
        self.kika.change_custom_keyboard()

    def settings(self):
        self.kika.app_settings()

    # 修改为第几个主题
    def theme_change(self):
        self.kika.change_theme(5)
        self.d.start_activity('yuside.cn.numbersonly', 'yuside.cn.numbersonly.MainActivity')
        # 键盘输入检查
        top_y = self.BF.keyboard_get_ready('com.qisiemoji.inputmethod/com.android.inputmethod.latin.LatinIME', 'class',
                                           'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.d, top_y)
        keyboard.send_input('qwertyuiopasdfghjklzxcvbnm')
        keyboard.send_input('shift')
        keyboard.send_input('g')
        s_input = self.BF.attribute_name('classes', 'android.widget.EditText[0]', 'qwertyuiopasdfghjklzxcvbnmG')
        self.BF.check_assertTrue(s_input, '键盘输入内容错误')

    # 随机下载主题并清除下载的主题
    def downloda_theme(self):
        self.kika.random_download_theme()
        self.d.start_activity('yuside.cn.numbersonly', 'yuside.cn.numbersonly.MainActivity')
        # 键盘输入检查
        top_y = self.BF.keyboard_get_ready('com.qisiemoji.inputmethod/com.android.inputmethod.latin.LatinIME', 'class',
                                           'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.d, top_y)
        keyboard.send_input('qwertyuiopasdfghjklzxcvbnm')
        keyboard.send_input('shift')
        keyboard.send_input('g')
        s_input = self.BF.attribute_name('classes', 'android.widget.EditText[0]', 'qwertyuiopasdfghjklzxcvbnmG')
        self.BF.check_assertTrue(s_input, '键盘输入内容错误')
        self.kika.clear_download_theme()

    # 跟换emoji的风格
    def emoji_style_change(self):
        top_y = self.BF.keyboard_get_ready('com.qisiemoji.inputmethod/com.android.inputmethod.latin.LatinIME', 'class',
                                           'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.d, top_y)
        keyboard.send_input('emoji')
        old_emoji = keyboard.get_keyboard_picture(0, top_y + 40 * keyboard.density()['density'], keyboard.phone_width,
                                                  keyboard.density()['app'] - top_y - 80 * keyboard.density()[
                                                      'density'],
                                                  'old_emoji')
        self.kika.change_emoji_style(1)
        self.d.start_activity('yuside.cn.numbersonly', 'yuside.cn.numbersonly.MainActivity')
        # 键盘输入检查
        top_y = self.BF.keyboard_get_ready('com.qisiemoji.inputmethod/com.android.inputmethod.latin.LatinIME', 'class',
                                           'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.d, top_y)
        keyboard.send_input('emoji')
        now_emoji = keyboard.keyboard_same(0, top_y + 40 * keyboard.density()['density'], keyboard.phone_width,
                                           keyboard.density()['app'] - top_y - 80 * keyboard.density()['density'],
                                           old_emoji)
        self.BF.check_assertFalse(now_emoji, 'emoji风格更换失败')

    # 下载并更换emoji主题后清理
    def emoji_style_download(self):
        top_y = self.BF.keyboard_get_ready('com.qisiemoji.inputmethod/com.android.inputmethod.latin.LatinIME', 'class',
                                           'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.d, top_y)
        keyboard.send_input('emoji')
        old_emoji = keyboard.get_keyboard_picture(0, top_y + 40 * keyboard.density()['density'], keyboard.phone_width,
                                                  keyboard.density()['app'] - top_y - 80 * keyboard.density()[
                                                      'density'],
                                                  'old_emoji')
        self.kika.random_download_emoji_style()
        self.d.start_activity('yuside.cn.numbersonly', 'yuside.cn.numbersonly.MainActivity')
        # 键盘输入检查
        top_y = self.BF.keyboard_get_ready('com.qisiemoji.inputmethod/com.android.inputmethod.latin.LatinIME', 'class',
                                           'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.d, top_y)
        keyboard.send_input('emoji')
        now_emoji = keyboard.keyboard_same(0, top_y + 40 * keyboard.density()['density'], keyboard.phone_width,
                                           keyboard.density()['app'] - top_y - 80 * keyboard.density()['density'],
                                           old_emoji)
        self.BF.check_assertFalse(now_emoji, 'emoji风格更换失败')
        self.kika.clear_download_emoji_style()

    # 下载font对比后并清理
    def download_font(self):
        top_y = self.BF.keyboard_get_ready('com.qisiemoji.inputmethod/com.android.inputmethod.latin.LatinIME', 'class',
                                           'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.d, top_y)
        old_keyboard = keyboard.get_keyboard_picture(0, top_y + 40 * keyboard.density()['density'],
                                                     keyboard.phone_width,
                                                     (keyboard.density()['app'] - top_y - 40 * keyboard.density()[
                                                         'density']) * 3 / 4,
                                                     'keyboard_old')
        self.kika.random_download_font()
        self.d.start_activity('yuside.cn.numbersonly', 'yuside.cn.numbersonly.MainActivity')
        time.sleep(5)
        top_y = self.BF.keyboard_get_ready('com.qisiemoji.inputmethod/com.android.inputmethod.latin.LatinIME', 'class',
                                           'android.widget.ScrollView')

        keyboard = Keyboard_Operation(self.d, top_y)
        k = keyboard.keyboard_same(0, top_y + 40 * keyboard.density()['density'], keyboard.phone_width,
                                   (keyboard.density()['app'] - top_y - 40 * keyboard.density()['density']) * 3 / 4,
                                   old_keyboard)
        self.BF.check_assertFalse(k, '字体修改失败')
        self.kika.clear_font()

    # pop_key检查
    def pop_key(self):
        top_y = self.BF.keyboard_get_ready('com.qisiemoji.inputmethod/com.android.inputmethod.latin.LatinIME',
                                           'class',
                                           'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.d, top_y)
        keyboard.pop_select('a', 'á')
        a = self.BF.attribute_name('xpath', '//android.widget.EditText[@index="0"]', 'á')
        self.BF.check_assertTrue(a, 'popkey有问题')
        self.BF.check_find_element('xpath', '//android.widget.EditText[@index="0"]').clear()
        keyboard.send_input('number')
        keyboard.pop_select('.', '…', keyboard_type='normal_number')
        number = self.BF.attribute_name('xpath', '//android.widget.EditText[@index="0"]', '…')
        self.BF.check_assertTrue(number, 'popkey有问题')
        self.BF.check_find_element('xpath', '//android.widget.EditText[@index="0"]').clear()
        keyboard.send_input('symbol', keyboard_type='normal_number')
        keyboard.pop_select('=', '∞', keyboard_type='normal_symbol')
        symbol = self.BF.attribute_name('xpath', '//android.widget.EditText[@index="0"]', '∞')
        self.BF.check_assertTrue(symbol, 'popkey有问题')

    # 开启Number和Select后的layout检查
    def keyboard_layout(self):
        default_top_y = self.BF.keyboard_get_ready('com.qisiemoji.inputmethod/com.android.inputmethod.latin.LatinIME',
                                                   'class',
                                                   'android.widget.ScrollView')
        # 开启数字和select
        self.kika.app_settings()
        self.BF.click('name', 'Keyboard Settings')
        self.BF.click_change('xpath',
                             '//*[@text="Number Row"]/../../android.widget.LinearLayout')
        self.BF.click_change('xpath',
                             '//*[@text="Selector Row"]/../../android.widget.LinearLayout')
        # 打开input
        self.d.start_activity('yuside.cn.numbersonly', 'yuside.cn.numbersonly.MainActivity')
        top_y = self.BF.keyboard_get_ready('com.qisiemoji.inputmethod/com.android.inputmethod.latin.LatinIME', 'class',
                                           'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.d, top_y)
        keyboard.send_input('1234567890', number=True, select=True)
        number = self.BF.attribute_name('xpath', '//android.widget.EditText[@index="0"]', '1234567890')
        self.BF.check_assertTrue(number, '输入错误，数字键有问题')
        self.BF.check_find_element('xpath', '//android.widget.EditText[@index="0"]').clear()
        self.BF.click('xpath', '//android.widget.EditText[@index="0"]')
        keyboard.send_input('asdfghj', inputtype='long_pass', number=True, select=True)
        symbol = self.BF.attribute_name('xpath', '//android.widget.EditText[@index="0"]', '@#$%&-+')
        self.BF.check_assertTrue(symbol, '输入错误，pop_key有问题')
        # 关闭Number和Select
        self.kika.app_settings()
        self.BF.click('name', 'Keyboard Settings')
        self.BF.click_change('xpath',
                             '//*[@text="Number Row"]/../../android.widget.LinearLayout')
        self.BF.click_change('xpath',
                             '//*[@text="Selector Row"]/../../android.widget.LinearLayout')
        # 检查键盘是否高度变化
        self.d.start_activity('yuside.cn.numbersonly', 'yuside.cn.numbersonly.MainActivity')
        new_top_y = self.BF.keyboard_get_ready('com.qisiemoji.inputmethod/com.android.inputmethod.latin.LatinIME',
                                               'class',
                                               'android.widget.ScrollView')
        if default_top_y == new_top_y:
            cancel_result = True
        else:
            cancel_result = False
        self.BF.check_assertTrue(cancel_result, '取消Number和Select后键盘高度变化了')

    # 新老版本语言
    def new_language(self):
        self.kika.precast_condition('com.emoji.ikeyboard',
                                    '/Users/xm/Downloads/app-ikeyboard-96601-release-news_refactor.apk')
        self.BF.adb_install('/Users/xm/Downloads/app-kika-193601-release-a26fe07.apk', DEVICE_CONFIG)
        self.kika.app_settings()
        self.BF.click('name', 'Language')
        l1 = self.BF.existence('name', 'English (US)')
        l2 = self.BF.existence('name', 'Español (US)')
        l3 = self.BF.existence('name', 'Português (Brasil)')
        if l1 and l2 and l3 is True:
            new_result = True
        else:
            new_result = False
        self.BF.check_assertTrue(new_result, '覆盖安装后键盘的内容减少了')

    def test(self):
        top_y = self.BF.keyboard_get_ready('com.qisiemoji.inputmethod/com.android.inputmethod.latin.LatinIME', 'class',
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
    # suite.addTest(Keyboard_Test('precast_condition'))
    # suite.addTest(InputApp('theme'))
    # suite.addTest(InputApp('old_new_app1'))
    # suite.addTest(InputApp('old_new_app2'))
    # suite.addTest(InputApp('old_new_app3'))
    # suite.addTest(InputApp('precast_condition'))
    # suite.addTest(InputApp('theme_change'))
    # suite.addTest(InputApp('downloda_theme'))
    # suite.addTest(InputApp('emoji_style_change'))
    # suite.addTest(InputApp('emoji_style_download'))
    # suite.addTest(InputApp('download_font'))
    # suite.addTest(InputApp('pop_key'))
    # suite.addTest(InputApp('keyboard_layout'))
    # suite.addTest(InputApp('new_language'))
    suite.addTest(InputApp('test', 'HT54ASV03365'))
    # 执行用例
    runner = unittest.TextTestRunner()
    # filename = '%s' % report('gz')
    # fp = open(filename, 'wb')
    # runner = HTMLTestRunner(stream=fp, title='自动化测试报告', description='自动化测试报告')
    runner.run(suite)
