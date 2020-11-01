# アルファベット小文字→数値
# 例：z or Z→26、aa or AA→27、all or ALL→1000

#小文字
def a2num(alpha):
    num = 0
    for index, item in enumerate(list(alpha)):
        num += pow(26, len(alpha) - index - 1) * (ord(item) - ord('a') + 1)
    return num

#大文字
def A2num(alpha):
    num = 0
    for index, item in enumerate(list(alpha)):
        num += pow(26, len(alpha) - index - 1) * (ord(item) - ord('A') + 1)
    return num

#参考
#https://tanuhack.com/num2alpha-alpha2num/