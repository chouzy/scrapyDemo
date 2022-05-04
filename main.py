import os
import sys

from scrapy.cmdline import execute

# 打断点调试py文件
if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    print(os.path.dirname(os.path.abspath(__file__)))
    execute(['scrapy', 'crawl', 'scrape'])
