# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import yaml
import time
import os
import sys

PATH = os.path.dirname(os.path.abspath(__file__))
print(PATH)


def get_app_location():
    apps = {}
    # 注释部分是根据文件的创建时间筛选
    # path = './../package/'
    # temp = 0
    # app = ''
    # for filename in os.listdir('./../package'):
    #     app_time = os.path.getctime(path + filename)
    #     if app_time > temp:
    #         temp = app_time
    #         app = filename
    # print(path+app)
    # return path+app
    #
    for filename in os.listdir('./../package'):
        apps[filename] = filename.split('-')[2]
    temp = 0
    app = ''
    for i in apps:
        if int(apps[i]) > temp:
            temp = int(apps[i])
            app = i
    return app


def report(r_name):
    global name
    date = time.strftime('%Y%m%d', time.localtime())
    if os.path.exists(PATH + '/../Report') is False:
        os.mkdir(PATH + '/../Report')
    if os.path.exists(PATH + '/../Report/report_%s' % date) is False:
        os.mkdir(PATH + '/../Report/report_%s' % date)
    i = 1
    while True:
        if os.path.exists(PATH + '/../Report/report_%s/%s%s.html' % (date, r_name, i)) is True:
            i += 1
        else:
            name = PATH + '/../Report/report_%s/%s%s.html' % (date, r_name, i)
            break
    print('report over')
    return name


def yaml_reader(yaml_file):
    yf = open(yaml_file)
    yx = yaml.load(yf)
    return yx


def case_event_runner(yaml_file, self):
    case = yaml_reader(yaml_file)
    action_number = len(case)
    value = {}
    for i in range(action_number):
        action = case[i]
        print(action["action"])
        if action["type"] == "Null":
            select_function(action["function"], self, action)
        if action["type"] is True:
            self.ElementCheck.check_assert_true(
                select_function(action["function"], self, action),
                action["msg"])
        if action["type"] is False:
            self.ElementCheck.check_assert_false(
                select_function(action["function"], self, action),
                action["msg"])
        if action["type"] == "Value":
            value[action["value"]] = select_function(action["function"], self, action)


def select_function(function, self, action):
    functions = {
        # basics function方法
        "result_picture": lambda: self.ElementCheck.result_picture(action["result_name"]),
        "fail_picture": lambda: self.ElementCheck.fail_picture(action["timeout"]),
        "check_find_element": lambda: self.ElementCheck.check_find_element(action["element1_location"],
                                                                           action["element1_value"]),
        "wait_element": lambda: self.ElementCheck.wait_element(action["element1_location"], action["element1_value"]),
        "existence": lambda: self.ElementCheck.existenceexistence(action["element1_location"],
                                                                  action["element1_value"]),
        "element_input": lambda: self.ElementCheck.element_input(action["element1_location"], action["element1_value"],
                                                                 action["text"]),
        "elements": lambda: self.ElementCheck.elements(action["element1_location"], action["element1_value"]),
        "click": lambda: self.ElementCheck.click(action["element1_location"], action["element1_value"]),
        "click_jump": lambda: self.ElementCheck.click_jump(action["element1_location"], action["element1_value"],
                                                           action["element2_location"], action["element2_value"]),
        "click_change": lambda: self.ElementCheck.click_change(action["element1_location"], action["element1_value"],
                                                               action["mode"]),
        "attribute_name": lambda: self.ElementCheck.attribute_name(action["element1_location"],
                                                                   action["element1_value"], action["text"]),
        "swipe_up_down": lambda: self.ElementCheck.swipe_up_down(self, how="none", element="none", swipe_type="up",
                                                                 swipe_nm=6),
        "swipe_left_right": lambda: self.ElementCheck.swipe_left_right(self, how="none", element="none",
                                                                       swipe_type="left", swipe_nm=1),
        "random_click": lambda: self.ElementCheck.random_click(action["element1_location"], action["element1_value"],
                                                               click_type='click', how2=0, element2=0),
        "random_click_get_name": lambda: self.ElementCheck.random_click_get_name(action["element1_location"],
                                                                                 action["element1_value"]),
        "random_click_get_other_name": lambda: self.ElementCheck.random_click_get_other_name(
            action["element1_location"], action["element1_value"], action["element2_location"],
            action["element2_value"]),
        "reach_click": lambda: self.ElementCheck.reach_click(action["element1_location"], action["element1_value"],
                                                             action["element2_location"], action["element2_value"],
                                                             action["mode"], action["text"]),
        "reach_find_name_to_click": lambda: self.ElementCheck.reach_find_name_to_click(action["element1_location"],
                                                                                       action["element1_value"],
                                                                                       action["text"]),
        "swipe_page_left_right": lambda: self.ElementCheck.swipe_page_left_right(action["element1_location"],
                                                                                 action["element1_value"],
                                                                                 direction='left',
                                                                                 swipe_type='different'),
        "swipe_existence": lambda: self.ElementCheck.swipe_existence(action["element1_location"],
                                                                     action["element1_value"]),
        # "check_assert_true": lambda: self.ElementCheck.check_assert_true(self, chenck_ture_result, msg),
        # "check_assert_false": lambda: self.ElementCheck.check_assert_false(self, chenck_false_result, msg),
        "element_picture": lambda: self.ElementCheck.element_picture(action["element1_location"],
                                                                     action["element1_value"], name='element'),
        "contrast_element_picture": lambda: self.ElementCheck.contrast_element_picture(action["element1_location"],
                                                                                       action["element1_value"],
                                                                                       action["value"]),
        "adb_function": lambda: self.ElementCheck.adb_function(self, action["text"], device_udid='none'),
        "sougo_typewriting": lambda: self.ElementCheck.sougo_typewriting(self, device_udid='none'),
        "adb_input": lambda: self.ElementCheck.adb_input(self, action["text"], device_udid="none"),
        "element_loaction": lambda: self.ElementCheck.element_loaction(action["element1_location"],
                                                                       action["element1_value"], location_type='all'),
        "element_size": lambda: self.ElementCheck.element_size(action["element1_location"], action["element1_value"]),

    }
    return functions[function]()


if __name__ == '__main__':
    print(PATH)
