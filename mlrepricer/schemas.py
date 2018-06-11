# -*- coding: utf-8 -*-


def pricemonitor(target):
    class PriceMonitor(target):
        """Every table inherits from the Destination class."""

        def __init__(self):
            super().__init__()
            self.table = 'price_monitor'
            self.if_exists = 'append'
            self.eventdate = 'time_changed'

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
    return PriceMonitor


def pricemonitorrecent(target):
    class PriceMonitorRecent(target):
        """Every table inherits from the Destination class."""

        def __init__(self):
            super().__init__()
            self.table = 'price_monitor_recent'
            self.if_exists = 'append'
            self.eventdate = 'time_changed'

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
    return PriceMonitorRecent


def mapping(target):
    class Mapping(target):
        """Every table inherits from the Destination class."""

        def __init__(self):
            super().__init__()
            self.table = 'mapping'
            self.if_exists = 'replace'

        @property
        def mapping(self):
            return {
                'asin': (self.textshort, False),
                'seller_sku': (self.textmiddle, False),
                'isprime': (self.booly, False)}
    return Mapping
