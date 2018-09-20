# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import subprocess
import re
import time
import os
from golable_function.extend import Appium_Extend
from golable_function.image_recognition import ocr_text
from golable_function.checkpoint_record import *
from golable_function.picture_different import *
import sys

PATH = os.path.dirname(os.path.abspath(__file__))


class Keyboard_Operation:
    def __init__(self, driver, top_y, device_config='none'):
        self.driver = driver
        self.top_y = top_y
        self.device_config = device_config
        self.phone_height = self.driver.get_window_size()['height']
        self.phone_width = self.driver.get_window_size()['width']
        self.keyheight = (self.phone_height - self.top_y) / 5
        self.AppiumExtend = Appium_Extend(self.driver)
        # 一般键盘键位
        self.keyboard_qwerty = {
            'system': ['0', '1'], 'theme': ['0', '2'], 'masssenge': ['0', '0'], 'sticker2': ['0', '3'],
            'stop': ['0', '4'],
            '1': ['1', '1'], '2': ['1', '2'], '3': ['1', '3'], '4': ['1', '4'], '5': ['1', '5'], '6': ['1', '6'],
            '7': ['1', '7'], '8': ['1', '8'], '9': ['1', '9'], '0': ['1', '10'],
            'q': ['2', '1'], 'w': ['2', '2'], 'e': ['2', '3'], 'r': ['2', '4'], 't': ['2', '5'], 'y': ['2', '6'],
            'u': ['2', '7'], 'i': ['2', '8'], 'o': ['2', '9'], 'p': ['2', '10'],
            'a': ['3', '1'], 's': ['3', '2'], 'd': ['3', '3'], 'f': ['3', '4'], 'g': ['3', '5'], 'h': ['3', '6'],
            'j': ['3', '7'], 'k': ['3', '8'], 'l': ['3', '9'],
            'shift': ['4', '1'], 'z': ['4', '2'], 'x': ['4', '3'], 'c': ['4', '4'], 'v': ['4', '5'], 'b': ['4', '6'],
            'n': ['4', '7'], 'm': ['4', '8'], 'delete': ['4', '9'],
            'number': ['5', '1'], 'emoji': ['5', '2'], ',': ['5', '3'], ' ': ['5', '4'], '.': ['5', '5'],
            'ente': ['5', '6']
        }
        # 一般键盘长按按键(row,line)
        self.normal_keyboard_pop = {
            'q': {'1': [1, 0]},
            'w': {'2': [1, 0]},
            'e': {'è': [1, -1], '3': [1, 0], 'é': [1, 1], 'ē': [2, -1], 'ê': [2, 0], 'ë': [2, 1]},
            '': {'4': [1, 0]},
            't': {'5': [1, 0]},
            'y': {'6': [1, 0]},
            'u': {'û': [1, -1], '7': [1, 0], 'ú': [1, 1], 'ū': [2, -1], 'ü': [2, 0], 'ù': [2, 1]},
            'i': {'î': [1, -1], '8': [1, 0], 'í': [1, 1], 'ì': [2, -1], 'ï': [2, 0], 'ī': [2, 1]},
            'o': {'ó': [1, -1], '9': [1, 0], 'ô': [1, -1], 'ö': [1, -3], 'ò': [1, -4], 'œ': [2, 0], 'ø': [2, -1],
                  'ō': [2, -2], 'õ': [2, -3]},
            'p': {'0': [1, 0]},
            'a': {'@': [1, 0], 'à': [1, 1], 'á': [1, 2], 'â': [1, 3], 'ä': [1, 3], 'æ': [2, 0], 'ã': [2, 1],
                  'å': [2, 2], 'ā': [2, 3]},
            's': {'#': [1, 0], 'ß': [1, 1]},
            'd': {'$': [1, 0]},
            'f': {'%': [1, 0]},
            'g': {'&': [1, 0]},
            'h': {'-': [1, 0]},
            'j': {'+': [1, 0]},
            'k': {'(': [1, 0]},
            'l': {')': [1, 0]},
            'z': {'*': [1, 0]},
            'x': {'"': [1, 0]},
            'c': {"'": [1, 0], 'ç': [1, 1]},
            'v': {':': [1, 0]},
            'b': {';': [1, 0]},
            'n': {'!': [1, 0], 'ñ': [1, 1]},
            ',': {'setting': [1, 0]},
            '.': {'!': [1, -1], '#': [1, -2], '?': [1, 1], ':': [2, -1], '-': [2, -1], '@': [2, 1]}
        }
        # 一般键盘数字
        self.normal_number = {
            '1': 'q', '2': 'w', '3': 'e', '4': 'r', '5': 't', '6': 'y', '7': 'u', '8': 'i', '9': 'o', '0': 'p',
            '@': 'a', '#': 's', '$': 'd', '%': 'f', '&': 'g', '-': 'h', '+': 'j', '(': 'k', ')': 'l',
            'symbol': 'shift', '*': 'z', '"': 'x', "'": 'c', ':': 'v', ';': 'b', '!': 'n', '?': 'm', 'delete': 'delete',
            'normal': [4, 1], '_': [4, 2], '/': [4, 3], ',': [4, 4], ' ': [4, 5], '.': [4, 6], 'next': [4, 7]
        }
        # 一般键盘数字pop
        self.normal_number_pop = {
            '1': {'¹': [1, 0], '½': [1, 1], '⅓': [1, 2], '¼': [1, 3], '⅛': [1, 4]},
            '2': {'²': [1, 0], '⅔': [1, 1]},
            '3': {'³': [1, 0], '⅜': [1, -1], '¾': [1, 1]},
            '4': {'⁴': [1, 0]},
            '7': {'⅞': [1, 0]},
            '0': {'ⁿ': [1, 0], '∅': [1, -1]},
            '$': {'¢': [1, 0], '€': [1, -1], '₱': [1, -2], '£': [1, 1], '¥': [1, 2]},
            '-': {'_': [1, 0], '—': [1, -1], '–': [1, 1], '·': [1, 2]},
            '(': {'<': [1, -1], '{': [1, 0], '[': [1, 1]},
            ')': {']': [1, 0], '}': [1, -1], '>': [1, -2]},
            '*': {'†': [1 - 1], '★': [1, 0], '‡': [1, 1]},
            '"': {'”': [1, 0], '“': [1, -1], '„': [1, -2], '«': [1, 1], '»': [1, 2]},
            "'": {"’": [1, 0], "‘": [1, -1], "‚": [1, -2], "‹": [1, 1], "›": [1, 2]},
            '.': {'…': [1, 0]}

        }
        # 一般键盘符号
        self.normal_symbol = {
            '~': '1', '`': '2', '|': '3', '•': '4', '√': '5', 'Π': '6', '÷': '7', '×': '8', '¶': '9', '∆': '0',
            '£': '@', '¢': '#', '€': '$', '¥': '%', '^': '&', '°': '-', '=': '+', '{': '(', '}': ')',
            'number': 'symbol', '\\': '*', '©': '"', '®': "'", '™': ':', '℅': ';', '[': '!', ']': '?',
            'delete': 'delete',
            'normal': 'normal', '<': '_', '>': '/', ',': ',', ' ': ' ', '.': '.', 'next': 'next'
        }
        # 一般键盘符号pop
        self.normal_symbol_pop = {
            '•': {'♪': [1, 0], '♠': [1, -1], '♣': [1, -2], '♥': [1, 1], '♦': [1, 2]},
            'Π': {'π': [1, 0]},
            '¶': {'§': [1, 0]},
            '^': {'↑': [1, 0], '←': [1, -1], '↓': [1, 1], '→': [1, 2]},
            '=': {'≠': [1, 0], '∞': [1, -1], '≈': [1, 1]},
            '<': {'≤': [1, 0], '‹': [1, -1], '«': [1, 1]},
            '>': {'≥': [1, 0], '›': [1, -1], '»': [1, 1]},
            '.': {'…': [1, 0]}
        }
        # 数字输入
        self.number_decimal = {
            '1': [1, 1], '2': [1, 2], '3': [1, 3], '-': [1, 4],
            '4': [2, 1], '5': [2, 2], '6': [2, 3], ',': [2, 4],
            '7': [3, 1], '8': [3, 2], '9': [3, 3], 'delete': [3, 4],
            ' ': [4, 1], '0': [4, 2], '.': [4, 3], 'ente': [4, 4]
        }
        # 数字密码
        self.number_password = {
            '1': [1, 1], '2': [1, 2], '3': [1, 3],
            '4': [2, 1], '5': [2, 2], '6': [2, 3],
            '7': [3, 1], '8': [3, 2], '9': [3, 3],
            'delete': [4, 1], '0': [4, 2], 'ente': [4, 3]
        }
        # 表情
        self.emoji_kb = {
            'normal_key': ['0', '1'], 'emoji': ['0', '2'], 'sticke': ['0', '3'], 'gif': ['0', '4'],
            'emoticon': ['0', '5'],
            'delete': ['0', '6'],
        }
        # mainmenu键位
        self.main_menu = {'theme': [1, 1], 'coolfont': [1, 2], 'style': [1, 3], 'selecto': [1, 4],
                          'clipboard': [2, 1], 'custom': [2, 2], 'layout': [2, 3],
                          'size': [3, 1], 'settings': [3, 2], 'likeus': [3, 3], 'vibrate': [3, 4],
                          'stickerpop': [4, 1]}
        # select按键
        self.select = {
            'up': [0, 1], 'down': [0, 2], 'left': [0, 3], 'right': [0, 4]
        }
        # sticker2
        self.sticker2 = {
            'add': [0, 1], 'close': [0, 2]
        }

    # 获取分辨率参数或者手机应用的最高
    def density(self):
        if self.device_config is 'none':
            density = 'adb  shell dumpsys window displays '
        else:
            density = 'adb  -s %s shell dumpsys window displays' % self.device_config
        # density_result = subprocess.Popen(os.open(density), stdout=subprocess.PIPE,shell=False).stdout.read()
        density_result = os.popen(density).read()
        p = re.findall('...dpi', str(density_result))[0].split('dpi')[0]
        try:
            app = re.findall('app=.........', str(density_result))[0].split('x')[1]
            app = int(app)
        except:
            app = re.findall('app=.......', str(density_result))[0].split('x')[1]
            app = int(app)
        # print(p)
        # print(app)
        # print(int(p) / int(160))
        return {'density': int(p) / int(160), 'app': int(app)}

        # 向上滑动屏幕

    # 根据高度上滑屏幕
    def up_swip(self, row, row_line, u_height):
        # 滑动有一个预准备动作这个值还不准确
        print('滑动屏幕')
        print('@' + str(u_height))
        select_begin_y = self.top_y + float(self.density()['density']) * 40
        ss_x = self.phone_width / 2
        ss_y = select_begin_y + (self.phone_height - select_begin_y) / 2
        print(float(self.density()['density']))
        for i in range(int(row) - int(row_line)):
            self.driver.swipe(start_x=ss_x, start_y=ss_y, end_x=ss_x,
                              end_y=ss_y - u_height - float(self.density()['density']) * 8)
            time.sleep(1)

            # 图像识别文字后根据文字数量返回x和width

    # 根据坐标宽高截图返回截图文字的的宽和坐标
    def orc_location(self, x, y, width, height, set_lang='eng'):
        orc_location_result = {}
        self.AppiumExtend.get_screenshot_by_location(x, y, width, height).write_to_file(PATH + '/../temp', 'top_tab')
        text_result = ocr_text(PATH + '/../temp/top_tab.png', set_lang)
        if '\n' in text_result:
            text_result = text_result.replace('\n', ' ')
        text = text_result.split(' ')
        for i in text:
            if i == '':
                text.remove(i)
        print(text_result)
        print(text)
        button = {}
        # 获取每个字所在位置的值
        for i in range(0, len(text)):
            button[i] = [text[i], len(text[i])]
        a = 0
        for e in button:
            a += button[e][1]
        unit_length = 1080 / a
        print(unit_length)
        orc_x = x
        for f in range(0, len(text)):
            orc_width = unit_length * button[f][1]
            orc_location_result[f] = {'x': orc_x, 'y': y, 'width': orc_width, 'height': height}
            orc_x += unit_length * button[f][1]
        return orc_location_result

    # 获取的坐标统一为左上角
    # qwerty键盘的坐标
    def normal_key_location(self, row_s, line_s, number=False, select=False):
        # print('####')
        global x, y, width, height
        row = int(row_s)
        line = int(line_s)
        density = self.density()
        height_row1 = 40 * float(density['density'])
        # height_row1 = 40 * 3
        # 高度计算
        width = self.phone_width * 0.1
        print(width)
        # 是否开启数字键
        if number == False:
            line_no = 4
            row_d = 2
        else:
            line_no = 5
            row_d = 1
        if select == False:
            select_height = 0
        else:
            select_height = 50 * float(density['density'])
        height = (int(density['app']) - select_height - self.top_y - height_row1) / line_no
        if line == 1:
            x = 0
        if row == 0:
            y = self.top_y
            height = height_row1
            width = 50 * float(density['density'])
            50 * float(density['density'])
            if line == 1:
                x = float(density['density']) * 10
                height = 40 * float(density['density'])
                width = 40 * float(density['density'])
            if line == 4:
                width = 55 * float(density['density'])
                x = self.phone_width - width
            if line == 2:
                x = 60 * float(density['density'])
            if line == 0:
                width = 40 * float(density['density'])
                x = 100 * float(density['density'])
        else:
            y = self.top_y + height_row1 + height * (row - row_d)
        if row == 2 or row == 1:
            x = self.phone_width * 0.1 * (line - 1)
        elif row == 3:
            if line == 1:
                x = self.phone_width * 0.05
            else:
                x = self.phone_width * (0.05 + 0.1 * (line - 1))
        elif row == 4:
            x = self.phone_width * (0.15 + 0.1 * (line - 2))
            if line == 1:
                width = self.phone_width * 0.15
            elif line == 8:
                width = self.phone_width - x
        elif row == 5:
            if line == 1:
                width = self.phone_width * 0.15
            elif line == 2 or line == 3 or line == 4:
                x = self.phone_width * 0.15 + self.phone_width * 0.1 * (line - 2)
                if line == 4:
                    width = self.phone_width * 0.4
            elif line == 5:
                x = self.phone_width * 0.15 + self.phone_width * 0.1 * 2 + self.phone_width * 0.4
            elif line == 6:
                x = self.phone_width * 0.15 + self.phone_width * 0.1 * 3 + self.phone_width * 0.4

        return {'x': int(x), 'y': int(y), 'width': int(width), 'height': int(height)}

        # 最下方表情选择

    # 键盘pop
    def key_pop_location(self, long_pass_key, key, keyboard_type='normal', number=False, select=False):
        long_pass_key_loaction = self.keyboard_reader(long_pass_key, keyboard_type, number=number, select=select)
        long_pass_key_x = long_pass_key_loaction['x']
        long_pass_key_y = long_pass_key_loaction['y']
        key_width = long_pass_key_loaction['width']
        key_height = long_pass_key_loaction['height']
        if keyboard_type == 'normal':
            key_location = self.normal_keyboard_pop[long_pass_key][key]
        elif keyboard_type == 'normal_number':
            key_location = self.normal_number_pop[long_pass_key][key]
        elif keyboard_type == 'normal_symbol':
            key_location = self.normal_symbol_pop[long_pass_key][key]
        key_row = key_location[0]
        key_line = key_location[1]
        # print(key_row, key_line)
        relative_position_x = key_line * key_width
        # 高度移动了50%就足够了
        relative_position_y = -key_row * key_height / 2
        key_x = long_pass_key_x + relative_position_x
        key_y = long_pass_key_y + relative_position_y
        return {'x': key_x, 'y': key_y, 'width': key_width, 'height': key_height,
                'relative_position_x': relative_position_x, 'relative_position_y': relative_position_y}

    # 一般键盘数字
    def normal_number_location(self, key, select=False):
        to_key = self.normal_number[key]
        try:
            loaction = self.keyboard_reader(to_key, keyboard_type='normal', select=select)
        except:
            if select == False:
                select_height = 0
            else:
                select_height = 50 * float(self.density()['density'])
            row = int(to_key[0])
            line = int(to_key[1])
            select_begin_y = self.top_y + float(self.density()['density']) * 40
            height_nn = (int(self.density()['app']) - select_height - select_begin_y) / 4
            y_nn = select_begin_y + 3 * height_nn
            if line == 1:
                x_nn = 0
                width_nn = self.phone_width * 0.15
            elif line == 2 or line == 3 or line == 4 or line == 5:
                x_nn = self.phone_width * 0.15 + self.phone_width * 0.1 * (line - 2)
                width_nn = 0.1 * self.phone_width
                if line == 5:
                    width_nn = 0.3 * self.phone_width
            elif line == 6:
                x_nn = self.phone_width * 0.15 + self.phone_width * 0.1 * 3 + self.phone_width * 0.3
                width_nn = 0.1 * self.phone_width
            elif line == 7:
                x_nn = self.phone_width * 0.15 + self.phone_width * 0.1 * 4 + self.phone_width * 0.3
                width_nn = self.phone_width - x_nn
            loaction = {'x': x_nn, 'y': y_nn, 'width': width_nn, 'height': height_nn}
        return loaction

    # 一般符号键盘
    def normal_symbol_location(self, key, select=False):
        to_key = self.normal_symbol[key]
        loaction = self.keyboard_reader(to_key, keyboard_type='normal_number', select=select)
        return loaction

    # number_decimal键盘
    def number_decimal_loaction(self, row_nd, line_nd, select=False):
        if select == False:
            select_height = 0
        else:
            select_height = 50 * float(self.density()['density'])
        row = int(row_nd)
        line = int(line_nd)
        density = self.density()
        sys_h = 40 * float(density['density'])
        y_begin = self.top_y + sys_h
        height_nd = (int(self.density()['app']) - select_height - self.top_y - sys_h) / 4
        y_nd = y_begin + height_nd * (row - 1)
        width_nd = 0.26667 * self.phone_width
        x_nd = 0 + width_nd * (line - 1)
        if line == 4:
            width_nd = self.phone_width - width_nd * 3
        return {'x': int(x_nd), 'y': int(y_nd), 'width': int(width_nd), 'height': int(height_nd)}

    # number_password
    def number_password_location(self, row_pw, line_pw, select=False):
        if select == False:
            select_height = 0
        else:
            select_height = 50 * float(self.density()['density'])
        row = int(row_pw)
        line = int(line_pw)
        density = self.density()
        sys_h = 40 * float(density['density'])
        y_begin = self.top_y + sys_h
        height_pw = (int(self.density()['app']) - select_height - self.top_y - sys_h) / 4
        width_pw = 0.26667 * self.phone_width
        x_pw = 0.1 * self.phone_width + width_pw * (line - 1)
        y_pw = y_begin + height_pw * (row - 1)
        return {'x': int(x_pw), 'y': int(y_pw), 'width': int(width_pw), 'height': int(height_pw)}

    # 表情大类型选择
    def emoji_key_locaton(self, rows, lines):
        print("****")
        global c_x, c_y, c_width, c_height, select_begin_y
        row = int(rows)
        try:
            line = int(lines)
        except:
            line = lines
        dens = self.density()
        select_begin_y = self.top_y + float(dens['density']) * 40
        c_height = float(dens['density']) * 40
        if row == 0:
            print(dens['app'])
            c_y = int(dens['app']) - float(dens['density']) * 40
            print(c_y)
            c_x = float(dens['density']) * 48 + float(dens['density']) * 53 * (line - 2)
            if line == 1 or line == 6:
                c_width = float(dens['density']) * 48
                c_x = 0
            else:
                c_width = float(dens['density']) * 53
            if line == 6:
                c_x = self.phone_width - float(dens['density']) * 48
        return {'x': int(c_x), 'y': int(c_y), 'width': int(c_width), 'height': int(c_height)}

        # 对应emoji个中类型选择

    # 表情小类型选择
    def emoji_class(self, emoji, s_no):
        global ec_x, ec_y, ec_width, ec_height, move
        no = s_no
        dens = self.density()
        select_begin_y = self.top_y + float(dens['density']) * 40
        if emoji == 'emoji':
            # serach
            if no == 1:
                ec_width = 14.2857 * 0.01 * self.phone_width
                ec_height = float(dens['density']) * 40
                ec_y = self.top_y
                ec_x = 0
            else:
                print('#')
                ec_width = float(dens['density']) * 40
                ec_height = ec_width
                ec_y = self.top_y
                ec_x = 14.2857 * 0.01 * self.phone_width + ec_width * (no - 2)
        if emoji == 'sticke':
            ec_width = float(dens['density']) * 44
            ec_height = float(dens['density']) * 40
            ec_x = ec_width * (no - 1)
            ec_y = self.top_y
            if no > 8:
                for i in range(no - 8):
                    # 预备动作大概是10这个可能会影响适配
                    self.driver.swipe(start_x=self.phone_width / 2, start_y=self.top_y + 10,
                                      end_x=self.phone_width / 2 - ec_width - float(dens['density']) * 8,
                                      end_y=self.top_y + 10)
                    time.sleep(0.5)
                ec_x = ec_width * 8
        if emoji == 'gif' or emoji == 'emoticon':
            no = no - 1
            ec_y = self.top_y
            ec_height = float(dens['density']) * 40
            move = []
            if no > 3:
                width = self.ocr_location(0, self.top_y, 1080, ec_height)
                for i in range(0, 4):
                    move.append(width[i]['width'])
                print(move)
                for e in move:
                    print(e)
                    # 预备动作10
                    # self.driver.swipe(start_x=self.phone_width, start_y=self.top_y + 20, end_x=self.phone_width-e, end_y=self.top_y + 20)
                    TouchAction(self.driver).long_press(x=self.phone_width / 2, y=self.top_y + 20).move_to(
                        x=self.phone_width / 2 - e - float(dens['density']) * 8, y=self.top_y + 20).release().perform()
                x_width = self.ocr_location(0, self.top_y, 1080, ec_height)[no - 4]
                print(no - 4)
                ec_x = x_width['x']
                ec_width = x_width['width']
            else:
                x_width = self.ocr_location(0, self.top_y, 1080, ec_height)[no]
                ec_x = x_width['x']
                ec_width = x_width['width']
        # self.AppiumExtend.get_screenshot_by_location(int(ec_x), int(ec_y), int(ec_width),
        #                                              int(ec_height)).write_to_file(
        #     './', 'class')
        return {'x': int(ec_x), 'y': int(ec_y), 'width': int(ec_width), 'height': int(ec_height)}

    # 表情选择
    def emoji(self, e_class, s_row, s_line):
        print('&&&&&&')
        global s_x, s_y, s_width, s_height
        row = s_row
        line = s_line
        dens = self.density()
        select_begin_y = self.top_y + float(dens['density']) * 40
        if e_class == 'emoji':
            s_width = 14.2857 * 0.01 * self.phone_width
            s_height = s_width
            s_x = s_width * (int(line) - 1)
            if int(row) > 3:
                # 向上滑动屏幕
                self.up_swip(row, 3, s_height)
                time.sleep(5)
                s_y = select_begin_y + 2 * s_width
            else:
                s_y = select_begin_y + (row - 1) * s_width
        if e_class == 'sticke':
            s_width = self.phone_width / 4
            s_height = s_width * 4 / 5
            # s_height = (self.density()['app'] - select_begin_y) / 2.5
            s_x = s_width * (line - 1)
            s_y = select_begin_y + s_height * (row - 1)
            if row > 2:
                self.up_swip(row, 2, s_height)
                s_y = select_begin_y + s_height
        if e_class == 'gif':
            s_width = self.phone_width / 2
            s_height = s_width * 11 / 18
            s_x = 0
            s_y = select_begin_y
            if line >= 2:
                s_x = s_width
            if row > 1:
                self.up_swip(row, 1, s_height)
        if e_class == 'emoticon':
            s_width = self.phone_width / 2
            s_height = float(dens['density']) * 40
            s_y = select_begin_y + s_height * (row - 1)
            if line == 1:
                s_x = 0
            else:
                s_x = s_width
            if row > 4:
                self.up_swip(row, 4, s_height)
                s_y = select_begin_y + s_height * 3
        return {'x': int(s_x), 'y': int(s_y), 'width': int(s_width), 'height': int(s_height)}

    # pop按键选择
    def pop_select(self, long_pass_key, key, keyboard_type='normal', number=False, select=False):
        long_pass_key_loaction = self.keyboard_reader(long_pass_key, keyboard_type, number=number, select=select)
        long_pass_key_x = long_pass_key_loaction['x']
        long_pass_key_y = long_pass_key_loaction['y']
        key_location = self.key_pop_location(long_pass_key, key, keyboard_type)
        relative_position_x = key_location['relative_position_x']
        relative_position_y = key_location['relative_position_y']
        # 选择操作
        TouchAction(self.driver).long_press(x=long_pass_key_x + 12, y=long_pass_key_y + 22).wait(2) \
            .move_to(x=relative_position_x + 12, y=relative_position_y + 22). \
            wait(0.5).release().perform()
        time.sleep(0.5)

    # 字典
    def dictionary(self, no, row, line):
        begin_y = self.top_y - 6 * float(self.density()['density'])
        begin_x = 10 * float(self.density()['density'])
        dic_all_wind = self.phone_width - 10 * float(self.density()['density'])
        dic_height = 32 * float(self.density()['density'])
        dic_wind = dic_all_wind / no
        dic_x = begin_x + row * dic_wind
        dic_y = begin_y - dic_height * line
        return {'x': dic_x, 'y': dic_y, 'width': dic_wind, 'height': dic_height}

    def click_dictionary(self, no, row, line):
        self.location_click(self.phone_width / 2, self.top_y, 'long_pass')
        location = self.dictionary(no, row, line)
        self.location_click(location['x'], location['y'])

    # 键盘坐标读取
    def keyboard_reader(self, key, keyboard_type='normal', number=False, select=False):
        if keyboard_type == 'normal':
            layout = self.keyboard_qwerty[key]
            row = layout[0]
            line = layout[1]
            loaction = self.normal_key_location(row, line, number, select)
        elif keyboard_type == 'emoji':
            layout = self.emoji_kb[key]
            row = layout[0]
            line = layout[1]
            loaction = self.emoji_key_locaton(row, line)
        elif keyboard_type == 'number_decimal':
            layout = self.number_decimal[key]
            row = layout[0]
            line = layout[1]
            loaction = self.number_decimal_loaction(row, line, select)
        elif keyboard_type == 'number_password':
            layout = self.number_password[key]
            row = layout[0]
            line = layout[1]
            loaction = self.number_password_location(row, line, select)
        elif keyboard_type == 'normal_number':
            loaction = self.normal_number_location(key, select)
        elif keyboard_type == 'normal_symbol':
            loaction = self.normal_symbol_location(key, select)

        print(key, loaction)
        return loaction

    # 输入内容解读
    def string_reader(self, text):
        keys = []
        for i in text:
            keys.append(i)
        return keys

    # 坐标点击
    def location_click(self, l_x, l_y, input_type='click'):
        if input_type == 'click':
            TouchAction(self.driver).tap(x=l_x + 12, y=l_y + 32).wait(0.1).perform()
        else:
            TouchAction(self.driver).long_press(x=l_x + 12, y=l_y + 32).wait(1).perform()
        time.sleep(0.5)

    # 点击键盘输入按键（normal,number_decimal,number_password)
    def send_input(self, text, keyboard_type='normal', inputtype='click', number=False, select=False):
        send_content = self.string_reader(text)
        # print(send_content)
        if text in ['system', 'theme', 'sticker2', 'stop', 'delete', 'emoji', 'ente', 'number', 'normal_key',
                    'messenge', 'shift',
                    # emoji
                    'emoji', 'sticke', 'gif', 'emoticon', 'delete',
                    # normal_number
                    'symbol', 'normal', 'next',
                    # normal_symbol
                    'number', 'normal']:
            locton_size = self.keyboard_reader(text, keyboard_type, number, select)
            self.location_click(int(locton_size['x']), int(locton_size['y']), inputtype)
        else:
            for i in send_content:
                locton_size = self.keyboard_reader(i, keyboard_type, number, select)
                self.location_click(int(locton_size['x']), int(locton_size['y']), inputtype)
        return locton_size  # (x,y,width,height)

    # mainmenu页面点击
    # def main_menu_click(self, button):
    #     global m_x, m_y
    #     loaction = self.main_menu[button]
    #     row = int(loaction[0])
    #     line = int(loaction[1])
    #     m_x = self.phone_width * (line - 1) / 4
    #     dens = self.density()
    #     select_begin_y = self.top_y + float(dens['density']) * 40
    #     pic = [0, select_begin_y, self.phone_width / 4, int(dens['app']) - select_begin_y]
    #     while True:
    #         if row == 1:
    #             m_y = select_begin_y
    #             break
    #         self.driver.swipe(start_x=self.phone_width / 2,
    #                           start_y=(select_begin_y + (int(dens['app']) - select_begin_y) / 2),
    #                           end_x=self.phone_width / 2,
    #                           end_y=select_begin_y)
    #         if row == 2:
    #             self.AppiumExtend.get_screenshot_by_location(pic[0], pic[1], pic[2], pic[3]).write_to_file(path + '/temp',
    #                                                                                                        'menu')
    #             text = ocr_text(path + '/temp/menu.png', 'eng')
    #             if 'Theme' not in text:
    #                 m_y = select_begin_y
    #                 break
    #         elif row == 3:
    #             self.AppiumExtend.get_screenshot_by_location(pic[0], pic[1], pic[2], pic[3]).write_to_file(path + '/temp',
    #                                                                                                        'menu')
    #             text = ocr_text(path + '/temp/menu.png', 'eng')
    #             if 'clipBoard' not in text:
    #                 m_y = select_begin_y
    #                 break
    #         elif row == 3:
    #             self.AppiumExtend.get_screenshot_by_location(pic[0], pic[1], pic[2], pic[3]).write_to_file(path + '/temp',
    #                                                                                                        'menu')
    #             text = ocr_text(path + '/temp/menu.png', 'eng')
    #             if 'clipBoard' not in text:
    #                 m_y = select_begin_y + (int(dens['app']) - select_begin_y) / 2
    #                 break
    #     self.location_click(int(m_x), int(m_y))
    #     time.sleep(0.5)

    def main_menu_select(self, button):
        select_begin_y = self.top_y + float(self.density()['density']) * 40
        row = int(self.main_menu[button][0])
        line = int(self.main_menu[button][1])
        main_height = float(self.density()['density']) * 88
        main_width = self.phone_width / 4
        main_x = 0 + main_width * (line - 1)
        main_y = select_begin_y + main_height * (row - 1)
        # self.location_click(main_x, main_y)
        return {'x': int(main_x), 'y': int(main_y), 'width': int(main_width), 'height': int(main_height)}

    def main_menu_click(self, button):
        location = self.main_menu_select(button)
        self.location_click(location['x'], location['y'])

    # 选择表情小类型
    def select_emoji_class(self, eomjy, s_no):
        locton_size = self.emoji_class(eomjy, s_no)
        print(locton_size)
        # TouchAction(self.driver).tap(x=int(locton_size['x'] + 12), y=int(locton_size['y'] + 12)).wait(0.1).perform()
        self.location_click(int(locton_size['x']), int(locton_size['y']))
        time.sleep(0.5)
        return locton_size

    # 点选择表情
    def select_emoji(self, e_class, s_row, s_line):
        locton_size = self.emoji(e_class, s_row, s_line)
        print(locton_size)
        # TouchAction(self.driver).tap(x=int(locton_size['x'] + 12), y=int(locton_size['y'] + 12)).wait(0.1).perform()
        self.location_click(int(locton_size['x']), int(locton_size['y']))
        time.sleep(0.5)
        return locton_size

    # sticker2键盘
    def sticker2_select(self, key, *args):
        if key == 'add':
            s_x = 0
            s_y = self.top_y
            s_width = 40 * float(self.density()['density'])
            s_height = 40 * float(self.density()['density'])
        elif key == 'close':
            s_y = self.top_y
            s_width = 40 * float(self.density()['density'])
            s_height = 40 * float(self.density()['density'])
            s_x = self.phone_width - s_width
        elif key == 'class':
            s_width = 40 * float(self.density()['density'])
            s_height = 40 * float(self.density()['density'])
            s_x = int(args[0]) * s_width
            if int(args[0]) > 7:
                for i in range(int(args[0]) - 7):
                    self.driver.swipe(start_x=self.phone_width / 2, start_y=self.top_y + 10,
                                      end_x=self.phone_width / 2 + s_width + 8 * float(self.density()['density']),
                                      end_y=self.top_y + 10)
                    time.sleep(0.5)
                s_x = 7 * s_width
            s_y = self.top_y
        else:
            # 在选择stick的时候要填写两个值row,line
            print(args[0])
            if args[0] == 1:
                s_y = self.top_y + 40 * float(self.density()['density'])
                s_x = (int(args[1]) - 1) * (self.phone_width / 4)
                s_width = self.phone_width / 4
                s_height = 90 * float(self.density()['density'])
            elif args[0] == 2:
                s_y = self.top_y + 40 * float(self.density()['density']) + 90 * float(self.density()['density'])
                s_x = (int(args[1]) - 1) * (self.phone_width / 4)
                s_width = self.phone_width / 4
                s_height = 90 * float(self.density()['density'])
            else:
                s_height = 90 * float(self.density()['density'])
                self.up_swip(int(args[0]), 2, s_height)
                s_y = self.top_y + 40 * float(self.density()['density'])
                s_x = (int(args[1]) - 1) * (self.phone_width / 4)
                s_width = self.phone_width / 4
        return {'x': s_x, 'y': s_y, 'width': s_width, 'height': s_height}

    # sticker2点击
    def sticker2_click(self, key, *args):
        loaction = self.sticker2_select(key, *args)
        self.location_click(loaction['x'], loaction['y'])

    # 主题选择/表情风格
    def select_theme(self, s_row, s_line):
        global st_x, st_y
        row = int(s_row)
        line = int(s_line)
        dens = self.density()
        select_begin_y = self.top_y + float(dens['density']) * 40
        if line == 1:
            st_x = self.phone_width / 4
        else:
            st_x = self.phone_width * 3 / 4
        st_y = select_begin_y + (self.phone_height - select_begin_y) / 4
        if row == 1:
            pass

        else:
            for i in range(row - 1):
                self.driver.swipe(start_x=self.phone_width / 2, start_y=select_begin_y, end_x=self.phone_width / 2,
                                  end_y=select_begin_y - (self.phone_height - select_begin_y) / 2)
        print(st_x, st_y)
        time.sleep(2)
        # TouchAction(self.driver).tap(x=int(st_x) + 12, y=int(st_y) + 22).wait(0.1).perform()
        self.location_click(int(st_x), int(st_y))
        time.sleep(1)

    # 选择select按键
    def select_select_key(self, key, input_type='click'):
        location = self.select[key]
        row = location[0]
        line = location[1]
        select_width = self.phone_width / 4
        select_height = 50 * float(self.density()['density'])
        select_x = 0 + select_width * (line - 1)
        select_y = self.density()['app'] - select_height
        self.location_click(select_x, select_y, input_type=input_type)
        return {'x': select_x, 'y': select_y, 'width': select_width, 'height': select_height}

    # 选词栏检查
    def select_word_check(self, word, set_lang='eng'):
        select_location = {"x": 0, "y": int(self.top_y), 'width': int(self.phone_width),
                           'height': int(self.density()['density'] * 40)}
        self.AppiumExtend.get_screenshot_by_location(select_location['x'], select_location['y'],
                                                     select_location['width'], select_location['height']).write_to_file(
            PATH + '/../temp', 'select_word')
        text_result = ocr_text(PATH + '/../temp/select_word.png', set_lang)
        print(text_result)
        if word in text_result:
            return True
        else:
            return False

    # 图片中有是否有文字
    def word_in_pic(self, x, y, width, height, word, set_lang='eng'):
        select_location = {"x": x, "y": y, 'width': width, 'height': height}
        self.AppiumExtend.get_screenshot_by_location(select_location['x'], select_location['y'],
                                                     select_location['width'], select_location['height']).write_to_file(
            PATH + '/../temp', 'pic_word')
        text_result = ocr_text(PATH + '/../temp/pic_word.png', set_lang)
        print(text_result)
        if word in text_result:
            return True
        else:
            return False

    # 滑动输入
    def sliding_input(self, text, number=False, select=False):
        key = []
        send_content = self.string_reader(text)

        func_call_times = len(send_content)
        for i in range(func_call_times):
            locton_size = self.keyboard_reader(send_content[i], number=number, select=select)
            key.append(locton_size)

        touch_action = TouchAction(self.driver).press(x=key[0]['x'] + 12, y=key[0]['y'] + 12)
        # 下面touch这个使用类型记住
        for i in range(func_call_times - 1):
            touch_action = touch_action.move_to(x=key[i + 1]['x'] - key[i]['x'] + 12,
                                                y=key[i + 1]['y'] - key[i]['y'] + 12)
        touch_action.wait(0.5).release().perform()

    # 坐标位置滑动
    def swip_location(self, x, y, width, height):
        TouchAction(self.driver).long_press(x=x + width / 2, y=y + height / 2).move_to(x=x + width,
                                                                                       y=y + height / 2).release().perform()

    # 元素截图
    def get_keyboard_picture(self, kb_x, kb_y, kb_width, kb_height, pic_name):
        name_p = pic_name + time.strftime('%Y%m%d%H%M%S')
        try:
            os.path.exists(PATH + '/../temp') == False
            os.mkdir(PATH + '/../temp')
        except:
            pass
        self.AppiumExtend.get_screenshot_by_location(kb_x, kb_y, kb_width, kb_height).write_to_file(PATH + '/../temp',
                                                                                                    name_p)
        load = self.AppiumExtend.load_image(PATH + '/../temp/%s.png' % name_p)
        return {'load': load, 'pic': name_p}

    # 图片是否一致
    def keyboard_same(self, x, y, width, height, load, diff=1):
        self.AppiumExtend.get_screenshot_by_location(x, y, width, height).write_to_file(PATH + '/../temp',
                                                                                        'keyborad_same')
        same_result = self.AppiumExtend.get_screenshot_by_location(x, y, width, height).same_as(load['load'], 0)
        print(same_result)
        if same_result == False:
            if diff == 1:
                try:
                    os.path.exists(PATH + '/../diff_pic') == False
                    os.mkdir(PATH + '/../diff_pic')
                except:
                    pass
                name_p = 'diff' + time.strftime('%Y%m%d%H%M%S')
                compare_images(PATH + '/../temp/%s.png' % load['pic'], PATH + '/../temp/keyborad_same.png',
                               PATH + '/../diff_pic/%s.jpg' % name_p)
                print('图片不一致，差异图%s' % name_p)
            else:
                print('不做图片diff')
        return same_result

    def checkpoint_pic(self, kb_x, kb_y, kb_width, kb_height, pic_name):
        name_p = pic_name + time.strftime('%Y%m%d%H%M%S')
        try:
            os.path.exists(PATH + '/../checkpoint_record_data') == False
            os.mkdir(PATH + '/../checkpoint_record_data')
        except:
            pass
        self.AppiumExtend.get_screenshot_by_location(kb_x, kb_y, kb_width, kb_height).write_to_file(
            PATH + '/../checkpoint_record_data', name_p)
        return 'keyboard_regression/checkpoint_record_data/' + name_p + '.png'

    def checkpoint(self, table_name, kb_x, kb_y, kb_width, kb_height, pic_name):
        create_table(table_name)
        no = query_the_fist(table_name)
        print(no)
        # 图片地址
        pic = self.checkpoint_pic(kb_x, kb_y, kb_width, kb_height, pic_name)
        view_date = time.strftime('%Y%m%d%H%M%S')
        date = time.time()
        if no == True:
            pics = query_Initial_last(table_name)
            i_pic = self.AppiumExtend.load_image(pics['Initial'])
            l_pic = self.AppiumExtend.load_image(pics['last'])
            now_pic = self.AppiumExtend.get_screenshot_by_location(kb_x, kb_y, kb_width, kb_height)
            i_c = now_pic.similarity_rate(i_pic)
            l_c = now_pic.similarity_rate(l_pic)
            insert_table(table_name, view_date=view_date, date=date, pic=pic, Initial_pic=i_c, last_pic=l_c)
        else:
            print(table_name)
            print(view_date)
            print(date)
            print(pic)
            insert_table(table_name, view_date=view_date, date=date, pic=pic, Initial_pic=0, last_pic=0)

    # 获取截取图片上的文字
    def pic_text(self, pic, set_lang='eng'):
        text = ocr_text(PATH + '/../temp/%s.png' % pic['pic'], set_lang)
        return text

    def orc_location_text(self, x, y, width, height, set_lang='eng'):
        orc = ocr_text(PATH + '/../temp/%s.png' % self.get_keyboard_picture(x, y, width, height, 'orc_location')['pic'],
                       set_lang)
        print(orc)
        return orc
