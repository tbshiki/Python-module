# 数値→アルファベット
# 例：26→z or Z、27→aa or AA、10000→all or ALL

#小文字
def num2a(num):
    if num <= 26:
        return chr(96 + num)
    elif num % 26 == 0:
        return num2a(num // 26-1) + chr(122)
    else:
        return num2a(num // 26) + chr(96 + num % 26)

#大文字
def num2A(num):
    if num<=26:
        return chr(64+num)
    elif num%26==0:
        return num2a(num//26-1)+chr(90)
    else:
        return num2a(num//26)+chr(64+num%26)

#参考
#https://tanuhack.com/num2alpha-alpha2num/