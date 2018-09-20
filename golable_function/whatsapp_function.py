# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from golable_function.basefunction import BaseFunction
from golable_function.extend import Appium_Extend
import time


class Whatsapp_Function():
    def __init__(self, tester, driver, device_config='none'):
        self.driver = driver
        self.BF = BaseFunction(tester, self.driver)
        self.AppiumExtend = Appium_Extend(self.driver)
        self.device_config = device_config

    def select_user(self, Typewriting):
        self.BF.click('id', 'com.whatsapp:id/conversations_row_contact_name_holder')
        self.BF.click('id', 'com.whatsapp:id/entry')
        top_y = self.BF.keyboard_get_ready(Typewriting, 'id',
                                           'com.whatsapp:id/action_bar_root')
        return top_y
