from selenium import webdriver
import time

"""
这个脚本用来爬取给定url的景点
"""


def get_desc(par_ele):
    """从页面中获取景点描述信息"""
    try:
        summary = par_ele.find_element_by_class_name("summary")
        return summary.text
    except:
        return None


def get_img_src(root):
    """从页面中获取景点的图片url"""
    try:
        img_src = root.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div/a/div/div[1]/img').get_attribute('src')
        return img_src
    except:
        return None


def get_base_info(par_ele):
    """从页面中获取景点的一些基本信息,包括，电话号、网址、用时参考等"""
    try:
        tel = site = use_time = None
        ul = par_ele.find_element_by_class_name("baseinfo")
        lis = ul.find_elements_by_tag_name('li')
        for li in lis:
            label = li.find_element_by_class_name("label").text
            content = li.find_element_by_class_name("content").text
            if label == "电话":
                tel = content
            elif label == "网址":
                site = content
            elif label == "用时参考":
                use_time = content
        return tel, site, use_time
    except:
        return None, None, None


def get_other_info(par_ele):
    """从页面中获取景点的其他基本信息,包括，交通、门票、开放时间"""
    try:
        traffic = ticket = open_time = None
        dls = par_ele.find_elements_by_tag_name('dl')
        for dl in dls:
            dt = dl.find_element_by_tag_name('dt').text
            dd = dl.find_element_by_tag_name('dd').text
            if dt == "交通":
                traffic = dd
            elif dt == "门票":
                ticket = dd
            elif dt == "开放时间":
                open_time = dd
        return traffic, ticket, open_time
    except:
        return None, None, None


def get_position(par_ele):
    """从页面中获取景点的位置信息"""
    try:
        position = par_ele.find_element_by_class_name("mhd").find_element_by_class_name("sub").text
        return position
    except:
        return None


def get_travels_url(root):
    """从页面中获取景点对应的游记展示页面的地址，以进一步爬取游记"""
    try:
        travels_url = root.find_element_by_link_text("查看相关游记").get_attribute('href')
        return travels_url
    except:
        return None


def get_hotels(root):
    """从页面中获取景点对应的酒店页面的地址，以进一步爬取酒店"""
    try:
        hotels = root.find_element_by_class_name("row-hotel").find_elements_by_tag_name('li')
        hotel_list = []
        for i in range(1, 3):
            a = hotels[i].find_element_by_tag_name("a").get_attribute('href')
            # s_list.append(hotels[i].find_element_by_tag_name("img").get_attribute('src'))
            # s_list.append(hotels[i].find_element_by_class_name("price").text)
            hotel_list.append(a)
        return hotel_list[0], hotel_list[1]
    except:
        return None, None


def grab_single_attraction(browser, url):
    """通过给定url爬取单个景点
        这里也是使用了selenium技术
        :param browser: 通过webdriver创建的chrome浏览器的引用
        :param url: 本次要爬取的url
        :return: 景点数据数组
    """

    browser.get(url)
    # browser.refresh()
    time.sleep(1)

    cn_name = browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[3]/h1').text
    print(cn_name)

    en_name = browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[3]/div').text
    print(en_name)

    over_view = browser.find_element_by_xpath('/html/body/div[2]/div[3]')

    img_src = get_img_src(browser)
    print(img_src)

    desc = get_desc(over_view)
    print(desc)

    tele, site, use_time = get_base_info(over_view)
    print(tele)
    print(site)
    print(use_time)

    traffic, ticket, open_time = get_other_info(over_view)
    print(traffic)
    print(ticket)
    print(open_time)

    position = get_position(over_view)
    print(position)

    travels_url = get_travels_url(browser)
    print(travels_url)

    hotel_1, hotel_2 = get_hotels(browser)
    print(hotel_1)
    print(hotel_2)
    return cn_name, en_name, img_src, desc, tele, site, use_time, traffic, ticket, open_time, position, travels_url, hotel_1, hotel_2


if __name__ == '__main__':
    browser = webdriver.Chrome()
    url = "http://www.mafengwo.cn/poi/6631445.html"
    grab_single_attraction(browser, url)
    browser.close()

