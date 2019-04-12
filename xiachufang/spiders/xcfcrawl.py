# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from xiachufang.items import XiachufangCategoryItem,XiachufangCaiPuItem
import re
from scrapy_redis.spiders import RedisCrawlSpider
"""
1.获取所有的菜单分类列表存储到数据库（url, 名称，分类的id）
2.获取菜单分类下所有的菜品详情信息，存储到数据库
"""
#通用爬虫继承自CrawlSpider
# class XcfcrawlSpider(CrawlSpider):
class XcfcrawlSpider(RedisCrawlSpider):
    name = 'xcfcrawl'
    allowed_domains = ['xiachufang.com']
    #start_urls = ['http://www.xiachufang.com/category/']
    #设置redis_key目的是为了：爬虫端从redis数据库中获取起始任务
    redis_key = 'xcfcrawl:start_urls'

    #rules是一个元祖或者列表,存放Rule规则对象
    #LinkExtractor：设置url的提取规则
    #allow：对应的是正则表达式（根据真呢规则表达式提取页面中的URL地址）
    #restrict_xpaths=(): 根据xpath路径，确定需要提取的url地址所在的标签
    #restrict_css=():根据css表达式，确定需要提取的url地址所在的标签

    rules = (
        #http://www.xiachufang.com/category/731/
        #http://www.xiachufang.com/category/40073/
        Rule(
            LinkExtractor(allow=r'.*?category/\d+'),
            #请求成功后的回调方法
            callback='parse_item',
            #是否设置跟进
            follow=True
        ),
        #菜单详情的url地址
        #http://www.xiachufang.com/recipe/45007/
        Rule(
            LinkExtractor(
                allow=r'.*?recipe/\d+',
                restrict_xpaths='//ul[@class="list"]/li'
            ),
            callback='parse_caipu_detail',
            follow=True,
        )
    )

    def parse_start_url(self, response):
        """
        获取起始任务的响应结果
        :param response:
        :return:
        """
        """
        目标：
        :param response:
        :return:
        """
        print(response.status, response.url)
        # 获取菜单单分类的url地址
        category_as = response.xpath('//div[@class="cates-list clearfix has-bottom-border pb20 mb20"]//ul/li/a')
        # （url, 名称，分类的id）
        for a_tag in category_as:
            item = XiachufangCategoryItem()
            # 名称
            item['title'] = a_tag.xpath('./text()').extract_first('')
            # url
            item['url'] = response.urljoin(a_tag.xpath('./@href').extract_first(''))
            # 分类的id
            # http://www.xiachufang.com/category/1807/
            pattern = re.compile('\d+', re.S)
            item['id'] = int(re.search(pattern, item['url']).group())
            # print(item)

            yield item


    #回调函数不再是parse方法了，而是parse_item
    #切记：在继承自CrawlSpiderz的爬虫中，一定不要
    #实现parse方法
    def parse_item(self, response):
        print('请求成功',response.status,response.url)

    def parse_caipu_detail(self,response):
        #
        print('详情请求成功', response.status, response.url)
        print('详情请求成功', response.url, response.status)
        # 详情页我们还需要获取如下字段
        """
        标题
        封面
        综合评分
        做菜人数
        菜谱发布人
        菜谱的用料 (获取到后，拼接为一个字符串）
        菜谱的做法（将步骤拼接为一个字符串）
        小贴士内容
        菜谱详情url地址
        :param response:
        :return:
        """
        # 分类id
        item = XiachufangCaiPuItem()
        item['tagId'] = response.meta['tagId']
        # print(item['tagId'],'在这里解析菜谱详情',response.url)

        # 标题
        # title = response.xpath('//h1[@class="page-title"]/text()').extract_first('')
        item['name'] = response.css('h1.page-title ::text').extract_first('').replace('\n', '').replace(' ', '')

        # 图片地址
        # coverImage = response.xpath('//div[@class="cover image expandable block-negative-margin"]/img/@src').extract_first('')
        item['coverImage'] = response.css(
            'div.cover.image.expandable.block-negative-margin > img ::attr(src)').extract_first('')

        # 综合评分
        item['score'] = float(response.xpath('//div[@class="score float-left"]/span[@class="number"]/text()').extract_first(
            '0.0'))

        # 做菜人数
        item['doitnum'] = int(response.xpath(
            '//div[@class="cooked float-left"]/span[@class="number"]/text()').extract_first('0'))

        # 菜谱发布人
        item['author'] = response.xpath('//div[@class="author"]/a[1]/span/text()').extract_first('')

        # 菜谱的用料
        # 对吓：8只;对吓：8只;对吓：8只;对吓：8只;对吓：8只
        tr_list = response.css('div.ings tr')
        used_list = []
        for tr in tr_list:
            name = ''.join(tr.css('td.name ::text').extract()).replace('\n', '').replace(' ', '')
            value = ''.join(tr.css('td.unit ::text').extract()).replace('\n', '').replace(' ', '')
            if len(value) == 0:
                value = '若干'
            used_list.append(name + ':' + value)
        item['used'] = '; '.join(used_list)

        # 菜谱的做法
        item['methodway'] = '->'.join(response.css('div.steps p.text ::text').extract())

        # 小贴士内容
        item['tipNote'] = ''.join(response.css('.tip-container > div ::text').extract()).replace('\n','').replace(' ','')
        # 详情的url地址
        item['url'] = response.url
        # 将item交给管道
        yield item
