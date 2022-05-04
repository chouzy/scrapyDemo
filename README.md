# scrapyDemo

> Scrapy 框架练习项目
>
> 测试网站：https://ssr1.scrape.center/

功能：

- 解析网页，获取网页中的电影名称、类别、评分、简介、导演、演员等信息；
- 将数据存储在 MongoDB 和 Elasticsearch；
- 下载网页中的图片到本地并按照电影名称对图片进行分类和重命名；
- 自定义扩展实现向接口中发送爬取状态和信息；
- 定义了一个 API 接口用于获取爬虫的爬取状态；

## 项目结构

```
scrapyDemo
 ├── scrapyDemo
 │   ├── spiders
 │   │   └── scrape.py
 │   ├── extensions.py    # 自定义扩展
 │   ├── items.py
 │   ├── middlewares.py
 │   ├── pipelines.py
 │   └── settings.py
 ├── main.py    # 该文件可以以 debug 方式启动项目
 ├── README.md
 ├── requirements.txt
 ├── scrapy.cfg
 └── flask_api.py    # 自定义API接口
```

## 运行

### 安装依赖

```shell
pip install -r requirement.txt
```

### 修改项目配置

```
scrapyDemo -> scrapyDemo -> settings.py
```

```python
# 数据库链接
# MongoDB
MONGODB_CONNECTION_STRING = 'mongodb://localhost:27017'
MONGODB_DATABASE = 'movies'
MONGODB_COLLECTION = 'movies'
# ElasticSearch
ELASTICSEARCH_CONNECTION_STRING = 'http://127.0.0.1:9200'
ELASTICSEARCH_INDEX = 'movies'

# 照片存储路径
IMAGES_STORE = '../images'
```

### 运行

```
scrapy crawl scrape
```

### debug

```
main.py
```
