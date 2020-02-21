# 数値→アルファベット大文字
# 例：26→Z、27→AA、10000→ALL

def num2alpha(num):
    if num<=26:
        return chr(64+num)
    elif num%26==0:
        return num2alpha(num//26-1)+chr(90)
    else:
        return num2alpha(num//26)+chr(64+num%26)

#参考
#https://tanuhack.com/num2alpha-alpha2num/