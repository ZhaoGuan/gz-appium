# coding=utf-8
# __author__ = 'yuelian'

import os


class AppiumConfig(object):
    def get_device_udid(self):
        # 获取所连接设备的udid
        a = os.popen("adb devices").read()
        b = (a.split("\n"))[1:-2]
        udid = []
        for i in b:
            udid.append(i.split("\t")[0])
        return udid

    def get_appium_set(self):
        __udid = AppiumConfig.get_device_udid(self)
        # 编辑appium的服务地址及端口
        begin_server = {"ip": "127.0.0.1", "p": "4711", "bp": "4721", "udid": "%s" % __udid[0]}
        appium_server = []
        appium_config = []
        config = {}
        for i in range(len(__udid)):
            if i > 0:
                # win
                # appium_server.append({"ip": "127.0.0." + str(i + 1), "p": "471" + str(i + 1), "bp": "472" + str(i + 1),
                #                       "udid": "%s" % __udid[i]})
                # appium_config.append(["127.0.0." + str(i + 1), "471" + str(i + 1), "472" + str(i + 1)])
                # MAC
                appium_server.append({"ip": "127.0.0.1", "p": "471" + str(i + 1), "bp": "472" + str(i + 1),
                                      "udid": "%s" % __udid[i]})
                appium_config.append(["127.0.0.1", "471" + str(i + 1), "472" + str(i + 1)])
            else:
                appium_server.append(begin_server)
                appium_config.append(["127.0.0.1", "4711", "4721"])
            new_config = {__udid[i]: appium_config[i]}
            config.update(new_config)
        return config


if __name__ == "__main__":
    appium_config = AppiumConfig()
    udid = appium_config.get_device_udid()
    appium = appium_config.get_appium_set()
    print(udid)
    print(appium)
