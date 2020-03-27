from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

import platform
import time

#コントロール押しながらクリック
#browser_operation.click_C(driver, element)
class clickC():

    def __init__(self, driver, element):

        #クリック前のハンドル数を取得
        handle = len(driver.window_handles)

        actions = ActionChains(driver)

        if platform.system() == 'Darwin':
            #Macなのでコマンドキー
            actions.key_down(Keys.COMMAND)

        else:
            #Mac以外なのでコントロールキー
            actions.key_down(Keys.CONTROL)

        actions.click(element)
        actions.perform()

        WebDriverWait(driver, 30).until(lambda a: len(driver.window_handles) > handle)

        time.sleep(1)

    #コントロール押しながらクリックして一番右のタブに移動
    def rightmost(driver, element):
        clickC(driver, element)
        driver.switch_to.window(driver.window_handles[-1])

    def switchnew(driver, element):
        handle_list_befor = driver.window_handles
        clickC(driver, element)
        handle_list_after = driver.window_handles
        handle_list_new = list(set(handle_list_after) - set(handle_list_befor))
        driver.switch_to.window(handle_list_new[0])