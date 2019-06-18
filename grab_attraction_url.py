from selenium import webdriver
import time
import json

"""
grab_attraction_url是一个独立的脚本
它用来获取对应景点的url，并将获取到的信息存储到attraction.json中
我已经事先爬好了300个景点的url，所以轻易不要运行这个脚本，会顶掉attraction.json文件
"""

browser = webdriver.Chrome()

view_list = []

browser.get("http://js.mafengwo.net/js/hotel/sign/index.js?1552035728")
browser.get("http://www.mafengwo.cn/jd/13033/gonglve.html")
time.sleep(1)
browser.refresh()
time.sleep(1)

for _ in range(1, 21):
    if _ == 1:
        x = 6
    elif 2 <= _ <= 4:
        x = 7
    else:
        x = 8
    time.sleep(1)
    for i in range(1, 16):
        a = browser.find_element_by_xpath('//*[@id="container"]/div[4]/div/div[1]/ul/li[' + str(i) + ']/a')
        print(a.get_attribute("href"))
        view_list.append(a.get_attribute('href'))
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="container"]/div[4]/div/div[2]/div/a[' + str(x) + ']').click()

browser.close()
j = json.dumps(view_list)

print(j)

with open("attractions.json", "w") as f:
    f.write(j)


