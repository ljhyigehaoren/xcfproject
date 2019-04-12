
#pip3 intsall scrapy-redis
#实现分布式的目的：为了提高获取数据的效率

# scrapy-redis框架中redis数据库代替了scrapy
# 框架的调度器的一些功能（去重,任务存储）


#分布式爬虫分为主节点和从节点

# 主节点（共享的数据池）：不负责爬取任务，负
# 责存储任务，存储指纹，item数据；
#
# 从节点（爬虫端）：负责执行下载任务，解析数据等操作
# 下载的任务从主节点获取，拿到响应结果后，提取数据和
# 新的url，新的url会生成Request对象，这时我们会把这个
# 请求交给主节点存储，提取到的数据可以存储在redis数据库中
# 也可以存储在其他数据库中

# 分布式选择redis数据库的好处：
# 1.redis 数据库是基于内存的存储，读写数据的效率高
# 2.redis 数据库由丰富的数据类型（string、hash、list、set、zset）
# 3.redis 支持分布式


# 将scrapy爬虫修改为分布式
# step1：pip3 install scrapy-redis

#step:修改设置文件：
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
REDIS_HOST = 'redis数据库的ip'
REDIS_PORT = 'redis数据库的端口（默认6379）'

# 可选项：如果需要将爬虫获取的item数存储在redis数据库中
# 需要激活管道如下：
#'scrapy_redis.pipelines.RedisPipeline': 400,

注意：如果只修改了settings中的设置，不修改爬虫文件，
我们只用到了reids数据库存粗数据的功能，并没有实现分布式
可以实现断点爬取

如果要实现分布式爬虫，除了settings设置文件外还需要修改爬虫文件
#修改爬虫文件
第一种情况：爬虫继承自scrapy.Spider,
##### step1：则修改爬虫文件继承的类
"""
# class XcfSpider(scrapy.Spider):
class XcfSpider(RedisSpider):
"""
#####  step2：去掉start_urls，添加redis_key
"""
#start_urls = ['http://www.xiachufang.com/category/']
#设置redis_key目的是为了：爬虫端从redis数据库中获取起始任务
redis_key = 'xcf:start_urls'
"""
其他代码不变



第二种情况：爬虫继承自CrawlSpider,

##### step1：则修改爬虫文件继承的类
"""
# class XcfcrawlSpider(CrawlSpider):
class XcfcrawlSpider(RedisCrawlSpider):
"""

#####  step2：去掉start_urls，添加redis_key
"""
#start_urls = ['http://www.xiachufang.com/category/']
#设置redis_key目的是为了：爬虫端从redis数据库中获取起始任务
redis_key = 'xcfcrawl:start_urls'
"""

添加分布式爬虫的起始任务执行：
样例如下
lpush  xcfcrawl:start_urls  起始url任务

需要了解到master端redis数据库中存储的key有哪些：
爬虫名称:items   保存的是item数据
爬虫名称:dupefilter  保存的url指纹信息
爬虫名称:requests   保存待爬取的任务





