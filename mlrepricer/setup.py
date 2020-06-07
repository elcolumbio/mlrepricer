# -*- coding: utf-8 -*-

"""Read config file, an example Yaml file you can find in configs.yaml."""
import os
from ruamel.yaml import YAML

yaml = YAML()
yaml.default_flow_style = False


homedir = os.path.expanduser('~')
path_to_config = f'{homedir}/.config/mlrepricer_configs.yaml'  # '/home/jeff/'
path_to_config = f'{homedir}/mlrepricer_configs.yaml'  # '/home/jeff/'


if path_to_config is None:
    raise ValueError('path_to_config canot be empty')

# we read the main config file
with open(path_to_config, 'r') as f:
    configs = yaml.load(f)


# your decimal seperator
if configs['region'] in ['IT', 'FR', 'ES', 'DE']:
    decimal = ','
else:
    decimal = '.'
