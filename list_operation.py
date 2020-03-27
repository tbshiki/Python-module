#リストを逆順に
def reverse_list(list):
    for i in range(len(list) // 2):
        list[i],list[-1-i] = list[-1-i],list[i]

#参考 https://qiita.com/take333/items/b61e43c68751260689a6