# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from golable_function.basefunction import BaseFunction
from golable_function.keyboard_function import Keyboard_Operation
from golable_function.image_recognition import *
from golable_function.extend import Appium_Extend
import os
import time


class Kika_Function:
    def __init__(self, tester, driver, device_config='none'):
        self.driver = driver
        self.BF = BaseFunction(tester, self.driver)
        self.AppiumExtend = Appium_Extend(self.driver)
        self.device_config = device_config

    # 这个主要作为一个例子其中会涉及到使用到的安卓系统导致没有适配的能力所以暂时只写个例子
    def precast_condition(self, del_package, install_package_path, Typewriting):
        # 删除应用
        if self.device_config == 'none':
            try:
                unin_result = os.popen('adb uninstall %s' % del_package)
            except Exception as e:
                print(e)
                print('没有对应应用')
        else:
            try:
                unin_result = os.popen('adb -s %s uninstall %s' % (self.device_config, del_package))
            except Exception as e:
                print(e)
                print('没有对应应用')
        # 安装应用
        self.BF.adb_install(install_package_path, self.device_config)
        self.BF.keyboard_select(Typewriting, self.device_config)
        self.BF.open_app_atcivity('com.qisiemoji.inputmethod/com.qisi.ikeyboarduirestruct.NavigationActivity')
        theme = self.BF.existence('name', 'Settings')
        if theme == False:
            count = 0
            while True:
                try:
                    self.BF.click('name', 'Allow')
                    count += 1
                except:
                    time.sleep(3)
                if count == 3:
                    break
                if count == 6:
                    break
        self.BF.keyboard_select('com.qisiemoji.inputmethod/com.android.inputmethod.latin.LatinIME')
        # 点击设定
        self.BF.click('id', 'com.qisiemoji.inputmethod:id/item_settigns')
        # 点击语言
        self.BF.click('name', 'Language')
        # time.sleep(10)
        # 选择语言的时候最好根据自上而下的顺序这样就很快的都能加上
        # self.reach_language_add('Español (US)')
        # self.reach_language_add('Português (Brasil)')
        # self.driver.back()
        # self.BF.click('name', 'Language')
        # if self.BF.existence('name', 'Español (US)') and self.BF.existence('name',
        #                                                                    'English (US)') and self.BF.existence('name',
        #                                                                                                          'Português (Brasil)'):
        #     pass
        # else:
        #     assert 1 + 1 > 2, '语言添加失败'
        self.driver.start_activity('yuside.cn.numbersonly', 'yuside.cn.numbersonly.MainActivity')
        # 获取的高度不是默认的高度
        top_y = self.BF.keyboard_get_ready(Typewriting, 'class', 'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.driver, top_y)
        self.driver.back()
        self.BF.click('xpath', '//android.widget.EditText[@index="0"]')
        # 重新获取键盘高度
        top_y = self.BF.keyboard_get_ready(Typewriting, 'class', 'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.driver, top_y)
        keyboard.send_input('emoji')
        self.driver.back()
        self.BF.click('xpath', '//android.widget.EditText[@index="0"]')
        keyboard.send_input('emoji')
        keyboard.send_input('emoji', 'emoji')
        keyboard.select_emoji('emoji', 1, 3)
        emoji = self.BF.attribute_name('xpath', '//android.widget.EditText[@index="0"]', '😂')
        self.BF.check_assertTrue(emoji, 'emoji默认设置取消失败')

    # 寻找语言添加到键盘中（language根据应用中来选取）
    def reach_language_add(self, language):
        # 'Español'
        # 滑动高度v_y是根据语言名称外面的layout控件的高度来的有需要自己设定
        v_y = self.BF.element_size('id', 'com.qisiemoji.inputmethod:id/root', "height")
        self.BF.reach_element_click(v_y * 5, 'name', language)
        language_no = self.BF.elements('id', 'com.qisiemoji.inputmethod:id/tv_name')
        for i in range(len(language_no)):
            find_l = self.BF.attribute_name('ides', 'com.qisiemoji.inputmethod:id/tv_name[%s]' % i)
            if find_l == language:
                print(find_l)
                self.BF.click('ides', 'com.qisiemoji.inputmethod:id/tv_add[%s]' % i)

    def app_theme(self):
        self.BF.open_app_atcivity('com.qisiemoji.inputmethod/com.qisi.ikeyboarduirestruct.NavigationActivity')
        self.BF.keyboard_select('com.qisiemoji.inputmethod/com.android.inputmethod.latin.LatinIME')

        theme = self.BF.existence('name', 'Settings')
        if theme == False:
            count = 0
            while True:
                try:
                    self.BF.click('name', 'Allow')
                    count += 1
                except:
                    time.sleep(3)
                if count == 3:
                    break
            theme = self.BF.existence('name', 'Settings')
        self.BF.click('name', 'Theme')
        self.BF.check_assertTrue(theme, '进入Theme页面失败')

    def app_settings(self):
        self.BF.open_app_atcivity('com.qisiemoji.inputmethod/com.qisi.ikeyboarduirestruct.NavigationActivity')
        settings = self.BF.click_change('id', 'com.qisiemoji.inputmethod:id/item_settigns')
        self.BF.check_assertTrue(settings, '点击Setting失败')

    def old_new_app_theme(self, i, package, Typewriting, old, new):
        if self.device_config == 'none':
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
        # 安装老应用
        # self.driver.install_app(old)
        o = os.popen('adb install -r %s' % old)
        print(o.read())
        self.BF.keyboard_select(Typewriting)
        self.change_theme(i)
        self.driver.start_activity('yuside.cn.numbersonly', 'yuside.cn.numbersonly.MainActivity')
        # 截图
        top_y = self.BF.keyboard_get_ready(Typewriting, 'class', 'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.driver, top_y)
        old_keyboard = keyboard.get_keyboard_picture(0, top_y + 40 * keyboard.density()['density'],
                                                     keyboard.phone_width,
                                                     (keyboard.density()['app'] - top_y - 40 * keyboard.density()[
                                                         'density']) * 3 / 4,
                                                     'keyboard_old')
        self.driver.back()
        self.driver.back()
        # 强制安装
        self.BF.adb_install(new, self.device_config)
        # 对比
        # 以防键盘不弹起来
        self.BF.keyboard_select(Typewriting)
        self.driver.start_activity('yuside.cn.numbersonly', 'yuside.cn.numbersonly.MainActivity')
        time.sleep(5)
        top_y = self.BF.keyboard_get_ready(Typewriting, 'class', 'android.widget.ScrollView')

        keyboard = Keyboard_Operation(self.driver, top_y)
        k = keyboard.keyboard_same(0, top_y + 40 * keyboard.density()['density'],
                                   keyboard.phone_width,
                                   (keyboard.density()['app'] - top_y - 40 * keyboard.density()[
                                       'density']) * 3 / 4,
                                   old_keyboard)
        # self.BF.check_assertTrue(k, '第%s个默认主题出现问题' % (no + 1))
        return {'%s' % (i + 1): k}

    def old_new_app_font(self, i, package, Typewriting, old, new):
        if self.device_config == 'none':
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
        # 安装老应用
        # self.driver.install_app(old)
        o = os.popen('adb install -r %s' % old)
        print(o.read())
        self.BF.keyboard_select(Typewriting)
        self.cheage_font(i)
        self.driver.start_activity('yuside.cn.numbersonly', 'yuside.cn.numbersonly.MainActivity')
        # 截图
        top_y = self.BF.keyboard_get_ready(Typewriting, 'class', 'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.driver, top_y)
        old_font = keyboard.get_keyboard_picture(0, top_y + 40 * keyboard.density()['density'],
                                                 keyboard.phone_width,
                                                 (keyboard.density()['app'] - top_y - 40 * keyboard.density()[
                                                     'density']) * 3 / 4,
                                                 'font_old')
        self.driver.back()
        self.driver.back()
        # 强制安装
        self.BF.adb_install(new, self.device_config)
        # 对比
        self.BF.keyboard_select(Typewriting)
        self.driver.start_activity('yuside.cn.numbersonly', 'yuside.cn.numbersonly.MainActivity')
        time.sleep(5)
        top_y = self.BF.keyboard_get_ready(Typewriting, 'class', 'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.driver, top_y)
        k = keyboard.keyboard_same(0, top_y + 40 * keyboard.density()['density'], keyboard.phone_width,
                                   (keyboard.density()['app'] - top_y - 40 * keyboard.density()['density']) * 3 / 4,
                                   old_font)
        # self.BF.check_assertTrue(k, '第%s个默认字体出现问题' % (no + 1))
        return {'%s' % (i + 1): k}

    def seekbar(self, how, element, x):
        seekbar_button = self.BF.check_find_element(how, element)
        seekbar_button_x = seekbar_button.location['x']
        seekbar_button_y = seekbar_button.location['y']
        seekbar_button_width = seekbar_button.size['width']
        seekbar_button_height = seekbar_button.size['height']
        # 调节
        # begin_button_x = seekbar_button_x + seekbar_button_width
        begin_button_y = seekbar_button_y + seekbar_button_height / 2
        # end_button_x = seekbar_button_x + seekbar_button_width / 2
        # self.driver.swipe(start_x=begin_button_x * s_x, start_y=begin_button_y, end_x=end_button_x * e_x,
        #                   end_y=begin_button_y)
        self.driver.tap([(seekbar_button_x + seekbar_button_width * x, begin_button_y)])

    def custom_keyboard(self):
        self.app_theme()
        self.BF.click('id', 'com.qisiemoji.inputmethod:id/fab')
        self.BF.click('id', 'com.qisiemoji.inputmethod:id/fab')
        # 选择背景
        self.BF.random_click('xpath',
                             '//android.support.v4.view.ViewPager/android.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout[3]/android.widget.ImageButton')
        # Effect设定
        Effect = self.BF.click_change('name', 'Effect')
        self.BF.check_assertTrue(Effect, 'Effect点击无反应')
        theme_preview = self.BF.element_picture('id', 'com.qisiemoji.inputmethod:id/theme_preview')
        # 获取seekbar控件属性
        self.seekbar('id', 'com.qisiemoji.inputmethod:id/seek_bar_color_brightness', 1 / 2)
        theme_preview_change = self.BF.cintrast_element_picture('id',
                                                                'com.qisiemoji.inputmethod:id/seek_bar_color_brightness',
                                                                theme_preview)
        self.BF.check_assertFalse(theme_preview_change, 'Effect没有变化')
        # Button
        self.BF.click('name', 'Button')
        theme_preview_button = self.BF.element_picture('id', 'com.qisiemoji.inputmethod:id/theme_preview')
        self.BF.click_change('id', 'com.qisiemoji.inputmethod:id/button_2')
        theme_preview_button_change = self.BF.cintrast_element_picture('id',
                                                                       'com.qisiemoji.inputmethod:id/theme_preview',
                                                                       theme_preview_button)
        self.BF.check_assertFalse(theme_preview_button_change, 'button2修改无变化')
        self.BF.click_change('id', 'com.qisiemoji.inputmethod:id/button_1')
        theme_preview_button1_change = self.BF.cintrast_element_picture('id',
                                                                        'com.qisiemoji.inputmethod:id/theme_preview',
                                                                        theme_preview_button)
        self.BF.check_assertTrue(theme_preview_button1_change, 'button1点击无效果')
        theme_preview_button_seekbar = self.BF.element_picture('id', 'com.qisiemoji.inputmethod:id/theme_preview')
        self.seekbar('id', 'com.qisiemoji.inputmethod:id/seek_bar', 3 / 4)
        theme_preview_button_seekbar_change = self.BF.cintrast_element_picture('id',
                                                                               'com.qisiemoji.inputmethod:id/theme_preview',
                                                                               theme_preview_button_seekbar)
        self.BF.check_assertFalse(theme_preview_button_seekbar_change, 'button seek没有变化')
        # Font
        self.BF.click('name', 'Font')
        theme_preview_fount = self.BF.element_picture('id', 'com.qisiemoji.inputmethod:id/theme_preview')
        self.seekbar('id', 'com.qisiemoji.inputmethod:id/seek_bar', 1 / 3)
        theme_preview_fount_change = self.BF.cintrast_element_picture('id',
                                                                      'com.qisiemoji.inputmethod:id/theme_preview',
                                                                      theme_preview_fount)
        self.BF.check_assertFalse(theme_preview_fount_change, '字体大小没有变化')
        theme_preview_fount1 = self.BF.element_picture('id', 'com.qisiemoji.inputmethod:id/theme_preview')
        self.BF.random_click('id', 'com.qisiemoji.inputmethod:id/button')
        theme_preview_fount1_change = self.BF.cintrast_element_picture('id',
                                                                       'com.qisiemoji.inputmethod:id/theme_preview',
                                                                       theme_preview_fount1)
        self.BF.check_assertFalse(theme_preview_fount1_change, '字体样式没有变化')
        # color 无法做
        self.BF.click('id', 'com.qisiemoji.inputmethod:id/save')
        while True:
            try:
                self.BF.click('name', 'Theme saved successfully!')
                break
            except:
                pass
        self.BF.click('id', 'com.qisiemoji.inputmethod:id/md_buttonDefaultPositive')
        self.BF.result_picture('自定义键盘')

    def old_new_app_custom_keyboard(self, package, Typewriting, old, new):
        if self.device_config == 'none':
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
        # 安装老应用
        o = os.popen('adb install -r %s' % old)
        print(o.read())
        self.BF.keyboard_select(Typewriting)
        self.custom_keyboard()
        self.driver.tap([(200, 200)])
        self.driver.back()
        self.driver.start_activity('yuside.cn.numbersonly', 'yuside.cn.numbersonly.MainActivity')
        # 截图
        top_y = self.BF.keyboard_get_ready(Typewriting, 'class', 'android.widget.ScrollView')
        keyboard = Keyboard_Operation(self.driver, top_y)
        old_keyboard = keyboard.get_keyboard_picture(0, top_y + 40 * keyboard.density()['density'],
                                                     keyboard.phone_width,
                                                     (keyboard.density()['app'] - top_y - 40 * keyboard.density()[
                                                         'density']) * 3 / 4,
                                                     'keyboard_old')
        self.driver.back()
        self.driver.back()
        # 强制安装
        self.BF.adb_install(new, self.device_config)
        # 对比
        self.BF.keyboard_select(Typewriting)
        self.driver.start_activity('yuside.cn.numbersonly', 'yuside.cn.numbersonly.MainActivity')
        time.sleep(5)
        top_y = self.BF.keyboard_get_ready(Typewriting, 'class', 'android.widget.ScrollView')

        keyboard = Keyboard_Operation(self.driver, top_y)
        k = keyboard.keyboard_same(0, top_y + 40 * keyboard.density()['density'], keyboard.phone_width,
                                   (keyboard.density()['app'] - top_y - 40 * keyboard.density()['density']) * 3 / 4,
                                   old_keyboard)
        self.BF.check_assertTrue(k, '自定义主题消失了')

    # 自定义主题
    def change_custom_keyboard(self):
        self.app_theme()
        self.BF.click('id', 'com.qisiemoji.inputmethod:id/fab')
        before_change = self.BF.element_picture('ides', 'com.qisiemoji.inputmethod:id/item[0]')
        self.BF.click('id', 'com.qisiemoji.inputmethod:id/edit')
        self.BF.click('id', 'com.qisiemoji.inputmethod:id/edit_button_action')
        # 选择背景
        background = self.BF.element_picture('id', 'com.qisiemoji.inputmethod:id/theme_preview')
        bg_count = 0
        while True:
            self.BF.random_click('xpath',
                                 '//android.support.v4.view.ViewPager/android.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout[3]/android.widget.ImageButton')
            change_background = self.BF.cintrast_element_picture('id', 'com.qisiemoji.inputmethod:id/theme_preview',
                                                                 background)
            if change_background == False:
                c_b_g_r = True
                break
            else:
                bg_count += 1
                if bg_count >= 10:
                    c_b_g_r = False
                    break
        self.BF.check_assertTrue(c_b_g_r, '超时或者背景修改失败')
        # Effect设定
        Effect = self.BF.click_change('name', 'Effect')
        self.BF.check_assertTrue(Effect, 'Effect点击无反应')
        theme_preview = self.BF.element_picture('id', 'com.qisiemoji.inputmethod:id/theme_preview')
        # 获取seekbar控件属性
        self.seekbar('id', 'com.qisiemoji.inputmethod:id/seek_bar_color_brightness', 1 / 3)
        theme_preview_change = self.BF.cintrast_element_picture('id',
                                                                'com.qisiemoji.inputmethod:id/seek_bar_color_brightness',
                                                                theme_preview)
        self.BF.check_assertFalse(theme_preview_change, 'Effect没有变化')
        # Button
        self.BF.click('name', 'Button')
        theme_preview_button = self.BF.element_picture('id', 'com.qisiemoji.inputmethod:id/theme_preview')
        self.BF.click_change('id', 'com.qisiemoji.inputmethod:id/button_2')
        theme_preview_button_change = self.BF.cintrast_element_picture('id',
                                                                       'com.qisiemoji.inputmethod:id/theme_preview',
                                                                       theme_preview_button)
        self.BF.check_assertFalse(theme_preview_button_change, 'button2修改无变化')
        theme_preview_button_seekbar = self.BF.element_picture('id', 'com.qisiemoji.inputmethod:id/theme_preview')
        self.seekbar('id', 'com.qisiemoji.inputmethod:id/seek_bar', 1 / 4)
        theme_preview_button_seekbar_change = self.BF.cintrast_element_picture('id',
                                                                               'com.qisiemoji.inputmethod:id/theme_preview',
                                                                               theme_preview_button_seekbar)
        self.BF.check_assertFalse(theme_preview_button_seekbar_change, 'button seek没有变化')
        # Font
        self.BF.click('name', 'Font')
        theme_preview_fount = self.BF.element_picture('id', 'com.qisiemoji.inputmethod:id/theme_preview')
        self.seekbar('id', 'com.qisiemoji.inputmethod:id/seek_bar', 2 / 3)
        theme_preview_fount_change = self.BF.cintrast_element_picture('id',
                                                                      'com.qisiemoji.inputmethod:id/theme_preview',
                                                                      theme_preview_fount)
        self.BF.check_assertFalse(theme_preview_fount_change, '字体大小没有变化')
        theme_preview_fount1 = self.BF.element_picture('id', 'com.qisiemoji.inputmethod:id/theme_preview')
        f_count = 0
        while True:
            self.BF.random_click('id', 'com.qisiemoji.inputmethod:id/button')
            theme_preview_fount1_change = self.BF.cintrast_element_picture('id',
                                                                           'com.qisiemoji.inputmethod:id/theme_preview',
                                                                           theme_preview_fount1)
            if theme_preview_fount1_change == False:
                c_f_r = True
                break
            else:
                f_count += 1
                if bg_count >= 10:
                    c_f_r = False
                    break
        self.BF.check_assertTrue(c_f_r, '超时或者字体修改失败')
        # color 无法做
        self.BF.click('id', 'com.qisiemoji.inputmethod:id/save')
        while True:
            try:
                self.BF.click('name', 'Theme saved successfully!')
                break
            except:
                pass
        self.BF.click('id', 'com.qisiemoji.inputmethod:id/md_buttonDefaultPositive')
        self.BF.result_picture('自定义键盘修改结果')
        self.driver.back()
        self.BF.click('id', 'com.qisiemoji.inputmethod:id/edit')
        after_change = self.BF.cintrast_element_picture('ides', 'com.qisiemoji.inputmethod:id/item[0]', before_change)
        self.BF.check_assertFalse(after_change, '自定义键盘修改失败')

    # 选择第i个默认主题
    def change_theme(self, i):
        self.app_theme()
        self.BF.click('name', 'Theme')
        self.BF.click('id', 'com.qisiemoji.inputmethod:id/fab')
        time.sleep(2)
        no = i
        if i > 7:
            self.driver.swipe(start_x=self.driver.get_window_size()['width'] / 2,
                              start_y=self.driver.get_window_size()['height'] * 3 / 4,
                              end_x=self.driver.get_window_size()['width'] / 2,
                              end_y=self.driver.get_window_size()['height'] / 4)
            if i == 8:
                i = 4
            elif i == 9:
                i = 5
            elif i == 10:
                i = 6
            elif i == 11:
                i = 7
        self.BF.click('ides', 'com.qisiemoji.inputmethod:id/item[%s]' % i)
        self.driver.tap([(200, 200)])
        self.driver.back()

    def random_download_theme(self):
        self.app_theme()
        self.BF.click('name', 'More')
        self.BF.random_click('id', 'com.qisiemoji.inputmethod:id/item')
        self.BF.click('id', 'com.qisiemoji.inputmethod:id/button_download')
        count_install = 0
        while True:
            ex = self.BF.existence('id', 'com.android.vending:id/buy_button')
            if ex == True:
                self.BF.click('id', 'com.android.vending:id/buy_button')
                while_result1 = True
                break
            else:
                count_install += 1
                time.sleep(3)
                if count_install > 10:
                    while_result1 = False
                    break
        self.BF.check_assertTrue(while_result1, '未跳转到主题下载页')
        count_open = 0
        while True:
            ex = self.BF.existence('id', 'com.android.vending:id/launch_button')
            if ex == True:
                self.BF.click('id', 'com.android.vending:id/launch_button')
                while_result2 = True
                break
            else:
                count_open += 1
                time.sleep(3)
                if count_open > 20:
                    while_result2 = False
                    break
        self.BF.check_assertTrue(while_result2, '打开主题失败')
        time.sleep(10)
        self.BF.click('name', 'ACTIVATE THEME')

    def clear_download_theme(self):
        self.app_theme()
        self.BF.click('id', 'com.qisiemoji.inputmethod:id/fab')
        self.BF.click('id', 'com.qisiemoji.inputmethod:id/edit')
        while True:
            self.BF.click('id', 'com.qisiemoji.inputmethod:id/delete_button_action')
            self.BF.click('name', 'OK')
            time.sleep(8)
            if self.BF.existence('name', 'Downloaded') is False:
                break
        print('下载主题清理完毕')

    def change_emoji_style(self, i):
        self.app_theme()
        self.BF.click('name', 'Emoji')
        self.BF.click('id', 'com.qisiemoji.inputmethod:id/fab')
        self.BF.click('ides', 'com.qisiemoji.inputmethod:id/card_view[%s]' % i)

    def random_download_emoji_style(self):
        self.app_theme()
        self.BF.click('name', 'Emoji')
        self.BF.random_click('id', 'com.qisiemoji.inputmethod:id/card_view')
        self.BF.click('id', 'com.qisiemoji.inputmethod:id/button_download')
        count_install = 0
        while True:
            ex = self.BF.existence('id', 'com.android.vending:id/buy_button')
            if ex == True:
                self.BF.click('id', 'com.android.vending:id/buy_button')
                while_result1 = True
                break
            else:
                count_install += 1
                time.sleep(3)
                if count_install > 10:
                    while_result1 = False
                    break
        self.BF.check_assertTrue(while_result1, '未跳转到emoji_style下载页')
        count_open = 0
        while True:
            ex = self.BF.existence('id', 'com.android.vending:id/launch_button')
            if ex == True:
                self.BF.click('id', 'com.android.vending:id/launch_button')
                while_result2 = True
                break
            else:
                count_open += 1
                time.sleep(3)
                if count_open > 20:
                    while_result2 = False
                    break
        self.BF.check_assertTrue(while_result2, '打开emoji_style失败')
        time.sleep(10)
        self.driver.back()
        self.BF.click('name', 'ACTIVATE EMOJI')

    def clear_download_emoji_style(self):
        self.app_theme()
        self.BF.click('name', 'Emoji')
        self.BF.click('id', 'com.qisiemoji.inputmethod:id/fab')
        self.BF.click('id', 'com.qisiemoji.inputmethod:id/edit')
        while True:
            self.BF.click('id', 'com.qisiemoji.inputmethod:id/button_action')
            self.BF.click('name', 'OK')
            time.sleep(8)
            if self.BF.existence('id', 'com.qisiemoji.inputmethod:id/button_action') is False:
                break
        print('下载emoji_style清理完毕')

    def cheage_font(self, i):
        self.app_theme()
        y = self.BF.check_find_element('id', 'com.qisiemoji.inputmethod:id/tab_layout').location["y"]
        phone = self.driver.get_window_size()
        self.driver.swipe(start_x=phone['width'] / 2, start_y=y + 10, end_x=0, end_y=y + 10)
        self.BF.click('name', 'Font')
        self.BF.click('id', 'com.qisiemoji.inputmethod:id/fab')
        no = i
        print(len(self.BF.elements('id', 'com.qisiemoji.inputmethod:id/text_font_preview')))
        self.BF.click('ides', 'com.qisiemoji.inputmethod:id/text_font_preview[%s]' % i)
        self.driver.tap([(200, 200)])
        self.driver.back()

    def random_download_font(self):
        self.app_theme()
        self.BF.click('name', 'Sound')
        self.BF.click('name', 'Font')
        self.BF.random_click('id', 'com.qisiemoji.inputmethod:id/text_font_preview')
        self.BF.click('id', 'com.qisiemoji.inputmethod:id/button_download')
        count_install = 0
        while True:
            ex = self.BF.existence('name', 'Apply')
            if ex == True:
                self.BF.click('name', 'Apply')
                while_result1 = True
                break
            else:
                count_install += 1
                time.sleep(3)
                if count_install > 10:
                    while_result1 = False
                    break
        self.BF.check_assertTrue(while_result1, '获取字体失败')
        self.driver.back()

    def clear_font(self):
        self.app_theme()
        self.BF.click('name', 'Sound')
        self.BF.click('name', 'Font')
        self.BF.click('id', 'com.qisiemoji.inputmethod:id/fab')
        self.BF.click('id', 'com.qisiemoji.inputmethod:id/edit')
        while True:
            self.BF.click('id', 'com.qisiemoji.inputmethod:id/action_delete')
            time.sleep(8)
            if self.BF.existence('id', 'com.qisiemoji.inputmethod:id/action_delete') is False:
                break
        print('下载font清理完毕')


if __name__ == '__main__':
    package = 'com.qisiemoji.inputmethod'
    # c = os.popen('adb uninstall %s' % package)
    c = os.system('adb install -r /Users/xm/Downloads/app-oem-debug.apk')
    # 
    # IME = 'com.qisiemoji.inputmethod/com.android.inputmethod.latin.LatinIME'
    # os.system('adb shell ime set %s' % IME)
