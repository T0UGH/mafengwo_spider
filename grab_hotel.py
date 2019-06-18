from selenium import webdriver
import time


def grab_single_hotel(browser, url):
    """获取给定url上的酒店数据
        这里使用了selenium来对抗马蜂窝的js动态加载技术
        具体的爬取步骤就不讲了
        :param browser: 通过webdriver创建的chrome浏览器的引用
        :param url: 本次要爬取的url
        :return: 酒店数据数组[h_id, name, position, img_src, in_time, out_time, hotel_size, build_time, house_name, house_price]
    """
    browser.get(url)
    time.sleep(3)
    h_id = int(url[url.rfind('/') + 1:url.rfind(".")])
    intro = browser.find_element_by_class_name("intro-hd")
    name = intro.find_element_by_class_name("main-title").text
    position = intro.find_element_by_class_name("location").text
    img_src = browser.find_element_by_class_name("intro-bd").find_element_by_class_name("img-big").find_element_by_tag_name("img").get_attribute('src')
    tail = img_src.find("?")
    img_src = img_src = img_src[:tail] if tail != -1 else img_src
    infos = browser.find_element_by_class_name("hotel-info").find_element_by_class_name("info-section").find_elements_by_class_name("cell")
    print(name)
    print(position)
    build_time = in_time = out_time = hotel_size = None
    for info in infos:
        label = info.find_element_by_class_name("label").text
        content = info.find_element_by_class_name("content").text
        if label == "入住时间:":
            in_time = content
        elif label == "建成于:":
            build_time = content
        elif label == "离店时间:":
            out_time = content
        elif label == "酒店规模:":
            hotel_size = content

    books = browser.find_element_by_class_name("book-list").find_elements_by_class_name("_j_booking_item")
    house_name = house_price = None
    if len(books) > 0:
        book = books[1]
        house_name = book.find_element_by_class_name("low-room").text
        house_price = book.find_element_by_class_name("price").text
    print(img_src)
    print(in_time)
    print(out_time)
    print(build_time)
    print(hotel_size)
    print(house_name)
    print(house_price)
    return [h_id, name, position, img_src, in_time, out_time, hotel_size, build_time, house_name, house_price]


if __name__ == '__main__':
    browser = webdriver.Chrome()
    url = "http://www.mafengwo.cn/hotel/99169.html"
    browser.close()


