# -*- coding: utf-8 -*-
import unicodedata
import difflib

def main(str1,str2):
    # unicodedata.normalize() で全角英数字や半角カタカナなどを正規化する
    normalized_str1 = unicodedata.normalize('NFKC', str1)
    normalized_str2 = unicodedata.normalize('NFKC', str2)

    # 類似度を計算、0.0~1.0 で結果が返る
    s = difflib.SequenceMatcher(None, normalized_str1, normalized_str2).ratio()
    return s

if __name__=="__main__":
    main()

#参考
#https://blog.mudatobunka.org/entry/2016/05/08/154934