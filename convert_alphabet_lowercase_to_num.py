# アルファベット小文字→数値
def alpha2num(alpha):
    num=0
    for index, item in enumerate(list(alpha)):
        num += pow(26,len(alpha)-index-1)*(ord(item)-ord('a')+1)
    return num

#参考
#https://tanuhack.com/num2alpha-alpha2num/