# -*- coding: utf-8 -*-
"""Pushing new prices to amazon with the mws python api."""
import redis
import xmltodict
from mlrepricer import parser, helper, setup, minmax
import mws
import threading

mwsid = helper.mwscred['account_id']

if setup.configs['region'] in ['IT', 'FR', 'ES', 'DE']:
    decimal = ','
else:
    decimal = '.'

r = redis.StrictRedis(helper.rediscred, decode_responses=True)
mapping = minmax.load_csv()


class Updater(threading.Thread):
    """Demon Thread push new price data to your mws seller account."""

    def run(self):
        """Thread should run once."""
        print(f'Starting {self.name}')
        main()


def get_latest_message(asin):
    """Leverage the structure of redis zsets sorted sets with score."""
    m = r.zrevrangebyscore(asin, 'inf', '-inf', start=0, num=1,
                           withscores=True)
    return parser.main(xmltodict.parse(m[0][0]))


def get_buyboxwinners(parsedxml):
    """
    Return one or multiple winner for prime and not prime offers.

    If we are not in the buybox.
    Format: ([prime_offerobject, ...], [nonprime_offerobject, ...])
    """
    prime_winner, nonprime_winner = [], []
    for x in parsedxml:
        if (x['sellerid'] == mwsid) & (x['isbuyboxwinner']):
            return [], []  # if we are winning, we are happy
        elif x['isbuyboxwinner'] & x['isprime']:
            prime_winner.append(x)
        elif x['isbuyboxwinner'] & ~x['isprime']:
            nonprime_winner.append(x)
    return prime_winner, nonprime_winner


def get_sku(asin):
    """We assume there is you have max one offer per type."""
    m = mapping.asin == asin
    prime_offer = list(mapping[m & (mapping.isprime)].seller_sku.values)
    nonprime_offer = list(mapping[m & ~(mapping.isprime)].seller_sku.values)
    return (prime_offer, nonprime_offer)


def matchprice(sku, winner):
    for x, y in zip(sku, winner):
        if x and y:  # When the buybox is the same type as our listing
            sellersku = x[0]
            p = [c['price'] for c in y]
            buyboxprice = round(sum(p)/float(len(p)), 2)
            return sellersku, buyboxprice


def make_feed_row(feed_row_template, product):
    return feed_row_template.format(product[0],
                                    str(product[1]).replace('.', decimal))


def create_feed(products_to_update):
    feed_header = 'sku\tprice\n'
    feed_row_template = '{}\t{}'
    feed_row_list = []

    for product in products_to_update:
        if product is not None:
            feed_row = make_feed_row(feed_row_template, product)
            feed_row_list.append(feed_row)

    feed_data = feed_header + '\n'.join(feed_row_list)
    return feed_data.encode('utf8')


def main():
    products_to_update = []
    for asin in r.smembers('updated_asins'):
        winner = get_buyboxwinners(get_latest_message(asin))
        sku = get_sku(asin)
        products_to_update.append(matchprice(sku, winner))

    feed_data = create_feed(products_to_update)
    feeds_api = mws.Feeds(**helper.mwscred)
    return feeds_api.submit_feed(feed_data, '_POST_FLAT_FILE_INVLOADER_DATA_')
