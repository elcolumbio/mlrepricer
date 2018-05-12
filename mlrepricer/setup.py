# -*- coding: utf-8 -*-

"""Read config."""

from ruamel.yaml import YAML

yaml = YAML(typ='unsafe')
yaml.default_flow_style = False

with open('./configs.yaml', 'r') as f:
    configs = yaml.load(f)
