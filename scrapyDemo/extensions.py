import requests
from scrapy import signals

NOTIFIER_URL = 'http://127.0.0.1:5000/notify'


class NotificationExtension(object):
    """
    This extension sends a notification to a webhook when a spider finishes.
    """

    @classmethod
    def from_crawler(cls, crawler):
        """
        Called when the extension is created.
        :param crawler:
        :return:
        """
        ext = cls()
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
        return ext

    def spider_opened(self, spider):
        """
        Called when a spider is opened.
        :param spider:
        :return:
        """
        requests.post(NOTIFIER_URL, json={
            'event': 'spider_opened',
            'data': {'spider_name': spider.name}
        })

    def spider_closed(self, spider):
        """
        Called when a spider is closed.
        :param spider:
        :return:
        """
        requests.post(NOTIFIER_URL, json={
            'event': 'spider_closed',
            'data': {'spider_name': spider.name}
        })

    def item_scraped(self, item, spider):
        """
        Called when an item is scraped.
        :param item:
        :param spider:
        :return:
        """
        requests.post(NOTIFIER_URL, json={
            'event': 'item_scraped',
            'data': {'item': dict(item).get('name'), 'spider_name': spider.name}
        })
