# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from mitmproxy import ctx
import logging
import re

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='./mitm_Test.log',
                    filemode='a')

# @concurrent

from mitmproxy import ctx
import json

replace_content = json.load(open('./featurelist.json', 'r'))
replace_content_1 = '''
        {
  "errorCode": 0,
  "errorMsg": "ok",
  "data": {
    "ab_test": [
      {
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
      },
      {
        "feature_name": "copy_paste_tip_new",
        "value": "0",
        "events": []
      },
      {
        "feature_name": "sticker2_suggestion",
        "value": "1",
        "events": []
      },
      {
        "feature_name": "facebook_ad_test_disable",
        "value": "0",
        "events": []
      },
      {
        "feature_name": "local_emoji_recommend",
        "value": "0",
        "events": []
      },
      {
        "feature_name": "picture_share_pop",
        "value": "0",
        "events": []
      },
      {
        "feature_name": "report_performance_matrix",
        "value": "0",
        "events": []
      },
      {
        "feature_name": "voice_box",
        "value": "1",
        "events": []
      },
      {
        "feature_name": "keyboard_dango",
        "value": "0",
        "events": []
      },
      {
        "feature_name": "keyboard_menu_theme",
        "value": "1",
        "events": []
      },
      {
        "feature_name": "keyboard_emoji_ad",
        "value": "0",
        "events": []
      },
      {
        "feature_name": "search",
        "value": "0",
        "events": []
      },
      {
        "feature_name": "navigation_browser",
        "value": "0",
        "events": []
      },
      {
        "feature_name": "emoji_engine_ab",
        "value": "0",
        "events": []
      },
      {
        "feature_name": "browser_search",
        "value": "0",
        "events": []
      },
      {
        "feature_name": "browser_web_search",
        "value": "0",
        "events": []
      },
      {
        "feature_name": "hot_word",
        "value": "0",
        "events": []
      },
      {
        "feature_name": "emoji_category",
        "value": "0",
        "events": []
      },
      {
        "feature_name": "app_search",
        "value": "0",
        "events": []
      },
      {
        "feature_name": "open_platform",
        "value": "1",
        "events": []
      },
      {
        "feature_name": "test_ab_config_2",
        "value": "0",
        "events": []
      },
      {
        "feature_name": "new_app_layout",
        "value": "0",
        "events": []
      },
      {
        "feature_name": "news_ads_position",
        "value": "-1",
        "events": []
      },
      {
        "feature_name": "hot_word",
        "value": "1",
        "events": []
      },
      {
        "feature_name": "trace",
        "value": "1"
      },
      {
        "feature_name": "show_single_gesture",
        "value": "1"
      }
    ]
  }
}
        '''
replace_response_content = '''{
  "ab": {
    "interval": 21600,
    "switch": 0
  },
  "ad": {
    "env": {
      "net": 0
    },
    "listen_apps": 1,
    "switch": 1
  },
  "data": {
    "conf_id": 1,
    "switch": 1
  },
  "error": {
    "env": {
      "net": 0
    },
    "switch": 1
  },
  "event": {
    "env": {
      "net": 0
    },
    "interval": 30,
    "lines": 200,
    "oid_in": [],
    "oid_out": [
      "db2dcc8e32c4992429f3d8a829293fc3",
      "d903e3d8ef3d3850276a415c88114ef6",
      "97e8f14cdeb4cf6e958af62f2e52019c",
      "a7d6d4391eea5e0e9cee6a13ee213c2c",
      "e09f30b142a1eff2e8392c6c27efcd45",
      "4c3302187384354e536a03a297f51e1a",
      "80429f5a38597ac23fcc5ccd4f7f746f",
      "d2258860bcb30509a9725ecd3cc4375a",
      "8d746950b68bdae1c0a4101c2088c663",
      "8684de3dbb86ee77439de127be412b58",
      "8b81b513e69641b9e603e068758f5d1a",
      "374488f6f1a5e9c27da1e91bc5292b76",
      "641075978209fc320424270bb190af75",
      "34fd61a1885ea3fb6e048248e26c2970",
      "fae85d73c50e9e2ea61a6b4e17197f52",
      "2eb6af447a946369750b36dc71d770ac",
      "d692317ccdc54ab57d5a02e8441e8dbc",
      "1c966b0de5fdc604d6f44826ea2d4b2f"
    ],
    "size_threshold": 204800,
    "switch": 1
  },
  "feature": {
    "kappi": {
      "events": [],
      "value": ""
    },
    "keyboard_emoji_ad": {
      "events": [
        "keyboard_emoji_ad,ad_click"
      ],
      "value": ""
    },
    "keyboard_menu_theme": {
      "events": [
        "plugin_tab,home"
      ],
      "value": ""
    },
    "kika_voice": {
      "events": [
        "system,stat",
        "keyboard,voice"
      ],
      "value": ""
    },
    "list": "emoji_tab_ad,open_platform_auto_full_screen,kika_voice,kappi,navigation_browser,open_platform_no_apptable,keyboard_emoji_ad,open_platform_push_style1,keyboard_menu_theme,open_platform",
    "navigation_browser": {
      "events": [
        "keyboard_inputview,create_time"
      ],
      "value": ""
    },
    "open_platform": {
      "events": [
        "keyboard_inputview,create_time"
      ],
      "value": ""
    },
    "open_platform_auto_full_screen": {
      "events": [],
      "value": ""
    },
    "open_platform_no_apptable": {
      "events": [],
      "value": ""
    },
    "open_platform_push_style1": {
      "events": [],
      "value": ""
    }
  },
  "heartbeat": {
    "interval": 21600,
    "switch": 0
  },
  "meta": {
    "env": {
      "net": 0
    },
    "interval": 14400,
    "switch": 1
  },
  "word": {
    "content": [
      "word",
      "trace"
    ],
    "env": {
      "net": 0
    },
    "interval": 20,
    "lines": 1,
    "mem_lines": 10,
    "size_threshold": 204800,
    "switch": 1
  }
}'''


def request(flow):
    if flow.request.host == 'api.kikakeyboard.com':
        flow.request.host = 'api-dev.kikakeyboard.com'
        logging.info('#########')
        logging.info(flow.request)
        logging.info(flow.request.header)
    text = 'hello'
    # flow.response.content = text.encode("utf-8")
    # flow.response.stream = True
    # logging.info(flow.request.pretty_host)
    pattern = re.compile('/v1/utils/get_app_config\?key=sticker2&')
    # logging.info(flow.request)
    # logging.info(flow.request.pretty_host)
    # logging.info(flow.request.path)
    # logging.info(flow.respon)
    # if flow.request.host == "172.16.2.167":
    # if pattern.match(flow.request.path):
    #     logging.info(flow)
    #     logging.info(flow.server_conn.address)
    #     logging.info(flow.server_conn.source_address)
    #     logging.info(flow.server_conn.spoof_source_address)
    # conn = open('./conn', 'w')
    # conn.write(str(flow))
    # if flow.request.host == 'm.baidu.com':
    if pattern.match(flow.request.path):
        logging.info('######################################')
        # f = flow.copy()
        # flow.request.host = "172.16.2.167"
        # flow.request.port = 4567
        # flow.request.path = '/v1/utils/feature_list'
        # ctx.master.replay_request(flow, block=False)
        # logging.info(f)
        logging.info(flow)
        logging.info(flow.request.path)
        logging.info(flow.request)
        logging.info(flow.response)
    if flow.request.host == "m.baidu.com":
        logging.info(flow)
        logging.info(flow.server_conn.address)
        logging.info(flow.server_conn.source_address)
        logging.info(flow.server_conn.spoof_source_address)
        logging.info(flow.server_conn.cert)
        logging.info(flow.server_conn.server_certs)
        logging.info(flow.server_conn.sni)
        # logging.info(flow.server_conn.cert)
        # logging.info(flow.server_conn.cert)
        # logging.info(flow.server_conn.cert)
        logging.info(flow.response)
        # flow.server_conn.address = None
        # flow.server_conn.sni = None
        # flow.server_conn = None
        flow.request.host = "172.16.2.167"
        flow.request.port = 4567
        flow.request.path = '/v1/utils/feature_list'
        logging.info("$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        logging.info(flow)
        logging.info(flow.server_conn.address)
        logging.info(flow.server_conn.source_address)
        logging.info(flow.server_conn.spoof_source_address)
        logging.info(flow.response)
        #     logging.info(flow)
        # data = json.load()
        # logging.info(flow.request.content)
        # logging.info(flow.request.host)
        # logging.info('^^^^^^^^^^^^^^^^^^^^^^^')
        # logging.info(flow.request.content)
        # if flow.request.host == 'api.kikakeyboard.com':
        #     logging.info('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        #     logging.info(flow)
        #     logging.info(flow.request.path)
        #     logging.info(flow.request.content)
        #     logging.info(flow.request.headers)
        #     logging.info(flow.request.data)
        # f = flow.copy()
        # replace =
        # ctx.master.view.add(f)
        # f.request.path = "/changed"
        # logging.info('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        # logging.info(f)
        # pattern = re.compile('/v1/utils/feature_list')
        # pattern = re.compile('/api/getStatisticStrategy')
        # if pattern.match(flow.request.path):
        #     logging.info(flow)
        #     logging.info(flow.request.host)
        # logging.info(flow.response.content)
        # flow.request.host = '192.168.0.106'
        # flow.request.port = 4567
        # flow.response.content = str(replace_content).encode("utf-8")
        # logging.info('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
        # logging.info(flow)
        # logging.info(flow.response.content)
        # logging.info(flow.request.content)
        # logging.info(flow.request.headers)
        # logging.info(flow.request.first_line_format)
        # logging.info(flow.request.scheme)
        # logging.info(flow.request.method)
        # logging.info(flow.request.timestamp_start)
        # logging.info(flow.request.timestamp_end)
        # ctx.master.view.add(f)
        # f.request.content = bytes(replace_content.encode())
        # logging.info('???????????????????')
        # logging.info(f)
        # logging.info(f.request.content)
        # logging.info(f.request.headers)
        # logging.info(f.request.first_line_format)
        # logging.info(f.request.scheme)
        # logging.info(f.request.method)
        # logging.info(f.request.timestamp_start)
        # logging.info(f.request.timestamp_end)
        # ctx.master.replay_request(f,  block=True)
