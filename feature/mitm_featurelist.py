# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import logging
import re
import json

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='./feature.log',
                    filemode='a')
with open('./featurelist.json', 'r') as featureslist:
    replace_content1 = json.load(featureslist)
with open('./old_ab.json', 'r') as ab:
    replace_content2 = ab


def response(flow):
    pattern1 = re.compile('/v1/utils/feature_list')
    pattern2 = re.compile('/api/getStatisticStrategy')
    if pattern1.match(flow.request.path):
        logging.info(flow)
        # logging.info(flow.request.host)
        logging.info(flow.response.content)
        # flow.request.host = '192.168.0.106'
        # flow.request.port = 4567
        flow.response.content = str(replace_content1).encode("utf-8")
        logging.info('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
        logging.info(flow)
        logging.info(flow.response.content)
    elif pattern2.match(flow.request.path):
        logging.info(flow)
        # logging.info(flow.request.host)
        logging.info(flow.response.content)
        # flow.request.host = '192.168.0.106'
        # flow.request.port = 4567
        flow.response.content = str(replace_content2).encode("utf-8")
        logging.info('********************************')
        logging.info(flow)
        logging.info(flow.response.content)
