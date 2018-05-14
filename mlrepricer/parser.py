# -*- coding: utf-8 -*-

"""Created on SA 2018.05.12 @author: elcolumbio ."""

from ruamel.yaml import YAML
import os
import datetime
import pandas as pd

from . import setup
from . import helper

yaml = YAML(typ='unsafe')
yaml.default_flow_style = False

datafolder = f"{setup.configs['datafolder']}sub/"
marketplaceid = setup.configs['marketplaceid']
currencycode = setup.configs['currencycode']


def validate_message_content(message):
    """Validatation."""
    metadata = message['Notification']['NotificationMetaData']
    payload = message['Notification']['NotificationPayload'][
        'AnyOfferChangedNotification']['OfferChangeTrigger']
    assert metadata['MarketplaceId'] == marketplaceid
    assert metadata['NotificationType'] == 'AnyOfferChanged'
    assert metadata['PayloadVersion'] == '1.0'
    assert payload['MarketplaceId'] == marketplaceid
    assert payload['ItemCondition'] == 'new'


def parse_offers(payload):
    """Create one dict per offer, up to 20 offers per listing."""
    resultlist = []
    # common attributes per listing.
    asin = payload['OfferChangeTrigger']['ASIN']
    time_changed = datetime.datetime.strptime(
        payload['OfferChangeTrigger']['TimeOfOfferChange'],
        "%Y-%m-%dT%H:%M:%S.%fZ")

    for offer in payload['Offers']['Offer']:
        # attributes per offer
        if isinstance(offer, str):
            # bad format
            print(filename, offer)
            continue
        assert offer['SubCondition'] == 'new'
        assert offer['ListingPrice']['CurrencyCode'] == currencycode
        assert offer['Shipping']['CurrencyCode'] == currencycode

        # quantative, real valued
        price_total = float(offer['ListingPrice']['Amount']) + float(
            offer['Shipping']['Amount'])
        feedbackcount = int(offer['SellerFeedbackRating']['FeedbackCount'])
        pfeedbackpercent = int(
            offer['SellerFeedbackRating']['SellerPositiveFeedbackRating'])

        # nominal, unordered categorical
        sellerid = offer['SellerId']

        # ordinal, ordered categorical
        shipping_maxhours = int(offer['ShippingTime']['@maximumHours'])
        shipping_minhours = int(offer['ShippingTime']['@minimumHours'])

        # booleans
        isprime = int(offer['IsFulfilledByAmazon'] == 'true')
        isbuyboxwinner = int(offer['IsBuyBoxWinner'] == 'true')
        isfeaturedmerchant = int(offer['IsFeaturedMerchant'] == 'true')
        instock = int(offer['ShippingTime']['@availabilityType'] == 'NOW')

        row_dict = dict(
            time_changed=time_changed, asin=asin, sellerid=sellerid,
            price=price_total, isbuyboxwinner=isbuyboxwinner,
            feedback=feedbackcount, feedbackpercent=pfeedbackpercent,
            isfeaturedmerchant=isfeaturedmerchant,
            instock=instock, shipping_maxhours=shipping_maxhours,
            shipping_minhours=shipping_minhours, isprime=isprime)

        resultlist.append(row_dict)
    return resultlist


def main():
    global filename
    resultlist = []
    for filename in os.listdir(datafolder):
        with open(datafolder + filename, 'r') as f:
            message = yaml.load(f)
        if message is None or isinstance(message, str):
            # print(filename, message)
            continue
        validate_message_content(message)

        payload = message['Notification']['NotificationPayload'][
            'AnyOfferChangedNotification']
        newrows = parse_offers(payload)
        resultlist += newrows

    df = pd.DataFrame(resultlist)
    helper.dump_dataframe(df)


if __name__ == '__main__':
    main()
