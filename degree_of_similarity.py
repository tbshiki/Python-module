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
#参考
#https://blog.mudatobunka.org/entry/2016/05/08/154934

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def sub(str1,str2):
    # unicodedata.normalize() で全角英数字や半角カタカナなどを正規化する
    normalized_str1 = unicodedata.normalize('NFKC', str1)
    normalized_str2 = unicodedata.normalize('NFKC', str2)

    # 類似度を計算、0.0~1.0 で結果が返る
    s = fuzz.partial_ratio(normalized_str1, normalized_str2)
    return s
#参考
#https://qiita.com/cvusk/items/7fe24e7fd74516ea3cba