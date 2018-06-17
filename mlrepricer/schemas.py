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
                'asin': (self._textshort, False),
                'feedback': (self._inty, False),
                'feedbackpercent': (self._inty, False),
                'instock': (self._booly, False),
                'isbuyboxwinner': (self._booly, False),
                'isfeaturedmerchant': (self._booly, False),
                'isprime': (self._booly, False),
                'price': (self._numericy, False),
                'sellerid': (self._textshort, False),
                'shipping_maxhours': (self._inty, False),
                'shipping_minhours': (self._inty, False),
                'time_changed': (self._datey, False)}
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
                'asin': (self._textshort, False),
                'feedback': (self._inty, False),
                'feedbackpercent': (self._inty, False),
                'instock': (self._booly, False),
                'isbuyboxwinner': (self._booly, False),
                'isfeaturedmerchant': (self._booly, False),
                'isprime': (self._booly, False),
                'price': (self._floaty, False),
                'sellerid': (self._textshort, False),
                'shipping_maxhours': (self._inty, False),
                'shipping_minhours': (self._inty, False),
                'time_changed': (self._datey, False)}
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
                'asin': (self._textshort, False),
                'seller_sku': (self._textmiddle, False),
                'isprime': (self._booly, False)}
    return Mapping
