# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from elasticsearch import Elasticsearch
# useful for handling different item types with a single interface
from pymongo import MongoClient
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class MongoDBPipeline(object):
    """
    将数据存入 MongoDB
    """

    @classmethod
    def from_crawler(cls, crawler):
        """
        获取配置信息
        :param crawler:
        :return:
        """
        cls.connection_string = crawler.settings.get('MONGODB_CONNECTION_STRING')
        cls.database = crawler.settings.get('MONGODB_DATABASE')
        cls.collection = crawler.settings.get('MONGODB_COLLECTION')
        return cls()

    def open_spider(self, spider):
        """
        启动 spider 时调用，用于链接 MongoDB
        :param spider:
        :return:
        """
        self.client = MongoClient(self.connection_string)
        self.db = self.client[self.database]

    def process_item(self, item, spider):
        """
        将数据存储到 MongoDB
        :param item:
        :param spider:
        :return:
        """
        self.db[self.collection].update_one({
            'name': item['name']
        }, {
            '$set': dict(item)
        }, True)
        return item

    def close_spider(self, spider):
        """
        关闭数据库
        :param spider:
        :return:
        """
        self.client.close()


class ElasticsearchPipeline(object):
    """
    将数据存入 ES
    """

    @classmethod
    def from_crawler(cls, crawler):
        """
        获取配置信息
        :param crawler:
        :return:
        """
        cls.connection_string = crawler.settings.get('ELASTICSEARCH_CONNECTION_STRING')
        cls.index = crawler.settings.get('ELASTICSEARCH_INDEX')
        return cls()

    def open_spider(self, spider):
        """
        链接数据库
        :param spider:
        :return:
        """
        self.conn = Elasticsearch(hosts=self.connection_string)
        if not self.conn.indices.exists(index=self.index):
            self.conn.indices.create(index=self.index)

    def process_item(self, item, spider):
        """
        将数据存入 ES
        :param item:
        :param spider:
        :return:
        """
        self.conn.index(index=self.index, body=dict(item), id=hash(item['name']))
        return item

    def close_spider(self, spider):
        """
        关闭数据库
        :param spider:
        :return:
        """
        self.conn.transport.close()


class ImagePipeline(ImagesPipeline):
    """
    图片处理
    """

    def file_path(self, request, response=None, info=None, *, item=None):
        """
        设置文件存储名称
        :param request:
        :param response:
        :param info:
        :param item:
        :return:
        """
        movie = request.meta['movie']
        type = request.meta['type']
        name = request.meta['name']
        file_name = f'{movie}/{type}/{name}.jpg'
        return file_name

    def item_completed(self, results, item, info):
        """
        判断文件是否下载成功
        :param results:
        :param item:
        :param info:
        :return:
        """
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem('Item Download Failed')
        return item

    def get_media_requests(self, item, info):
        """
        遍历 item 获取下载链接
        :param item:
        :param info:
        :return:
        """
        for director in item['directors']:
            director_name = director['name']
            director_image = director['image']
            yield Request(director_image, meta={
                'name': director_name,
                'type': 'director',
                'movie': item['name']
            })
        for actor in item['actors']:
            actor_name = actor['name']
            actor_image = actor['image']
            yield Request(actor_image, meta={
                'name': actor_name,
                'type': 'actor',
                'movie': item['name']
            })
