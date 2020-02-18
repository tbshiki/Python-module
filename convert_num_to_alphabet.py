# 数字からアルファベットを返す関数
# 例：26→Z、27→AA、10000→NTP

def toAlpha(num):
    if num <= 26:
        return chr(64 + num)
    elif num % 26 == 0:
        return toAlpha(num // 26 - 1) + chr(90)
    else:
        return toAlpha(num // 26) + chr(64 + num % 26)

#参考
#https://tanuhack.com/gspread-dataframe/