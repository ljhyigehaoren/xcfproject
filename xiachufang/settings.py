# -*- coding: utf-8 -*-

# Scrapy settings for xiachufang project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'xiachufang'

SPIDER_MODULES = ['xiachufang.spiders']
NEWSPIDER_MODULE = 'xiachufang.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'xiachufang (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #   # 'Accept-Language': 'en',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'xiachufang.middlewares.XiachufangSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'xiachufang.middlewares.XiachufangDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    #'xiachufang.pipelines.XiachufangPipeline': 300,
    #'xiachufang.pipelines.XiachufnagCoverImagePipeline':299,
   'scrapy_redis.pipelines.RedisPipeline': 400,
}

#设置图片的存储路径
IMAGES_STORE = '/Users/ljh/Desktop/xiachufang/Images'

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

#配置数据库信息(mysql)
MYSQL_HOST = '127.0.0.1'
MYSQL_USER = 'root'
MYSQL_PWD = 'ljh1314'
MYSQL_DB = 'class1809'
MYSQL_PORT = 3306
MYSQL_CHARSET = 'utf8'

#DUPEFILTER_CLASS:设置去重组件为scrapy_redis自定义的模块,
#不再使用scrapy框架自带的去重组件（必须设置）
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

#SCHEDULER：设置调度器组件为scrapy_redis自定义的模块,
#不再使用 scrapy框架自带的调度器模块
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

#设置为True，表示允许断点爬取
SCHEDULER_PERSIST = True

#设置任务队列的存取方式（三选一，默认第一种方式）
#  SpiderPriorityQueue是scrapy——redis框架默认的任务存储方式
# （任务有自己的优先级，队列的实现方式是使用的redis数据库中的有序集合）
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"

#SpiderQueue (FIFO:先进先出)
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
#SpiderStack（ LIFO:后进先出）
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"

#设置redis数据库库的配置信息（redis 数据库中存储队列任务和指纹集合）
REDIS_HOST = '118.24.255.219'
REDIS_PORT = 6380