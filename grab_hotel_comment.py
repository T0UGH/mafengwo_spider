from selenium import webdriver
import time

browser = webdriver.Chrome()
browser.get("http://www.mafengwo.cn/hotel/1033.html")
browser.refresh()
time.sleep(1)
txt = browser.find_element_by_class_name("txt").text
txt = txt.encode('unicode-escape')
txt = txt.replace('\/', '/')
txt = "ꌢꢚ㇫，ퟐ古城，ꈀꌦ游玩城内景。ꇎꈀ帮忙约车王院等城外景高铁站。"
print(txt)
txt.encode("utf8").decode('unicode-escape')
print(txt)
print(txt.encode("utf8"))
# browser.close()
