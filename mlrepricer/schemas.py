# -*- coding: utf-8 -*-
# import your Target Class, for a example see exampley_destination.py
import Target


class PriceMonitor(Target):
    """
    For each table define a class which inherits from the Destination class.
    """
    table = 'price_monitor'
    if_exists = 'append'
    eventdate = 'time_changed'

    @property
    def mapping(self):
        return {
            'asin': (self.textshort, False),
            'feedback': (self.inty, False),
            'feedbackpercent': (self.inty, False),
            'instock': (self.booly, False),
            'isbuyboxwinner': (self.booly, False),
            'isfeaturedmerchant': (self.booly, False),
            'isprime': (self.booly, False),
            'price': (self.float, False),
            'sellerid': (self.textshort, False),
            'shipping_maxhours': (self.inty, False),
            'shipping_minhours': (self.inty, False),
            'time_changed': (self.datey)}

    @property
    def conn(self):
        return self.connection_engine()


class PriceMonitorRecent(Target):
    """
    For each table define a class which inherits from the Destination class.
    """
    table = 'price_monitor_recent'
    if_exists = 'append'
    eventdate = 'time_changed'

    @property
    def mapping(self):
        return {
            'asin': (self.textshort, False),
            'feedback': (self.inty, False),
            'feedbackpercent': (self.inty, False),
            'instock': (self.booly, False),
            'isbuyboxwinner': (self.booly, False),
            'isfeaturedmerchant': (self.booly, False),
            'isprime': (self.booly, False),
            'price': (self.float, False),
            'sellerid': (self.textshort, False),
            'shipping_maxhours': (self.inty, False),
            'shipping_minhours': (self.inty, False),
            'time_changed': (self.datey)}

    @property
    def conn(self):
        return self.connection_engine()
