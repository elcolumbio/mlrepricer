# -*- coding: utf-8 -*-
"""Pushing new prices to amazon with the mws python api."""
import datetime as dt
import mws
import threading
import time
import redis
import xmltodict

from mlrepricer import parser, helper, setup, minmax

mwsid = helper.mwscred['account_id']
decimal = setup.decimal

r = redis.Redis(**helper.rediscred, decode_responses=True)
mapping = minmax.load_csv()


class Updater(threading.Thread):
    """Demon Thread push new price data to your mws seller account."""

    def run(self):
        """Thread should run once."""
        print(f'Starting {self.name}')
        main()


def get_all_messages(asin):
    """Return the parsed and flattend message stored in redis zsets."""
    message = r.zrevrangebyscore(asin, 'inf', '-inf', start=0, num=1,
                                 withscores=True)
    return parser.main(xmltodict.parse(message[0][0]))


def get_latest_message(asin):
    """Return the latest message per asin as a pandas dataframe."""
    # Leverage the structure of redis zsets, sorted sets with score.
    message = r.zrevrangebyscore(asin, 'inf', '-inf', start=0, num=1,
                                 withscores=True)
    if message:
        latest_message = parser.parse(eval(message[0][0]))
        if latest_message.empty:
            latest_message = False
    else:  # memo without data, shouldn't happen in production
        latest_message = False
    return latest_message


def get_buyboxwinner(message_df):
    """
    Return one or multiple winner for prime and not prime offers.

    Format: ([prime_offerobject, ...], [nonprime_offerobject, ...])
    If both lists are empty, nobody owns the buybox.
    """
    prime_winner, nonprime_winner = [], []
    for x in message_df.iterrows():
        x = x[1]  # get values for each row
        if (x['sellerid'] == mwsid) & (x['isbuyboxwinner']):
            # mark this as own listings
            if x['isbuyboxwinner'] & x['isprime']:
                prime_winner.append(x)
            elif x['isbuyboxwinner'] & ~x['isprime']:
                nonprime_winner.append(x)
        elif x['isbuyboxwinner'] & x['isprime']:
            prime_winner.append(x)
        elif x['isbuyboxwinner'] & ~x['isprime']:
            nonprime_winner.append(x)
    return prime_winner, nonprime_winner


def get_sku(asin):
    """Return your listings for an asin, both for prime and nonprime."""
    # We assume you have max one offer per type, or we use a random one
    prime_offer = list(
        mapping[mapping.asin == asin + '_prime'].seller_sku.values)
    nonprime_offer = list(
        mapping[mapping.asin == asin + '_seller'].seller_sku.values)
    if len(prime_offer) > 1:  # ignore duplicate same type of listing
        prime_offer = prime_offer[0] 
    if len(nonprime_offer) > 1:
        nonprime_offer = nonprime_offer[0]
    return (prime_offer, nonprime_offer)


def compare_prime_type(sku, winner):
    """Easier to compare listings of different types."""
    compare = zip(sku, winner)
    # x = [prime_sku, prime_price], y = [nonprime_sku, nonprime_price]
    # there are 3 common cases, same listingtyp than winner
    # different listingtype than winner, no listing at all.
    # probably we need to define all permutations
    # comment: own_listing_type -> buyboxwinner_listing_type
    # than we can apply tactics for each case
    if compare[0][0] and compare[0][1]:
        pass
        # prime -> prime
    elif compare[1][0] and compare[1][1]:
        pass
        # nonprime -> nonprime
    elif compare[0][0] and compare[1][1]:
        pass
        # prime -> nonprime
    elif compare[1][0] and compare[0][1]:
        pass
        # nonprime -> prime
    else:
        # nobuyboxwinner
        assert any(compare) is False


def matchprice(sku, winner):
    """Primitive repricing rule."""
    # x = [prime_sku, prime_price], y = [nonprime_sku, nonprime_price]
    for x, y in zip(sku, winner):
        if x and y:  # When the buybox is the same type as our listing
            sellersku = x[0]
            p = [c['price'] for c in y]
            buyboxprice = round(sum(p)/float(len(p)), 2)
            return sellersku, buyboxprice
    return False, False


def boundaries(sku, buyboxprice):
    df = minmax.load_csv()
    min = buyboxprice >= df[df.seller_sku == sku]['min'].values[0]
    max = buyboxprice <= df[df.seller_sku == sku]['max'].values[0]
    return min and max  # return True if new prize is between min and max


def create_feed(new_prices):
    """Create a tsv file for the mws feeds api."""
    feed_header = 'sku\tprice\n'
    feed_row_list = []

    for product in new_prices:
        if product is not None:
            # the feedrow format: 'sku\tprice'
            feed_row = f"{product[0]}\t{str(product[1]).replace('.', decimal)}"
            feed_row_list.append(feed_row)

    feed_data = feed_header + '\n'.join(feed_row_list)
    return feed_data.encode('utf8')


def main():
    """Pop the list of changed asins and take action on them."""
    while True:
        starttime = time.time()
        new_prices = []
        for asin in r.smembers('updated_asins'):
            message = get_latest_message(asin)
            r.srem('updated_asins', asin)  # remove memo to process asin
            if not isinstance(message, bool):
                # all rows of one message have the same date
                winner = get_buyboxwinner(message)
                own_skus = get_sku(asin)  # max one for each type
                sku, new_price = matchprice(own_skus, winner)
                if sku and new_price and boundaries(sku, new_price):
                    new_prices.append([sku, new_price])
                    # we store the action in redis
                    time_changed = message['time_changed'][0].isoformat()
                    # we will use the redis stream datatype
                    print(redis.__version__)
                    r.xadd('actions', {'asin': asin, 'sku': sku, 'new_price': new_price, 'time_changed': time_changed})

        feed_data = create_feed(new_prices)
        feeds_api = mws.Feeds(**helper.mwscred)
        feeds_api.submit_feed(feed_data, '_POST_FLAT_FILE_INVLOADER_DATA_')
        # We send maximum every 120 seconds a new feed to the mws api.
        time.sleep(120.0 - ((time.time() - starttime) % 120.0))
