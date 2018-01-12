# rensou-game
word2vecで連想ゲーム作ってみた  


概要：  
word2vecを用いて、2つの単語がどうやって連想されていくのか調べてみた  
連想をword2vecで実装し、連想結果をwordnetのhypernym()で調べる  

実行環境：  
python == 3.6.1  
numpy == 1.13.3+mkl  
scipy == 1.0.0rc2  
gensim == 3.1.0  
nltk == 3.2.5  
networkx == 1.11  
scikit-learn == 0.19.0  
Flask == 0.12.2  

使い方:  
1.http://github.com/Hirosan/ja.text8/ よりja.text8.zipをダウンロードする  
2.gakushu.pyを実行し,sampleJA.modelを作成する  
3.app.pyを実行  
4.http://127.0.0.1:5000/ を開く  
5.二つの単語を入力して、実行ボタンを押す  

問題点：  
・時間が1～2分かかる  
・wordnetによるカテゴリ分類が不完全  
・word2vecによる連想が不完全  

作成者：  
Ono hodaka  
Kaneta hirotaka  
Takahashi chinatsu  

word2vecの学習をする際に参考にさせていただいたサイト  
http://hironsan.hatenablog.com/entry/japanese-text8-corpus  
word2vecを用いた連想を行うのに参考にさせていただいたサイト  
https://qiita.com/uppers12/items/49080dd74eccbde02119  
