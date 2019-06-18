import json
import time
import pymysql
from selenium import webdriver

from grab_hotel import grab_single_hotel
from grab_single_attraction import grab_single_attraction
from grab_travels import grab_travels

START = 51
STEP = 5


# 爬取给定url上的景点数据并存储到数据库
def insert_attraction(browser, attraction_url, db):
    try:
        cn_name, en_name, img_src, desc, tele, site, use_time, traffic, ticket, open_time\
                , position, travels_url, hotel_1, hotel_2 = grab_single_attraction(browser, attraction_url)
        a_id = int(attraction_url[attraction_url.rfind("/") + 1:attraction_url.rfind('.')])
    except Exception as err:
        raise Exception()
    try:
        sql = "INSERT INTO attraction VALUES ('%d', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%d')" \
                  % (a_id, cn_name, en_name, img_src, desc, tele, site,
                     use_time, traffic, ticket, open_time, hotel_1, hotel_2, travels_url, i)
        cursor.execute(sql)
        db.commit()
    except Exception as err:
        db.rollback()
        raise Exception()


# 爬取给定景点id对应的两篇游记并存储到数据库
def insert_travels(attraction_id, db):
    travels = grab_travels(attraction_id)
    for travel in travels:
        try:
            sql = "INSERT INTO travels VALUES ('%d', '%d', '%s', '%s', '%s', '%d', '%s', '%s')" \
                  % (travel[0], travel[1], travel[2], travel[3], travel[4], travel[5], travel[6], travel[7])
            cursor.execute(sql)
            db.commit()
        except Exception as err:
            db.rollback()
            print(err)


# 爬取给定url的酒店并存储到数据库
def insert_hotel(browser, hotel_url, db):
    try:
        hotel = grab_single_hotel(browser, hotel_url)
        try:
            sql = "INSERT INTO hotel VALUES ('%d', '%d', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                  % (hotel[0], attraction_id, hotel[1], hotel[2], hotel[3], hotel[4], hotel[5], hotel[6], hotel[7], hotel[8], hotel[9])
            cursor.execute(sql)
            db.commit()
        except Exception as err:
            db.rollback()
            print(err)
    except Exception as err:
        print(err)


# 从数据库中获取对应景点的两个酒店链接
def get_hotel_url_from_db(attraction_id, db):
    try:
        sql = "SELECT attraction_id,attraction_hotel_url_1, attraction_hotel_url_2 FROM attraction WHERE attraction_id = %d" % attraction_id
        cursor.execute(sql)
        attr = cursor.fetchone()
        if attr is not None:
            return attr[1], attr[2]
        else:
            return None, None
    except Exception as err:
        print(err)
        return None, None


if __name__ == '__main__':
    # 初始化数据库
    db = pymysql.connect("localhost", "root", "123456", "shanxi_tourism")
    cursor = db.cursor()

    # 读取景点url文件
    with open("attractions.json", encoding="utf8") as file:
        attraction_urls = json.load(file)

    # 初始化浏览器
    browser = webdriver.Chrome()
    browser.get("http://www.mafengwo.cn/poi/6631445.html")
    browser.refresh()
    time.sleep(1)

    # 爬取每个景点的信息，及相关酒店信息，及相关游记
    for i in range(START, START + STEP):
        try:
            attraction_url = attraction_urls[i]
            attraction_id = int(attraction_url[attraction_url.rfind("/") + 1:attraction_url.rfind('.')])
            insert_attraction(browser, attraction_url, db)
            insert_travels(attraction_id, db)
            hotel_url_1, hotel_url_2 = get_hotel_url_from_db(attraction_id, db)
            if hotel_url_1 is not None:
                insert_hotel(browser, hotel_url_1, db)
            if hotel_url_2 is not None:
                insert_hotel(browser, hotel_url_2, db)
            print(i, "finish")
        except:
            print(i, "err")
            continue

    # 关闭数据库的连接并关闭浏览器
    db.close()
    browser.close()



