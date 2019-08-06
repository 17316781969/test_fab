import time
from selenium import webdriver

def mychrome():
    browser = webdriver.Chrome(executable_path="/home/c/chromedriver")
    browser.get("http://httpbin.org/ip")
    time.sleep(9)
    browser.close()

if __name__ == '__main__':
    mychrome()
