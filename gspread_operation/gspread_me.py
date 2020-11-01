##
# gspread_update_cells(ワークシート変数, リスト変数, 開始セル)
#
##

import pandas as pd
import gspread
import re
import sys

# モジュールのあるパスを追加
sys.path.append('../module')
#数字とアルファベットを変換
import convert_alphabet_to_num
import convert_num_to_alphabet

#https://tanuhack.com/gspread-dataframe/
#指定セルから連想配列を貼り付け
def free(worksheet, list, startcell):
    df = pd.DataFrame(list)
    col_lastnum = len(df.columns) # DataFrameの列数
    row_lastnum = len(df.index)   # DataFrameの行数

    start_cell = startcell # 列はA〜Z列限定
    start_cell_col = re.sub(r'[\d]', '', start_cell)
    start_cell_row = int(re.sub(r'[\D]', '', start_cell))

    # 展開を開始するセルからA1セルの差分
    row_diff = start_cell_row - 1
    col_diff = convert_alphabet_to_num.A2num(start_cell_col) - convert_alphabet_to_num.A2num('A')

    # DataFrameのヘッダーと中身をスプレッドシートの任意のセルから展開する
    cell_list = worksheet.range(start_cell + ':' + convert_num_to_alphabet.num2A(col_lastnum + col_diff) + str(row_lastnum + row_diff))
    for cell in cell_list:
        val = df.iloc[cell.row - 2][cell.col - 1]
        cell.value = val
    worksheet.update_cells(cell_list)

#指定セル範囲へ配列を貼り付け
#gspred.just(worksheet, list, startcell, lastcell)
def just(worksheet, list, startcell, lastcell,):
    cell_list = worksheet.range(startcell + ":" + lastcell)

    for cell, item in zip(cell_list,list):
            cell.value = item
    worksheet.update_cells(cell_list)