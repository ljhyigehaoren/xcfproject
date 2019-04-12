# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from xiachufang.items import XiachufangCaiPuItem,XiachufangCategoryItem
from scrapy.http import Request
#图片下载管道
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.utils.project import get_project_settings

image_store = get_project_settings().get('IMAGES_STORE')
class XiachufnagCoverImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):

        if isinstance(item,XiachufangCaiPuItem):
            #根据图片的url地址，发起请求
            print('正在下载图片',item['coverImage'])
            coverImageUrl = item['coverImage']
            yield Request(url=coverImageUrl)

    def item_completed(self, results, item, info):
        """
        results：存放图片下在完成后的结果信息
        :param results:
        :param item:
        :param info:
        :return:
        """
        if isinstance(item, XiachufangCaiPuItem):
            """
            [
            (True, 
            {
            'url': 'http://i2.chuimg.com/bcf1f9ca2ac84e2398072ce76f_1280w_1024h.jpg?imageView2/2/w/660/interlace/1/q/90', 
            'path': 'full/7a042e41110454afe2d894579e6ca0dcc736b3b3.jpg', 
            'checksum': 'da193bcb9136279bcf28884912dc0eb5'}
            )
            ]
            """
            paths = [resultDict['path'] for status,resultDict in results if status]
            if len(paths) > 0:
                fullImagePath = image_store + '/' + paths[0]
                item['localImagePath'] = fullImagePath
            #print('图片下载结果',results)

        return item

# 切记激活管道文件（settings.py）
class XiachufangPipeline(object):

    def __init__(self,host,user,pwd,db,port,charset):
        #mysql链接
        # self.client = pymysql.Connect(
        #     '127.0.0.1','root','ljh1314',
        #     'class1809',port=3306,charset='utf8'
        # )
        self.client = pymysql.Connect(
            host, user, pwd,
            db, port=port, charset=charset
        )
        #游标
        self.cursor = self.client.cursor()

    @classmethod
    def from_settings(cls,settings):
        """
        from_settings类方法实现的目的：为了从settings.py文件中获取设置信息
        :param settings:
        :return:
        """
        MYSQL_HOST = settings['MYSQL_HOST']
        MYSQL_USER = settings['MYSQL_USER']
        MYSQL_PWD = settings['MYSQL_PWD']
        MYSQL_DB = settings['MYSQL_DB']
        MYSQL_PORT = settings['MYSQL_PORT']
        MYSQL_CHARSET = settings['MYSQL_CHARSET']

        return cls(MYSQL_HOST,MYSQL_USER,MYSQL_PWD,
                   MYSQL_DB,MYSQL_PORT,MYSQL_CHARSET)

    #最优解
    def process_item(self, item, spider):
        data = dict(item)
        sql, insert_data = item.get_sql_and_data(data)

        try:
            self.cursor.execute(sql,list(data.values()))
            self.client.commit()
            print('插入成功')
        except Exception as err:
            print(err)
            self.client.rollback()

        return item

    # def process_item(self, item, spider):
    #     """
    #     分类的item和菜谱详情的item都会经过这个方法
    #     :param item:
    #     :param spider:
    #     :return:
    #     """
    #     tablename = None
    #     if isinstance(item,XiachufangCaiPuItem):
    #         print('这是菜谱详情的item数据')
    #         tablename = 'caipu'
    #     elif isinstance(item,XiachufangCategoryItem):
    #         print('这是菜谱分类的item数据')
    #         tablename = 'category'
    #     data = dict(item)
    #     sql = """
    #     INSERT INTO %s (%s)
    #     VALUES (%s)
    #     """ % (
    #         tablename,
    #         ','.join(data.keys()),
    #         ','.join(['%s']*len(data))
    #     )
    #
    #     try:
    #         self.cursor.execute(sql,list(data.values()))
    #         self.client.commit()
    #         print('插入成功')
    #     except Exception as err:
    #         print(err)
    #         self.client.rollback()
    #
    #     return item
