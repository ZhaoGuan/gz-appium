# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import http.server
import urllib.parse
import time
from socketserver import ThreadingMixIn
import threading
import os
import json
import ssl


class WebRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        print('post message')
        parsed_path = urllib.parse.urlparse(self.path)
        paramstr = parsed_path.query
        path = parsed_path.path
        print(paramstr)
        print(path)
        for param in paramstr.split('&'):
            print(param)

        length = self.headers.get('content-length')
        nbytes = int(length)
        data = self.rfile.read(nbytes)
        cur_thread = threading.currentThread()
        print('Thread:%s\tdata:%s' % (cur_thread.getName(), data))

        message_parts = ['just a test']
        message = '\r\n'.join(message_parts)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(message.encode("utf-8"))

    def do_GET(self):
        print('get message')
        parsed_path = urllib.parse.urlparse(self.path)
        paramstr = parsed_path.query
        path = parsed_path.path
        print(paramstr)
        print(path)
        for param in paramstr.split('&'):
            print(param)

        if path == self.getShopLevelURL:
            buf = self.getShopLevelResponseBody
            buf = buf.encode("utf-8")
        elif path == self.getShopLevelURL1:
            # buf = open('./keyboard_preview.mp4', 'rb')
            buf = open('./keywords.txt', 'rb')
            buf = buf.read()
        else:
            buf = 'it works'
            buf = buf.encode("utf-8")
        # 获取文件大小
        size = os.path.getsize('./keywords.txt')
        self.protocal_version = 'HTTP/1.1'
        self.send_response(200)
        #添加头文件
        self.send_header('content-length', '%s' % size)
        self.send_header('content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(buf)
        # self.rfile.read(buf.encode("utf-8"))

    getShopLevelURL = '/v1/utils/feature_list'
    getShopLevelURL1 = '/gz/keywords.txt'
    # getShopLevelURL1 = '/api/getStatisticStrategy'
    getShopLevelResponseBody = '''
    {
    "errorCode": 0,
    "errorMsg": "ok",
    "data": {
        "ab_test": [{
            "feature_name": "open_platform_suggestion",
            "value": "1",
            "events": []
        },
        {
            "feature_name": "adjust_key_position",
            "value": "1",
            "events": []
        },
        {
            "feature_name": "is_support_voice_key",
            "value": "1",
            "events": []
        },
        {
            "feature_name": "kappi",
            "value": "1",
            "events": []
        },
        {
            "feature_name": "pull_strategy",
            "value": "1",
            "events": []
        },
        {
            "feature_name": "video_ad_test",
            "value": "0",
            "events": []
        },

        {
            "feature_name": "save_ads_for_fragments",
            "value": "1",
            "events": []
        },
        {
            "feature_name": "is_support_new_voice_ui",
            "value": "1",
            "events": []
        },
        {
            "feature_name": "detail_ad_admob",
            "value": "1",
            "events": []
        },

         {
            "feature_name": "magic_text",
            "value": "1",
            "events": []
        },
        {
            "feature_name": "sticker2_label_display",
            "value": "1",
            "events": []
        },
        {
            "feature_name": "detail_ad_admob_banner",
            "value": "1",
            "events": []
        },
         {
            "feature_name": "kappi_keyboard",
            "value": "1",
            "events": []
        },
        {
            "feature_name": "christmas_feature",
            "value": "0",
            "events": []
        },
        {
            "feature_name": "op_slide_on",
            "value": "1",
            "events": []
        },
        {
            "feature_name": "open_platform_view_pager",
            "value": "1",
            "events": []
        },

        {
            "feature_name": "is_charon_on",
            "value": "0",
            "events": []
        },
         {
            "feature_name": "op_icon_reddot",
            "value": "1",
            "events": []
        },
        {
            "feature_name": "news_push_icon",
            "value": "1",
            "events": []
        },
         {
            "feature_name": "open_platform_auto_full_screen",
            "value": "1",
            "events": []
        },
        {
            "feature_name": "try_keyboard",
            "value": "0",
            "events": []
        }, {
            "feature_name": "copy_paste_tip_new",
            "value": "0",
            "events": []
        }, {
            "feature_name": "sticker2_suggestion",
            "value": "1",
            "events": []
        }, {
            "feature_name": "facebook_ad_test_disable",
            "value": "0",
            "events": []
        }, {
            "feature_name": "local_emoji_recommend",
            "value": "0",
            "events": []
        }, {
            "feature_name": "picture_share_pop",
            "value": "0",
            "events": []
        }, {
            "feature_name": "report_performance_matrix",
            "value": "0",
            "events": []
        }, {
            "feature_name": "voice_box",
            "value": "1",
            "events": []
        }, {
            "feature_name": "keyboard_dango",
            "value": "0",
            "events": []
        }, {
            "feature_name": "keyboard_menu_theme",
            "value": "1",
            "events": []
        }, {
            "feature_name": "keyboard_emoji_ad",
            "value": "0",
            "events": []
        }, {
            "feature_name": "search",
            "value": "0",
            "events": []
        }, {
            "feature_name": "navigation_browser",
            "value": "0",
            "events": []
        }, {
            "feature_name": "emoji_engine_ab",
            "value": "0",
            "events": []
        }, {
            "feature_name": "browser_search",
            "value": "0",
            "events": []
        }, {
            "feature_name": "browser_web_search",
            "value": "0",
            "events": []
        }, {
            "feature_name": "hot_word",
            "value": "0",
            "events": []
        }, {
            "feature_name": "emoji_category",
            "value": "0",
            "events": []
        }, {
            "feature_name": "app_search",
            "value": "0",
            "events": []
        }, {
            "feature_name": "open_platform",
            "value": "1",
            "events": []
        }, {
            "feature_name": "test_ab_config_2",
            "value": "0",
            "events": []
        }, {
            "feature_name": "new_app_layout",
            "value": "0",
            "events": []
        }, {
            "feature_name": "news_ads_position",
            "value": "-1",
            "events": []
        }, {
            "feature_name": "hot_word",
            "value": "1",
            "events": []
        }, {
            "feature_name": "trace",
            "value": "1"
        }, {
        "feature_name": "show_single_gesture",
        "value": "0"
      }]
    }
}
    '''


class ThreadingHttpServer(ThreadingMixIn, http.server.HTTPServer):
    pass


if __name__ == '__main__':
    '''server = BaseHTTPServer.HTTPServer(('0.0.0.0',18360), WebRequestHandler) '''
    server = ThreadingHttpServer(('0.0.0.0', 9999), WebRequestHandler)
    # server.socket = ssl.wrap_socket(server.socket, certfile='./server.pem', server_side=True)
    ip, port = server.server_address
    '''Start a thread with the server -- that thread will then start one '''
    '''more thread for each request'''
    server_thread = threading.Thread(target=server.serve_forever)
    '''Exit the server thread when the main thread terminates'''
    server_thread.setDaemon(True)
    server_thread.start()

    print("Server loop running in thread:", server_thread.getName())
    while True:
        pass
