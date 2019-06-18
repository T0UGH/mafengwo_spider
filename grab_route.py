from selenium import webdriver
import time
import pymysql

"""
这是一个独立的脚本，用来爬取旅行线路(自由行)，一般不需要再运行了
"""

browser = webdriver.Chrome()
url = "http://www.mafengwo.cn/sales/0-0-M13033-0-0-0-0-0.html?seid=1E4C8D09-1309-495F-97BA-5C0F7BAF439D"
browser.get(url)
time.sleep(3)
route_list = []
routes = browser.find_element_by_class_name("list-wrap").find_elements_by_class_name("item")
for route in routes:
    a_href = route.get_attribute("href")
    a_id = a_href[a_href .rfind("/")+1: a_href .rfind(".")]
    img_src = route.find_element_by_class_name("image").find_element_by_tag_name("img").get_attribute("src")
    info = route.find_element_by_class_name("info")
    has_saled = info.find_element_by_tag_name("p").text
    name = info.find_element_by_tag_name("h3").text
    tag = info.find_element_by_class_name("s-tag").text
    price = route.find_element_by_class_name("price").text
    print(a_id)
    print(img_src)
    print(has_saled)
    print(name)
    print(tag)
    print(price)
    route_list.append([a_id, name, price, img_src, has_saled, tag])
browser.close()


db = pymysql.connect("localhost", "root", "123456", "shanxi_tourism")
cursor = db.cursor()
for route in route_list:
    try:
        sql = "INSERT INTO route VALUES ('%d', '%s', '%s', '%s', '%s', '%s')" \
              % (int(route[0]), route[1], route[2], route[3], route[4], route[5])
        cursor.execute(sql)
        db.commit()
    except Exception as err:
        db.rollback()
        print(err)
