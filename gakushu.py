# -*- coding: utf-8 -*-
from gensim.models import word2vec
import logging
# 進捗表示用
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
 
# Word2Vecの学習に使用する分かち書き済みのテキストファイルの準備
sentences = word2vec.Text8Corpus('ja.text8')
 
# Word2Vecのインスタンス作成
# sentences : 対象となる分かち書きされているテキスト
# size      : 出力するベクトルの次元数
# min_count : この数値よりも登場回数が少ない単語は無視する
# window    : 一つの単語に対してこの数値分だけ前後をチェックする
model = word2vec.Word2Vec(sentences, size=200, min_count=20, window=15)
 
# 学習結果を出力する
model.save("sampleJA.model")
 
if __name__ == '__main__':
    print ("Finish!!!")