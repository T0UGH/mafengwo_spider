import requests
from bs4 import BeautifulSoup


def grab_travels(attraction_id):
    """获取给定景点号对应的两篇最火的游记
        这里不需要对抗动态加载js，所以使用最简单的request+bs4来进行爬取
        :param attraction_id: 景点号
        :return: 景点数据数组
    """
    headers = {
        'Host': 'www.mafengwo.cn',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Referer': 'http://www.mafengwo.cn/jd/13033/gonglve.html',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    url = "http://www.mafengwo.cn/poi/youji-" + str(attraction_id) + ".html"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    lis = soup.find_all("li", class_="post-item")
    max_size = min(len(lis), 2)
    travels_list = []
    for i in range(0, max_size):
        try:
            li = lis[i]
            # 获取标题、id、略缩内容、图片src、观看人数
            title = li.find("a", class_="title-link").string
            travels_id = li.find("a", class_="title-link").get('href')
            travels_id = int(travels_id[travels_id.rfind("/")+1:travels_id.rfind('.')])
            travels_content_cut = li.find("div", class_="post-content").string
            img_src = li.find("img", class_="lazy").get('data-original')
            img_src = img_src = img_src[:img_src.find('?')] if img_src.find('?') != -1 else img_src
            view_num = next(li.find("span", class_="status").stripped_strings)
            # 爬取文章主要内容和字数
            sub_url = "http://www.mafengwo.cn/i/" + str(travels_id) + ".html"
            print(sub_url)
            r = requests.get(sub_url, headers=headers)
            sub_soup = BeautifulSoup(r.text, 'html.parser')
            travels_content_list = [text for text in sub_soup.find(class_="post_info").stripped_strings]
            travels_content = ''
            travels_content_list = travels_content_list[:-5]
            for content in travels_content_list:
                travels_content += content
            print(travels_content)
            words_num = int(sub_soup.find(class_="vc_total").find('span').get_text())
            print(words_num)
            l = [int(travels_id), int(attraction_id), title, travels_content_cut, travels_content, int(view_num), img_src, sub_url]
            travels_list.append(l)
        except Exception as err:
            print(err)
    return travels_list


