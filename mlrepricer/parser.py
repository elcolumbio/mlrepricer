# -*- coding: utf-8 -*-

"""
Created on SA 2018.05.12 @author: elcolumbio .

We call this quite hidden in listener.py in the dump_message_tosql method.
Before we used a file dump and parsed afterwards.
"""

import datetime
import pandas as pd
import xmltodict

from . import setup
from . import helper

marketplaceid = helper.Marketplaces[setup.configs['region']].marketplace_id
currencycode = setup.configs['currencycode']


def parse(message):
    """Parse the message and return a pandas dataframe."""
    r = xmltodict.parse(message[0]['Body'])
    # here we call the parser.py file •=•
    return pd.DataFrame(main(r))


def validate_message_meta(message):
    """Validatation for data we get per messageid."""
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
        if isinstance(offer, str):
            # print(f'wrong format for one {offer} expected dict got string')
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


def main(message):
    """Input is the message body, here parsing by xmltodict, outputs a dataframe"""
    validate_message_meta(message)
    payload = message['Notification']['NotificationPayload'][
        'AnyOfferChangedNotification']
    return parse_offers(payload)


if __name__ == '__main__':
    parse()
