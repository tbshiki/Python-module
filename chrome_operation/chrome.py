from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

import platform
import time
from pathlib import Path

#cromedriverを起動
#browser_operation.chrome_start(1, 30, 60,options)
def chrome_start(seconds=1, wait=30, timeout=60, options=None):
    #\githubの絶対パスを取得
    current_dir = Path(__file__).resolve().parent.parent.parent

    if platform.system() == 'Windows': # Windows
        driver = webdriver.Chrome(executable_path=str(current_dir) + '\chromedriver\chromedriver_win32\chromedriver.exe', options=options)
    elif platform.system() == 'Darwin': # Mac
        driver = webdriver.Chrome(executable_path=str(current_dir) + '\chromedriver\chromedriver_mac64\chromedriver', options=options)
    elif platform.system() == 'Linux': # Linux
        driver = webdriver.Chrome(executable_path=str(current_dir) + '\chromedriver\chromedriver_linux64\chromedriver', options=options)

    driver.implicitly_wait(wait)  # 暗黙的な待機・要素が無い場合に最大30秒待機
    driver.set_page_load_timeout(timeout)  # ページが完全にロードされるまで最大で60秒間待つよう指定

    time.sleep(seconds)
    return driver

#コントロール押しながらクリック
#browser_operation.click_C(driver, element)
class clickC():

    def __init__(self, driver, element):

        #クリック前のハンドル数を取得
        handles = len(driver.window_handles)

        actions = ActionChains(driver)

        if platform.system() == 'Darwin':
            #Macなのでコマンドキー
            actions.key_down(Keys.COMMAND)

        else:
            #Mac以外なのでコントロールキー
            actions.key_down(Keys.CONTROL)

        actions.click(element)
        actions.perform()

        try:
            # 新しいタブが開くのを最大30秒まで待機
            WebDriverWait(driver, 30).until(lambda a: len(a.window_handles) > handles)
        except TimeoutException:
            print('新しいタブが開かずタイムアウトしました')
            sys.exit(1)

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

def chrome_scrolle(driver,scrolle_xpath,seconds=1):
    scrolle_point = driver.find_element_by_xpath(scrolle_xpath)
    actions = ActionChains(driver)
    actions.move_to_element(scrolle_point)
    actions.perform()
    time.sleep(seconds)