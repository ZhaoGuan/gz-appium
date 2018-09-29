# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import yaml


def config_reader(yamlfile):
    try:
        with open(yamlfile) as yf:
            yx = yaml.load(yf)
    except:
        file = open(yamlfile, 'w')
        file.close()
        yx = None
    return yx


def config_writer(config_data, yamlfile):
    with open(yamlfile, 'w') as yf:
        yaml.dump(config_data, yf, default_flow_style=False, )


def rewriter_config(key, value, yamlfile):
    config = config_reader(yamlfile)
    if isinstance(config[key], list):
        config[key].append(value)
    else:
        config[key] = value
    config_writer(config, yamlfile)


def clear_config_key(key, value, yamlfile):
    config = config_reader(yamlfile)
    config[key] = value
    config_writer(config, yamlfile)
