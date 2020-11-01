#IDとパスワード/URL読み込み
from idpass.idpass import *
from idpass.url import *

from selenium import webdriver
from selenium.webdriver.support.ui import Select #セレクトボックスを扱えるよう

import time
import re
import sys
import gspread
from bs4 import BeautifulSoup

# モジュールのあるパスを追加
sys.path.append('../../module')
#スプレッドシート用関数読み込み
import gspread_update

#ログイン
#module_arzon.login(driver)
def login(driver):
    username = driver.find_element_by_name("username")
    username.clear()#入力されていればクリア
    username.send_keys(ARZON_ID)
    password = driver.find_element_by_name("password")
    password.clear()#入力されていればクリア
    password.send_keys(ARZON_PASS)
    login_button = driver.find_element_by_name("imageField")
    login_button.click()
    time.sleep(1)

#出品中商品ページに移動
#module_arzon.exhibitingpage(driver)
def exhibitingpage(driver):
    driver.find_element_by_partial_link_text("出品中の商品をみる").click()
    time.sleep(1)

#表示件数変更
#module_arzon.change_indication(driver,pagenum)
def change_indication(driver, pagenum):
    elnum = driver.find_element_by_xpath("//*[@id='exhibitlist']/div[1]/table/tbody/tr/td[3]/table/tbody/tr/td[1]/form/select")
    Select(elnum).select_by_value(pagenum)
    switch_button = driver.find_element_by_class_name("indication")
    switch_button.click()
    time.sleep(1)

#skuを入力して検索
#module_arzon.sku_serch(driver,sku)
def sku_serch(driver, sku):
    exserch = driver.find_element_by_xpath("//*[@id='exhibitlist']/form/div/input[3]")
    exserch.clear()#入力されていればクリア
    exserch.send_keys(sku)
    serch_button = driver.find_element_by_xpath("//*[@id='exhibitlist']/form/div/input[6]")
    serch_button.click()
    time.sleep(1)

#一覧の配列を取得
#module_arzon.create_exitem(driver, exnum)
def create_exitem(driver, exnum):
    segment_table = driver.find_element_by_class_name("exh") #出品一覧テーブルを取得
    segment = segment_table.find_elements_by_tag_name("tr") #出品一覧テーブルのtrタグを配列に
    exitem = []
    for i in range(int(exnum)):
        exnum_list =[]
        exnum_list.append(segment[i + 1].find_element_by_class_name("exh_date").text)
        exnum_list.append(segment[i + 1].find_element_by_xpath("//*[@id='exhibitlist']/div[2]/div/form/table/tbody/tr[" + str(i + 2) + "]/td[3]").text)
        exnum_list.append(segment[i + 1].find_element_by_xpath("//*[@id='exhibitlist']/div[2]/div/form/table/tbody/tr[" + str(i + 2) + "]/td[4]").text)
        exnum_list.append(segment[i + 1].find_element_by_class_name("tt").text.replace('\u3000', ' '))

        item_url = segment[i + 1].find_element_by_tag_name("a").get_attribute("href")
        exnum_list.append(item_url)
        cde = item_url.replace('https://www.arzon.jp/', '').replace('.html', '')
        exnum_list.append(cde[:cde.find("_")])
        exnum_list.append(cde[-(len(cde) - cde.find("_") - 1):])

        exitem.insert(len(exitem), exnum_list)
    return exitem

#個別ページに移動
#module_arzon.individualpage(driver, num)
def individualpage(driver, num):
    segment_table = driver.find_element_by_class_name("exh") #出品一覧テーブルを取得しなおし
    segment = segment_table.find_elements_by_tag_name("tr") #出品一覧テーブルのtrタグを配列に
    operate_btn = segment[num].find_element_by_class_name("operate") #配列から操作ボタンをクリック
    operate_btn.click()
    time.sleep(1)

#個別ページのデータを取得
#module_arzon.individuallist(driver)
def individuallist(driver):
    item_list = []
    ELEMENT_TUPLE = ('itemcd','itemnm','salestartdate','medianm','rectime','mediacd','makeritemcd','conditionno','condition','comment','makerprice','lowprice','price','shipping','number','rack')
    for i in ELEMENT_TUPLE:
        hidden_element = driver.find_element_by_name(i)
        hidden_element_value = hidden_element.get_attribute("value")
        item_list.append(hidden_element_value)
    return item_list

#個別ページから出品一覧に戻る
#module_arzon.individuallist_back(driver)
def individuallist_back(driver):
    item_buttons = driver.find_element_by_class_name("exhibit_button")
    backbtn = item_buttons.find_element_by_class_name("backbtn") #戻るボタン
    backbtn.click()
    time.sleep(1)

#個別ページの出品を取り止め（削除）ボタンをクリック
#module_arzon.individuallist_delete(driver)
def individuallist_delete(driver):
    item_buttons = driver.find_element_by_class_name("exhibit_button")
    stop_button = item_buttons.find_element_by_class_name("stop_exhibit") #出品を取り止め（削除）ボタン
    stop_button.click()
    time.sleep(1)
    del_button = driver.find_element_by_class_name("deletebtn")
    del_button.click()
    time.sleep(1)

#出品停止（削除）完了ページの出品中リストへ戻るをクリック
#module_arzon.returnexhibit_back(driver)
def returnexhibit_back(driver):
    return_button = driver.find_element_by_class_name("return_exhibit") #出品中リストへ戻るボタン
    return_button.click()
    time.sleep(1)

#出品検索ページで品番を入力して検索
def searchpage_num(driver, cell_list):
    itemnum = cell_list[6].value
    itemnumber = driver.find_element_by_name("itemnumber")
    itemnumber.clear()#入力されていればクリア
    itemkeyword = driver.find_element_by_name("keyword")
    itemkeyword.clear()#入力されていればクリア
    time.sleep(1)

    #品番に半角カナがあるかどうかチェックして入力
    #https://note.nkmk.me/python-re-regex-character-type/
    hankakukana_check = re.compile('[\uFF66-\uFF9F]+')
    if hankakukana_check.search(itemnum):
        driver.execute_script("document.getElementsByName('itemnumber')[0].value = '" + itemnum + "';")
    else:
        itemnumber.send_keys(itemnum)

    serch_button = driver.find_element_by_class_name("searchbtn")
    serch_button.click()
    time.sleep(1)

#出品検索ページでタイトルを入力して検索
def searchpage_title(driver, cell_list):
    itemtitle = cell_list[1].value
    itemnumber = driver.find_element_by_name("itemnumber")
    itemnumber.clear()#入力されていればクリア
    itemkeyword = driver.find_element_by_name("keyword")
    itemkeyword.clear()#入力されていればクリア
    time.sleep(1)

    #品番に半角カナがあるかどうかチェックして入力
    #https://note.nkmk.me/python-re-regex-character-type/
    hankakukana_check = re.compile('[\uFF66-\uFF9F]+')
    if hankakukana_check.search(itemtitle):
        driver.execute_script("document.getElementsByName('itemnumber')[0].value = '" + itemtitle + "';")
    else:
        itemkeyword.send_keys(itemtitle)

    serch_button = driver.find_element_by_class_name("searchbtn")
    serch_button.click()
    time.sleep(1)

#出品検索ページの情報取得してスプレッドシートに書き込み
#module_arzon.searchitem(driver, listitem, cell_list)
def searchitem(driver, worksheet,segment_list_num, listitem, cell_list):
    for i in range(len(listitem)):
        itemnum_list = []

        single_listitem_soup = listitem[i]
        single_listitem = driver.find_elements_by_id('listitem')[i]

        for j in range(len(listitem[i].find_all("ul"))):
            if 'JANコード' in listitem[i].find_all("ul")[j].text:
                ulnum = j + 1
                break

        if cell_list[1].value == single_listitem_soup.find("h3").text:

            #jan
            jan = single_listitem.find_element_by_xpath('div[2]/ul[' + str(ulnum) + ']/li[4]').text

            if not jan:
                single_listitem_soup = single_listitem = ulnum = j = None
                continue

            itemnum_list.append(jan)

            #cast
            cast = single_listitem.find_element_by_xpath("div[2]/ul[1]").text
            itemnum_list.append(cast.replace('マーケットプレイスに出品する\n女優：', ''))

            #maker
            maker = single_listitem.find_element_by_xpath("div[2]/ul[2]").text
            itemnum_list.append(maker.replace('メーカー： ', ''))

            #指定セル範囲へ配列を貼り付け
            gspread_update.row(worksheet, itemnum_list, 'X'+ str(segment_list_num + 2), 'Z' + str(segment_list_num + 2))

            #品番が空白なら入力
            if not cell_list[6].value:
                itemnum = single_listitem.find_element_by_xpath('div[2]/ul[' + str(ulnum) + ']/li[2]').text
                worksheet.update_acell('N'+ str(segment_list_num + 2), itemnum)

            break

#出品検索ページから戻る
def searchitem_back(driver):
    backbtn = driver.find_element_by_class_name("backbtn") #戻るボタン
    backbtn.click()
    time.sleep(1)

#検索結果から消し込み
def delete_check(driver, sheet_begin, soup, row):
    if '該当する商品はありません' not in soup.text:
            #出品数取得
            exnum = driver.find_element_by_class_name("detanumber1").text
            exnum = exnum.replace("件のデータ" , "")

            #表示件数変更
            if int(exnum) > 20:
                pagenum = '100'
                change_indication(driver, pagenum)

            for segment_list_num in range(int(exnum)):
                title = sheet_begin.range('E' + row).value

                segment_table = driver.find_element_by_class_name("exh") #出品一覧テーブルを取得しなおし
                segment = segment_table.find_elements_by_tag_name("tr") #出品一覧テーブルのtrタグを配列に
                r_title = segment[segment_list_num + 1].find_element_by_class_name("tt").text #タイトルを取得
                r_title = r_title.strip('非公開').strip('【発売中止】')

                if title.strip() == r_title.strip():
                    flag_del = '○'

                    #個別ページに移動
                    individualpage(driver, segment_list_num + 1)
                    #個別ページの商品を削除
                    individuallist_delete(driver)

                    soup2 = BeautifulSoup(driver.page_source, features="html.parser")
                    if '選択された出品を停止しました' not in soup2.text:
                        flag_del = '消し込みできてないかも'

                    #出品停止（削除）完了ページの出品中リストへ戻るをクリック
                    returnexhibit_back(driver)
                    break
                else:
                    flag_del = 'タイトルが違う'

    else:
        flag_del = '該当なし'

    return flag_del

def main():
    print('hogehoge')