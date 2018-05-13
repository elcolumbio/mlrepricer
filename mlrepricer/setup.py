# -*- coding: utf-8 -*-

"""Read config."""

from ruamel.yaml import YAML

path_to_config = '/home/flo/.config/mlrepricer/configs.yaml'  # '/home/jeff/'

if path_to_config is None:
    raise ValueError('path_to_config canot be empty')

yaml = YAML(typ='unsafe')
yaml.default_flow_style = False

with open(path_to_config, 'r') as f:
    configs = yaml.load(f)
