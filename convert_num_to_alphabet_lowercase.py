# 数値→アルファベット小文字
# 例：26→z、27→aa、10000→all

def num2alpha(num):
    if num <= 26:
        return chr(96 + num)
    elif num % 26 == 0:
        return num2alpha(num // 26-1) + chr(122)
    else:
        return num2alpha(num // 26) + chr(96 + num % 26)

#参考
#https://tanuhack.com/num2alpha-alpha2num/