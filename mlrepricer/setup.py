# -*- coding: utf-8 -*-

"""Read config, an example Yaml you can find in configs.yaml."""
import os
from ruamel.yaml import YAML

homedir = os.path.expanduser('~')
path_to_config = f'{homedir}/.config/mlrepricer/configs.yaml'  # '/home/jeff/'
path_to_config = f'{homedir}/mlrepricer_configs.yaml'  # '/home/jeff/'


if path_to_config is None:
    raise ValueError('path_to_config canot be empty')

yaml = YAML(typ='unsafe')
yaml.default_flow_style = False

with open(path_to_config, 'r') as f:
    configs = yaml.load(f)
