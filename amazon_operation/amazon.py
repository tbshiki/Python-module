from selenium import webdriver

import time

#トップページでキーワードを入力して検索ボタンをクリック
#amazon.search(driver, serch, 1)
def search(driver, search, seconds=1):
    twotabsearchtextbox = driver.find_element_by_id('twotabsearchtextbox')
    twotabsearchtextbox.clear()#入力されていればクリア
    twotabsearchtextbox.send_keys(search)
    time.sleep(seconds)

    searchsubmit = driver.find_element_by_xpath('//*[@id="nav-search-submit-text"]/input')
    searchsubmit.click()
    time.sleep(seconds)

#登録情報エリアの要素をひとつ返す
#amazon.get_tourokujyouhou(driver, li_element, parent_tag)
def get_tourokujyouhou(driver, li_element, parent_tag):
    if parent_tag == 'ul':

        text = li_element.find_element_by_xpath('span/span[1]').text
        list_text = text.split(':')
        text_heading = list_text[0].strip()

        text2 = li_element.find_element_by_xpath('span/span[2]').text
        text_contents = text2.strip()

    elif parent_tag == 'tbody':

        text = tr_element.find_element_by_xpath('th').text
        text_heading = text.strip()

        text2 = tr_element.find_element_by_xpath('td').text
        text_contents = text2.strip()

    return text_heading, text_contents