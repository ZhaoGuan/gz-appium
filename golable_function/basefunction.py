# -*- coding: utf-8 -*-
# __author__ = 'Gz'

import os
import random
import re
import subprocess
import time
import unittest

from appium.webdriver.common.touch_action import TouchAction

from golable_function.extend import AppiumExtend

from golable_function.checkpoint_record import *
import os

PATH = os.path.dirname(os.path.abspath(__file__))


class BaseFunction(object):
    def __init__(self, tester, driver):
        unittest.TestCase()
        self.tester = tester
        self.driver = driver
        self.extend = AppiumExtend(driver)

    # 结果截图
    def result_picture(self, result_name="结果"):
        try:
            os.path.exists(PATH + '/../result_picture')
            os.mkdir(PATH + '/../result_picture')
        except:
            pass
        result_time = time.strftime('%Y%m%d%H%M%S')
        result_done_name = result_name  # + result_time
        self.driver.get_screenshot_as_file("PATH/result_picture/%s.png" % result_done_name)

    # 错误截图
    def fail_picture(self, times=0):
        # 如果找不到元素进行截图，截图是按照当时时间来命名
        # 判断如果没有指定失败图片且，同文件夹的名字为Fail_picture的文件夹新建一个
        try:
            os.path.exists(PATH + '/../fail_picture')
            os.mkdir(PATH + '/../fail_picture')
        except:
            pass
        # 设置时间格式
        ISOTIMEFORMAT = '%Y%m%d_%X'
        localtime = str(time.strftime(ISOTIMEFORMAT, time.localtime())).replace(':', '')
        print('未找到要点击的元素页面截图为:', localtime)
        # 以时间命名截屏
        self.driver.get_screenshot_as_file(PATH + '/../fail_picture/' + localtime + '.png')
        if times != 0:
            print('网络延迟，超过', times, '秒')

    # 抓元素
    def check_find_element(self, how, element):
        global find_element
        if how == 'id':
            find_element = self.driver.find_element_by_id(element)
        elif how == 'name':
            a = "//*[@text='%s']" % element
            find_element = self.driver.find_element_by_xpath(a)
        elif how == 'class':
            find_element = self.driver.find_element_by_class_name(element)
        elif how == 'xpath':
            find_element = self.driver.find_element_by_xpath(element)
        elif how == 'classes':
            element = element.split('[')
            find_element = self.driver.find_elements_by_class_name(element[0])
            find_element = find_element[int(element[1].split(']')[0])]
        elif how == 'ides':
            element = element.split('[')
            find_element = self.driver.find_elements_by_id(element[0])
            find_element = find_element[int(element[1].split(']')[0])]
        return find_element

    # 等待元素超过多久报错,默认10S
    def wait_element(self, how, element, wait_time=10, fail_pic=True):
        wait_element = None
        dead_line = 0
        while True:
            try:
                wait_element = self.check_find_element(how, element)
                wait_validate = True
                print('找到元素，不进行等待')
                break
            except:
                time.sleep(1)
                dead_line += 1
                if dead_line <= wait_time:
                    # print('等待',deadline,'秒')
                    continue
                else:
                    # 如果找不到元素进行截图，截图是按照当时时间来命名
                    # 判断如果没有指定失败图片且，同文件夹的名字为Fail_picture的文件夹新建一个
                    if fail_pic:
                        self.fail_picture(int(wait_time))
                    wait_validate = False
                    break
        assert wait_validate is True, '超过设定等待时间未发现元素:' + element
        # 返回一个元素
        return wait_element

    # 检查是否存在某元素
    def existence(self, how, element, wait=2, fail_pic=True):
        time.sleep(wait)
        try:
            self.check_find_element(how, element)
            existence_result = True
        except:
            if fail_pic:
                self.fail_picture(0)
            existence_result = False
        return existence_result

    def _elements(self, how, element):
        if how == 'id':
            find_elements = self.driver.find_elements_by_id(element)
        elif how == 'name':
            find_elements = self.driver.find_elements_by_xpath("//*[@text='%s' ]" % element)
        elif how == 'class':
            find_elements = self.driver.find_elements_by_class_name(element)
        # elif how == 'xpath':
        else:
            find_elements = self.driver.find_elements_by_xpath(element)
        return find_elements

    # 等待一类元素超过多久报错,默认5S
    def elements(self, how, element, element_time_waite=5, fail_pic=True):
        deadline = 0
        while True:
            eles = self._elements(how, element)
            if len(eles) > 0:
                elements_validate = True
                print('找到元素，不进行等待')
                break
            else:
                time.sleep(1)
                deadline += 1
                if deadline <= element_time_waite:
                    # print('等待',deadline,'秒')
                    continue
                else:
                    if fail_pic:
                        self.fail_picture(element_time_waite)
                    elements_validate = False
                    break
        assert elements_validate is True, '超过设定等待时间未发现元素:' + element
        # 返回一个元素
        return eles

    # 元素检查和截图存放位置
    def click(self, how, element, fail_pic=True):
        event_click = self.wait_element(how, element, fail_pic=fail_pic)
        event_click.click()

    def click_jump(self, how1, element1, how2="0", element2="0", fail_pic=True):
        jump_validate = True
        # 点击元素1
        event1 = self.wait_element(how1, element1, fail_pic=fail_pic)
        event1.click()
        time.sleep(2)
        # 通过一个元素是否存在对按键进行检验
        if how2 != "0" and element2 != "0":
            try:
                self.wait_element(how2, element2, fail_pic=fail_pic)
                jump_validate = True
            except:
                jump_validate = False

        return jump_validate

    # 通过元素本身是否变化进行判断元素是否被点击
    def click_change(self, how, element, click_type='change', fail_pic=True):
        # 元素检查和截图存放位置
        # global change_validate
        # 截取元素点击前的图片
        change_event = self.wait_element(how, element, fail_pic=fail_pic)
        click_before = 'click_before' + time.strftime('%Y%m%d%H%M%S')
        self.extend.get_screenshot_by_element(change_event).write_to_file(PATH + '/../temp', click_before)
        load = self.extend.load_image(PATH + '/../temp/%s.png' % click_before)
        time.sleep(2)
        change_event.click()
        time.sleep(4)
        if click_type == 'change':
            click_after = 'click_after' + time.strftime('%Y%m%d%H%M%S')
            self.extend.get_screenshot_by_element(change_event).write_to_file(PATH + '/../temp', click_after)
            result_same = self.extend.get_screenshot_by_element(change_event).same_as(load, 0)
            if not result_same:
                change_validate = True
            else:
                change_validate = False
        # hide形式（元素有可能隐藏或者消失）
        else:
            result_existence = self.existence(how, element, fail_pic=fail_pic)
            if result_existence:
                print('发现元素', element, '截图看是否一致')
                result_picture = self.extend.get_screenshot_by_element(change_event).same_as(load, 0)
                if not result_picture:
                    change_validate = True
                else:
                    change_validate = False
            else:
                print('隐藏元素', element, '成功')
                change_validate = True
        return change_validate

    # 获取一个元素的name属性
    def attribute_name(self, how, element, same_thing='none', fail_pic=True):
        attribute_event = self.wait_element(how, element, fail_pic=fail_pic)
        attribute_result = attribute_event.get_attribute('name')
        if same_thing != 'none':
            if same_thing == attribute_result:
                attribute_result = True
            else:
                attribute_result = False
        return attribute_result

    # 上下翻页(根据元素的高如果没有元素没拿默认200，可以优化为根据屏幕尺寸适应滑动大小）
    def swipe_up_down(self, how="none", element="none", swipe_type="up", swipe_nm=6):
        size_window = self.driver.get_window_size()
        width = size_window['width']
        height = size_window['height']
        if element != "none" and how != "none":
            event_swipe = self.elements(how, element)
            size_event = event_swipe[0].size
            if size_event["height"] < 200:
                v_y = 200
            else:
                v_y = size_event["height"]
        else:
            v_y = 200
        if swipe_type != "down":
            for i in range(swipe_nm):
                self.driver.swipe(width / 2, height - 200, width / 2, height - 200 - v_y)
        else:
            for i in range(swipe_nm):
                self.driver.swipe(width / 2, 0, width / 2, v_y)

    def element_check_count(self, how, element, random_click_time_nm):
        random_result = None
        try:
            self.check_find_element(how, element)
            random_result = True
        except:
            random_click_time_nm += 1
            self.driver.back()
            if random_click_time_nm == 20:
                random_result = False
        return random_result

    def random_click_no_page_turing(self, elements, random_event, random_click_time_nm):
        how1 = elements["how1"]
        element1 = elements["element1"]
        click_type = elements["click_type"]
        how2 = elements["how2"]
        element2 = elements["element2"]
        if click_type == 'click':
            time.sleep(1)
            # 以防第一个显示不全所以从1开始
            self.click(how1, element1)
        else:
            time.sleep(3)
            # 以防第一个显示不全所以从1开始
            TouchAction(self.driver).long_press(random_event[0]).wait(1).perform()
        # 检查看是否有元素2
        if how2 != 0:
            random_result = self.element_check_count(how2, element2, random_click_time_nm)
        else:
            random_result = self.element_check_count(how1, element1, random_click_time_nm)
        return random_result

    def random_click_page_turing(self, elements, random_event, random_click_time_nm):
        how1 = elements["how1"]
        element1 = elements["element1"]
        click_type = elements["click_type"]
        how2 = elements["how2"]
        element2 = elements["element2"]
        self.swipe_up_down(how1, element1)
        if click_type == 'click':
            time.sleep(0.5)
            print('发现对应元素数量', len(random_event))
            # 以防第一个显示不全所以从1开始
            event_random = self.elements(how1, element1)
            time.sleep(0.5)
            event_random[random.choice(range(len(event_random)))].click()
        else:
            # 长按元素
            time.sleep(3)
            # 以防第一个显示不全所以从1开始（这个。。。。）
            event_random = self.elements(how1, element1)[1]
            TouchAction(self.driver).long_press(event_random[random.choice(range(len(event_random)))]).wait(
                1).perform()
        # 检查看是否有元素2
        if how2 != 0:
            random_result = self.element_check_count(how2, element2, random_click_time_nm)
        else:
            random_result = self.element_check_count(how1, element1, random_click_time_nm)
        return random_result

    # 根据元素滑动屏幕随机点击该元素（若元素高度小于200则按照200进行滑动），并根据第二个元素进行判断。若不是则返回继续随机点击
    def random_click(self, how1, element1, click_type='click', how2=0, element2=0, fail_pic=True):
        # global random_result
        # 翻页并且随机选取元素
        elements = {"how1": how1, "element1": element1, "how2": how2, "element2": element2, "click_type": click_type}
        random_event = self.elements(how1, element1, fail_pic)
        random_click_time_nm = 0
        while True:
            # 翻页
            if len(random_event) > 1:
                random_result = self.random_click_page_turing(elements, random_event, random_click_time_nm)
                print(random_result)
                if random_result is not None:
                    break
            else:
                random_result = self.random_click_no_page_turing(elements, random_event, random_click_time_nm)
                print(random_result)
                if random_result is not None:
                    break
        return random_result

    # 随机点一个元素并获取其name属性
    def random_click_get_name(self, how, element):
        events = self.elements(how, element)
        event = random.choice(events)
        name = event.get_attribute('name')
        event.click()
        return name

    # 随机点击元素并获取同级元素的name属性
    def random_click_get_other_name(self, how1, element1, how2, element2):
        events1 = self.elements(how1, element1)
        events2 = self.elements(how2, element2)
        no = random.choice(range(len(events1)))
        time.sleep(0.5)
        name = events2[no].get_attribute('name')
        events1[no].click()
        return name

    # 逐个元素点击根据进入后的一个元素的Name属性判断是不想要点击的元素（滑动的高度是点击原始的高,能够匹配多个是否想要的名称）
    def reach_click(self, how1, element1, how2, element2, decide_name, *args, swipe_type="up"):
        events = self.elements(how1, element1)
        # 获取屏幕分辨率
        # 按照元素高度滑动并且选取第二个元素
        time_no = 0
        while True:
            self.swipe_up_down(how1, element1, swipe_type)
            time.sleep(2)
            events[1].click()
            try:
                event_check = self.check_find_element(how2, element2)
                event_check_name = event_check.get_attribute('name')
                print(event_check_name)
                print(args)
                if decide_name == 'same':
                    print('same')
                    assert event_check_name in args
                else:
                    print('not same')
                    assert event_check_name not in args
                reach_result = True
                break
            except:
                time_no += 1
                self.driver.back()
                # 10 次判断
                if time_no == 10:
                    reach_result = False
                    break
        return reach_result

    # 寻找元素点击
    def reach_element_click(self, how1, element1, no=50, fail_pic=True, swipe_type="up"):
        # 获取屏幕分辨率
        time_no = 0
        # print(v_y)
        while True:
            self.swipe_up_down(swipe_type)
            time.sleep(1)
            if (time_no > no) and (self.existence(how1, element1, fail_pic=fail_pic) == False):
                break
            try:
                self.click(how1, element1, fail_pic)
                break
            except Exception as e:
                print(e)

    # 点击元素后查看是否为想要点击的
    def reach_click_element(self, how1, element1, how2, element2, no=10, swipe_type="up"):
        elements = self.elements(how1, element1)
        # 获取屏幕分辨率
        # 按照元素高度滑动并且选取第二个元素
        time_no = 0
        while True:
            self.swipe_up_down(how1, element1, swipe_type)
            # self.driver.swipe(width * 500 / 1080, height * 500 / 1766, width * 500 / 1080,
            #                   height * (500 - v_y) / 1766)
            time.sleep(1)
            elements[1].click()
            try:
                self.check_find_element(how2, element2)
                break
            except:
                time_no += 1
                self.driver.back()
                if time_no == no:
                    break
                continue

    # 在元素上滑动
    def swipe_element_no(self, how, element, count):
        reach_event = self.elements(how, element)
        v_y = reach_event[0].size["height"]
        size = self.driver.get_window_size()
        width = size['width']
        height = size['height']
        no = 0
        while True:
            self.driver.swipe(width / 2, height / 2, width / 2, height / 2 - v_y)
            no += 1
            if no > count:
                break
            else:
                continue

    def using_text_to_click(self, width, height, v_y, text, count, count_time):
        reach_result = None
        try:
            reach_result = self.driver.find_element_by_xpath(
                "//*[@text='%s']" % text).click()
            reach_result = True
        except:
            self.driver.swipe(width / 2, height / 2, width / 2, height / 2 - v_y)
            count += 1
            if count > count_time:
                print('经过%s次没有找到对应的元素' % time)
                reach_result = False
        return reach_result

    def using_text_to_find(self, width, height, v_y, text, count, count_time):
        reach_result = None
        try:
            reach_result = self.driver.find_element_by_xpath(
                "//android.widget.TextView[@text='%s']" % text)
            reach_result = True
        except:
            self.driver.swipe(width / 2, height / 2, width / 2, height / 2 - v_y)
            count += 1
            if count > count_time:
                print('经过%s次没有找到对应的元素' % time)
                reach_result = False
        return reach_result

    # 根据元素的高度进行滑屏，发现对应的text,对其进行点击(或长按）
    def reach_find_name_to_click(self, how, element, text, reach_type='click', count_time=20):
        reach_result = True
        reach_event = self.elements(how, element)
        v_y = reach_event[0].size["height"]
        size = self.driver.get_window_size()
        width = size['width']
        height = size['height']
        count = 0
        while True:
            if reach_type is 'click':
                reach_result = self.using_text_to_click(width, height, v_y, text, count, count_time)
                if reach_result is not None:
                    break

            else:
                reach_result = self.using_text_to_find(width, height, v_y, text, count, count_time)
                if reach_result is not None:
                    break
        return reach_result

    # 滑动页面到下一个页面(tab),查看元素变化
    def swipe_page_left_right(self, how, element, direction='left', swip_type='different', fail_pic=True):
        swipe_page_event = self.wait_element(how, element, fail_pic=fail_pic)
        # 获取屏幕分辨率
        size = self.driver.get_window_size()
        width = size['width']
        height = size['height']
        # 滑动前判定元素截图
        swipe_before = 'Swipe_before' + time.strftime('%Y%m%d%H%M%S')
        self.extend.get_screenshot_by_element(swipe_page_event).write_to_file(PATH + '/../temp',
                                                                              swipe_before)
        if direction == 'left':
            self.driver.swipe(width * 1050 / 1080, height * 500 / 1766, width * 50 / 1080, height * 500 / 1766)
        else:
            self.driver.swipe(width * 50 / 1080, height * 500 / 1766, width * 1050 / 1080, height * 500 / 1766)
        load = self.extend.load_image(PATH + '/../temp/%s.png' % swipe_before)
        swipe_after = 'Swipe_after' + time.strftime('%Y%m%d%H%M%S')
        self.extend.get_screenshot_by_element(swipe_page_event).write_to_file(PATH + '/../temp',
                                                                              swipe_after)
        result_swipe = self.extend.get_screenshot_by_element(swipe_page_event).same_as(load, 0)
        if swip_type == 'different':
            if not result_swipe:
                return True
            else:
                return False
        else:
            return result_swipe

    # 上下滑动后元素是否隐藏
    def swipe_existence(self, how, element, fail_pic=True):
        swipe_existence_event = self.wait_element(how, element, fail_pic=fail_pic)
        # 获取屏幕分辨率
        swipe_existence = 'existence' + time.strftime('%H%M%S')
        self.extend.get_screenshot_by_element(swipe_existence_event).write_to_file(PATH + '/../temp',
                                                                                   swipe_existence)
        # 获取屏幕分辨率
        self.swipe_up_down()
        load = self.extend.load_image(PATH + '/../temp/%s.png' % swipe_existence)
        try:
            result_swipe = self.extend.get_screenshot_by_element(swipe_existence_event).same_as(load, 0)
        except:
            result_swipe = False
        if not result_swipe:
            result_swipe = True
        else:
            result_swipe = False
        return result_swipe

    # 结果为真错误截图
    def check_assert_true(self, chenck_true_result, msg):
        if chenck_true_result is not True:
            if os.path.exists(PATH + '/../fail_picture') is False:
                os.mkdir(PATH + '/../fail_picture')
            # 设置时间格式
            localtime = time.strftime('%Y%m%d%H%M%S')
            print('结果错误截图为:', localtime)
            # 以时间来命名截屏
            self.driver.get_screenshot_as_file(PATH + '/../fail_picture/' + localtime + '.png')
        self.tester.assertTrue(chenck_true_result, msg)

    # 结果为假错误截图
    def check_assert_false(self, chenck_false_result, msg):
        if chenck_false_result is not False:
            if os.path.exists(PATH + '/../fail_picture') is False:
                os.mkdir(PATH + '/../fail_picture')
            # 设置时间格式
            ISOTIMEFORMAT = '%Y%m%d_%X'
            localtime = str(time.strftime(ISOTIMEFORMAT, time.localtime())).replace(':', '')
            print('结果错误截图为:', localtime)
            # 以时间来命名截屏
            self.driver.get_screenshot_as_file(PATH + '/../fail_picture/' + localtime + '.png')
        self.tester.assertFalse(chenck_false_result, msg)

    # 获取某元素的图片,name选填
    def element_picture(self, how, element, name='element', fail_pic=True):
        picture_event = self.wait_element(how, element, fail_pic=fail_pic)
        name_p = name + time.strftime('%Y%m%d%H%M%S')
        if os.path.exists(PATH + '/../temp') is False:
            os.mkdir(PATH + '/../temp')
        self.extend.get_screenshot_by_element(picture_event).write_to_file(PATH + '/../temp', name_p)
        loadname = PATH + '/../temp/' + name_p + '.png'
        load = self.extend.load_image(loadname)
        return load

    # 获取当前元素与指定元素截图进行图片对比
    def contrast_element_picture(self, how, element, load, fail_pic=True):
        # 元素检查和截图存放位置
        global result
        cintrast_event = self.wait_element(how, element, fail_pic=fail_pic)
        cintrast_name = "cintrast" + time.strftime('%Y%m%d%H%M%S')
        self.extend.get_screenshot_by_element(cintrast_event).write_to_file(PATH + '/../temp', cintrast_name)
        result = self.extend.get_screenshot_by_element(cintrast_event).same_as(load, 0)
        return result

    # 获取元素的位置返回值可控
    def element_location(self, how, element, location_type='all'):
        location_element = self.check_find_element(how, element)
        location = location_element.location
        if location_type is 'x':
            return location['x']
        elif location_type is 'y':
            return location['y']
        else:
            return location

    # 通过坐标点击元素（不得已）
    def location_click(self, how, element):
        location = self.element_location(how, element)
        self.driver.tap([(location['x'], location['y'])])

    # 获取元素尺寸
    def element_size(self, how, element, size_type='all'):
        size_element = self.check_find_element(how, element)
        size = size_element.size
        if size is '"width"':
            return size['"width"']
        elif size_type is 'height':
            return size['height']
        else:
            return size

    # 输入法选择
    def select_keyboard(self, ime, device_config='none'):
        if device_config is 'none':
            os.system('adb shell ime enable %s' % ime)
            os.system('adb shell ime set %s' % ime)
        else:
            os.system('adb -s %s shell ime enable %s' % (device_config, ime))
            os.system('adb -s %s shell ime set %s' % (device_config, ime))
        time.sleep(2)

    # adb输入
    def adb_commend(self, text, device_config="none"):
        if device_config is 'none':
            os.system('adb shell input text %s' % text)
        else:
            os.system('adb -s %s shell input text %s' % (device_config, text))

    # 屏幕密度计算
    def density(self, device_config="none"):
        if device_config is 'none':
            density = 'adb  shell dumpsys window displays -c'
        else:
            density = 'adb  -s %s shell dumpsys window displays' % device_config
        # 这个运行方法好像是因为win才用的跟具体的获取使用keyboard中的那个更全面
        density_result = subprocess.Popen(density, stdout=subprocess.PIPE, shell=False).stdout.read()
        p = re.findall('...dpi', str(density_result))[0].split('dpi')
        print(int(p[0]) / int(160))
        return int(p[0]) / int(160)

    # 键盘条件准备
    def keyboard_get_ready(self, ime, how, element, device_config='none'):
        # 切换输入法
        self.select_keyboard(ime, device_config)
        time.sleep(4)
        # 获取键盘的最上方高度
        a = self.check_find_element(how, element)
        location = a.location['y']
        size = a.size['height']
        top_y = int(location) + int(size)
        print(top_y)
        return top_y

    # pid获取
    def get_app_pid(self, app_name, device='none'):
        if device == 'none':
            pid = os.popen("adb shell ps | grep " + app_name).read().split()[1]
        else:
            pid = os.popen("adb -s %s shell ps | grep " % device + app_name).read().split()[1]
        return pid

    # pid 验证
    def pid_verification(self, app_name, pid_before, device='none'):
        if device == 'none':
            pid = os.popen("adb shell ps | grep " + app_name).read().split()[1]
        else:
            pid = os.popen("adb -s %s shell ps | grep " % device + app_name).read().split()[1]
        if pid == pid_before:
            print('pid前后一致')
        else:
            assert 1 == 2, 'pid前后不一致错误'

    def checkpoint_pic(self, how, element, name, fail_pic=True):
        picture_event = self.wait_element(how, element, fail_pic=fail_pic)
        name_p = name + time.strftime('%Y%m%d%H%M%S')
        if os.path.exists('%s/checkpoint_record_data' % PATH) is False:
            os.mkdir('%s/checkpoint_record_data' % PATH)
        self.extend.get_screenshot_by_element(picture_event).write_to_file('%s/checkpoint_record_data' % PATH, name_p)
        return 'keyboard_regression/checkpoint_record_data/' + name_p + '.png'

    def checkpoint(self, table_name, how, element, name, fail_pic=True):
        create_table(table_name)
        no = query_the_fist(table_name)
        # 图片地址
        pic = self.checkpoint_pic(how, element, name)
        view_date = time.strftime('%Y%m%d%H%M%S')
        date = time.time()
        if no:
            pics = query_initial_last(table_name)
            i_pic = self.extend.load_image(pics['Initial'])
            l_pic = self.extend.load_image(pics['last'])
            picture_event = self.wait_element(how, element, fail_pic=fail_pic)
            now_pic = self.extend.get_screenshot_by_element(picture_event)
            i_c = now_pic.similarity_rate(i_pic)
            l_c = now_pic.similarity_rate(l_pic)
            insert_table(table_name, view_date=view_date, date=date, pic=pic, initial_pic=i_c, last_pic=l_c)
            print(i_c, l_c)
        else:
            insert_table(table_name, view_date=view_date, date=date, pic=pic, initial_pic=0, last_pic=0)

    # adb 打开应用
    def open_app_atcivity(self, activity, device_config="none"):
        if device_config is 'none':
            os.system('adb shell am restart  %s' % activity)
            os.system('adb shell am start -n %s' % activity)
        else:
            os.system('adb shell am restart  %s' % activity)
            os.system('adb -s %s shell am start -n %s' % (device_config, activity))
        time.sleep(2)

    def adb_install(self, app_path, device_config="none"):
        if device_config is 'none':
            os.system('adb install -r  %s' % app_path)
        else:
            os.system('adb -s %s install -r %s' % (device_config, app_path))
