# -*- coding: utf-8 -*-
# __author__ = 'gz'


import os
import re
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
    def setUp(self):
        print('Test start')
        desired_caps = {}
        desired_caps['automationName'] = "appium"  # Appium,UiAutomator2,XCUITest,YouiEngine
        desired_caps['platformName'] = 'Android'
        desired_caps['deviceName'] = DEVICE_CONFIG
        desired_caps['udid'] = DEVICE_CONFIG
        desired_caps['appPackage'] = 'yuside.cn.numbersonly'
        desired_caps['appActivity'] = 'yuside.cn.numbersonly.MainActivity'
        # desired_caps['appPackage'] = 'com.qisiemoji.inputmethod'
        # desired_caps['appActivity'] = 'com.qisi.ikeyboarduirestruct.NavigationActivity'
        # 隐藏键盘
        # desired_caps['resetKeyboard'] = 'True'
        # 使用appium键盘
        # desired_caps['unicodeKeyboard'] = 'True'
        self.d = webdriver.Remote('http://%s:%s/wd/hub' % (APPIUM_CONFIG[0], APPIUM_CONFIG[1]), desired_caps)
        # self.d = webdriver.Remote('http://%s:%s/wd/hub' % ('127.0.0.1', '4711'), desired_caps)
        self.extend = Appium_Extend(self.d)
        self.BF = BaseFunction(self, self.d)
        self.kika = Kika_Function(self, self.d)
        time.sleep(2)



    def tearDown(self):
        print('Test end')
        self.d.quit()


    def test_add_language(self):
        print('Test add language, swipe and screenshot keyboard: ')
        new = '/Users/yanqing.xu/Downloads/app-kika-215101-release-ef36305.apk'
        old = '/Users/yanqing.xu/Downloads/app-kika-214801-release-60bf8dd.apk'
        package = 'com.qisiemoji.inputmethod'
        Typewriting = package + '/com.android.inputmethod.latin.LatinIME'
        activity = package + '/com.qisi.ikeyboarduirestruct.NavigationActivity'
        # 添加和截取键盘个数
        num = 50
        # 滑动添加时滑动次数
        rd = 20
        for i in range(0, 11):
            if self.kika.device_config == 'none':
                try:
                    unin_result = os.popen('adb uninstall %s' % package)
                except Exception as e:
                    print(e)
                    print('没有对应应用')
            else:
                try:
                    unin_result = os.popen('adb -s %s uninstall %s' % (self.device_config, package))
                except Exception as e:
                    print(e)
                    print('没有对应应用')
        os.system('adb install -r %s' % old)


      # 安装测试包并设置默认输入法
      #   del_package = 'com.qisiemoji.inputmethod'
        self.BF.keyboard_select(Typewriting)
        time.sleep(2)
        self.BF.open_app_atcivity(activity)
        time.sleep(3)
        self.BF.click('name','Settings')
        time.sleep(1)
        self.BF.click('name','Language')
    #   获取手机分辨率，计算右下角add大概坐标
    # adb shell dumpsys window displays |head -n 3计算x y
        dis = os.popen('adb shell dumpsys window displays |head -3').read()
        x = re.findall(r'init\=(.*?)x', dis)[0]
        y = re.findall(r'x(.*?)\s', dis)[0]
        swipex = int(x) * 1 / 2
        swipey1 = int(y) * 3 / 4
        swipey2 = int(y) * 1 / 4
        addx = int(x) - 30
        addy = int(y) - 100
        swipe = 'adb shell input swipe '
        add = 'adb shell input tap '
        # 向上滑
        for i in range(rd):
            print("swipe time:", i)
            ret = os.popen(
                swipe + str(int(swipex)) + ' ' + str(int(swipey1)) + ' ' + str(int(swipex)) + ' ' + str(int(swipey2)))
            ret.close()

        # 点击add添加所有language
        for j in range(num):
            print('Add language time:', j)
            try:
                self.BF.check_find_element('name','Yes')
                time.sleep(0.5)
                self.BF.click('name','Yes')
            except:
                pass
            os.system(add + str(addx) + ' ' + str(addy))


        os.system('adb shell am start -n yuside.cn.numbersonly/.MainActivity')
        time.sleep(1)

        top_y = self.BF.keyboard_get_ready(Typewriting, 'class',
                                           'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.d, top_y)
        width = keyboard.phone_width
        # 获取空格键位置
        sp = keyboard.keyboard_reader(' ')
        height = (keyboard.phone_height - top_y)
        time.sleep(1)


        picinfo = dict()
        for k in range(num):
            keyboard.swip_location(sp['x'], sp['y'], sp['width'], sp['height'])
            time.sleep(1)
            picinfo[k]=keyboard.get_keyboard_picture(0, top_y, width, height, 'lang')
        # ******************分割线*********
        # 等待几秒，安装新版包，做截图对比
        time.sleep(2)
        os.system('adb uninstall %s' % package)
        os.system('adb install -r %s' % new)
        self.BF.keyboard_select(Typewriting)
        self.BF.open_app_atcivity(activity)
        time.sleep(3)
        self.BF.click('name', 'Settings')
        time.sleep(1)
        self.BF.click('name', 'Language')

        for i in range(rd):
            print("swipe time:", i)
            ret = os.popen(
                swipe + str(int(swipex)) + ' ' + str(int(swipey1)) + ' ' + str(int(swipex)) + ' ' + str(int(swipey2)))
            ret.close()

        # 点击add添加所有language
        for j in range(num):
            print('Add language time:', j)
            try:
                self.BF.check_find_element('name', 'Yes')
                time.sleep(0.5)
                self.BF.click('name', 'Yes')
            except:
                pass
            os.system(add + str(addx) + ' ' + str(addy))
        os.system('adb shell am start -n yuside.cn.numbersonly/.MainActivity')
        self.BF.keyboard_get_ready(Typewriting, 'class',
                                   'android.widget.ScrollView')
        for k in range(num):
            keyboard.swip_location(sp['x'], sp['y'], sp['width'], sp['height'])
            time.sleep(1)
            keyboard.keyboard_same(0, top_y, width, height,picinfo[k])
        time.sleep(1)




if __name__ == "__main__":
    # 编辑用例
    # suite = Suit()
    suite = unittest.TestSuite()
    suite.addTest(Keyboard_Test('test_add_language'))
    # 执行用例
    runner = unittest.TextTestRunner()
    runner.run(suite)
