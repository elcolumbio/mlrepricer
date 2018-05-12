# -*- coding: utf-8 -*-

"""Created on SA 2018.05.12 @author: elcolumbio ."""

from ruamel.yaml import YAML
import os
import datetime
import setup

yaml = YAML(typ='unsafe')
yaml.default_flow_style = False

datafolder = setup.configs.datafolder
marketplaceid = setup.configs.marketplaceid
ownsellerid = setup.configs.ownsellerid
currencycode = setup.configs.currencycode


def test_message_content(message):
    """Validatation."""
    metadata = message['Notification']['NotificationMetaData']
    payload = message['Notification']['NotificationPayload'][
        'AnyOfferChangedNotification']['OfferChangeTrigger']
    assert metadata['MarketplaceId'] == marketplaceid
    assert metadata['NotificationType'] == 'AnyOfferChanged'
    assert metadata['SellerId'] == ownsellerid
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
        assert offer['SubCondition'] == 'new'
        sellerid = offer['SellerId']
        isprime = offer['IsFulfilledByAmazon'] == 'true'
        assert offer['ListingPrice']['CurrencyCode'] == currencycode
        assert offer['Shipping']['CurrencyCode'] == currencycode
        price_total = float(offer['ListingPrice']['Amount']) + float(
            offer['Shipping']['Amount'])
        isbuyboxwinner = offer['IsBuyBoxWinner'] == 'true'
        isfeaturedmerchant = offer['IsFeaturedMerchant'] == 'true'
        feedbackcount = int(offer['SellerFeedbackRating']['FeedbackCount'])
        pfeedbackpercent = int(
            offer['SellerFeedbackRating']['SellerPositiveFeedbackRating'])
        shipping_avail = offer['ShippingTime']['@availabilityType']
        shipping_maxhours = int(offer['ShippingTime']['@maximumHours'])
        shipping_minhours = int(offer['ShippingTime']['@minimumHours'])
        # shippingfrom = offer['ShipsFrom']['Country'] only if not prime

        row_dict = dict(
            time_changed=time_changed, asin=asin, sellerid=sellerid,
            price=price_total, isbuyboxwinner=isbuyboxwinner,
            feedbackcount=feedbackcount, pfeedbackpercent=pfeedbackpercent,
            isfeaturedmerchant=isfeaturedmerchant,
            shipping_avail=shipping_avail, shipping_maxhours=shipping_maxhours,
            shipping_minhours=shipping_minhours, isprime=isprime)

        resultlist.append(row_dict)
    return resultlist


resultlist = []
for filename in os.listdir(datafolder)[:1]:
    with open(datafolder + filename, 'r') as f:
        message = yaml.load(f)
    test_message_content(message)

    payload = message['Notification']['NotificationPayload'][
        'AnyOfferChangedNotification']
    newrows = parse_offers(payload)
    resultlist += newrows
