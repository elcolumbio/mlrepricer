import pytest
import os
from ruamel.yaml import YAML

from mlrepricer import setup

yaml = YAML(typ='unsafe')
yaml.default_flow_style = False

datafolder = f"{setup.configs['datafolder']}sub/"
marketplaceid = setup.configs['marketplaceid']
currencycode = setup.configs['currencycode']


def test_message():
    for filename in os.listdir(datafolder):
        with open(datafolder + filename, 'r') as f:
            message = yaml.load(f)
        if message is None or isinstance(message, str):
            print(filename, message)
            continue
        metadata = message['Notification']['NotificationMetaData']
        payload = message['Notification']['NotificationPayload'][
            'AnyOfferChangedNotification']['OfferChangeTrigger']
        assert metadata['MarketplaceId'] == marketplaceid
        assert metadata['NotificationType'] == 'AnyOfferChanged'
        assert metadata['PayloadVersion'] == '1.0'
        assert payload['MarketplaceId'] == marketplaceid
        assert payload['ItemCondition'] == 'new'
