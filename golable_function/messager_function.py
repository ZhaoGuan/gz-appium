# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from golable_function.basefunction import BaseFunction
from golable_function.extend import Appium_Extend
import time


class MessagerFunction:
    def __init__(self, tester, driver, device_config='none'):
        self.driver = driver
        self.BF = BaseFunction(tester, self.driver)
        self.appium_extend = Appium_Extend(self.driver)
        self.device_config = device_config

    def select_user(self, type_writing):
        self.BF.click('id', 'com.facebook.orca:id/recents_tab')
        time.sleep(10)
        # self.BF.click('classes', 'android.view.ViewGroup[0]')
        # 点击第一个用户
        self.BF.location_click('classes', 'android.view.ViewGroup[0]')
        self.BF.click('id', 'com.facebook.orca:id/text_input_bar')
        top_y = self.BF.keyboard_get_ready(type_writing, 'id',
                                           'com.facebook.orca:id/thread_view_root')
        return top_y
