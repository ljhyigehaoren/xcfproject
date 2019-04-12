import json
import redis
import pymongo
def main():
    # 指定Redis数据库信息
    rediscli = redis.StrictRedis(host='118.24.255.219', port=6380, db=0)
    # 指定MongoDB数据库信息
    mongocli = pymongo.MongoClient(host='localhost', port=27017)
    # 指定数据库
    db = mongocli['class1809']
    # 指定集合
    sheet = db['xcf']
    while True:
        # FIFO模式为 blpop，LIFO模式为 brpop，获取键值
        source, data = rediscli.blpop("xcf:items")
        data = data.decode('utf-8')
        item = json.loads(data)
        try:
            print(item)
            sheet.insert(item)
            print ("Processing:insert successed" % item)
        except Exception as err:
            print ("err procesing: %r" % item)

import pymysql

def save_data_to_mysql():
    #redis数据库链接
    server = redis.StrictRedis(host='118.24.255.219',port=6380,db=0)
    mysql_client = pymysql.Connect(
        '127.0.0.1','root','ljh1314',
        'class1809',port=3306,charset='utf8'
    )
    cursor = mysql_client.cursor()

    for _ in range(0,1):
        key,data = server.blpop('xcf:items')
        print(key,data)
        data = data.decode('utf-8')
        jsonData = json.loads(data)
        if jsonData:
            # sql = """
            # INSERT INTO caipu (id,name,....)
            # VALUES (%s,%s,....)
            # """
            sql = """
            INSERT INTO caipu (%s)
            VALUES (%s)
            """ % (
                ','.join(jsonData.keys()),
                ','.join(['%s']*len(jsonData))
            )
            try:
                cursor.execute(sql,list(jsonData.values()))
                mysql_client.commit()
                print('插入成功')
            except Exception as err:
                print('插入失败')
                print(err)

if __name__ == '__main__':
    save_data_to_mysql()
