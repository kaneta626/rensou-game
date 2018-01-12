#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gensim.models import word2vec
from nltk.corpus import wordnet as wn
import re
import random
import networkx as nx
import simplejson as json

#word2vecを用いて連想関係を作成し、wordnetを用いて単語間の連想関係を調べる
class Rensou:
    def __init__(self, word1, word2):
        self.word1 = word1
        self.word2 = word2
        self.str_list = []
        
        self.model = word2vec.Word2Vec.load("sampleJA.model")
        self.graph = nx.DiGraph()
        
        self.make_list(self.word1, self.word2)
        self.make_graph(self.str_list)
    
    #グラフを作るためのリスト作成、現在、1000単語
    #学習に時間がかかる際は、ここの単語数を少なくすると早く実行できる。しかし、精度は落ちる
    def make_list(self, word1, word2):
        str_list = [word1, word2]
        rand_list = sorted(self.model.wv.vocab.keys())
        random.shuffle(rand_list)
        str_list += rand_list[0:998]
        self.str_list = str_list
    
    #wordnetを使用する際に、文字を加工する
    #例.Synset('edible_fruit.n.01') → edible_fruit.n.01
    def make_word(self, word):
        maped_word = map(str, word)
        str_word = ','.join(maped_word)
        str_word = re.sub(r'\[', "",str_word)
        str_word = re.sub(r'\]', "",str_word)
        str_word = re.sub(r'Synset\(\'', "",str_word)
        str_word = re.sub(r'\'\)', "",str_word)
        str_word = re.sub(r'\,', " ",str_word)
        return str_word

    #wordnetでカテゴリ分けするのに英語の状態に戻す
    #例.'リンゴ' → ['apple.n.01', 'apple.n.02']
    def transJE(self, word):
        word = wn.synsets(word, lang='jpn')
        maped_word = map(str, word)
        str_word = ','.join(maped_word)
        str_word = re.sub(r'\[', "",str_word)
        str_word = re.sub(r'\]', "",str_word)
        str_word = re.sub(r'Synset\(\'', "",str_word)
        str_word = re.sub(r'\'\)', "",str_word)
        word_list = str_word.split(",")
        return word_list

    #このメソッドを用いて、wordnetのカテゴリ分けを行う
    #make_word()メソッドとtransJE()メソッドが必要
    def category(self, word1, word2):
        try:
            word1 = self.transJE(word1)
            word2 = self.transJE(word2)
            word = wn.synset(word1[0])
            word = word.lowest_common_hypernyms(wn.synset(word2[0]))
            str_word = self.make_word(word)
            str_word = wn.synset(str_word).lemma_names('jpn')
            return str_word
        except Exception as e:
            str_word = ['error']
            return str_word
    
    #連想関係を調べるためのネットワークを作成
    #make_list()メソッドで作成したリストを引数に使用
    #https://qiita.com/uppers12/items/49080dd74eccbde02119 を参照
    def make_graph(self, str_list):
        for x in str_list:
            self.graph.add_node(x)

        for x in str_list:
            for y in str_list:
                wait = pow(1 - self.model.similarity(x, y),2)
                self.graph.add_edge(x, y, weight=wait)

        json.dump(dict(nodes=[[n, self.graph.node[n]] for n in self.graph.nodes()],
                           edges=[[u, v, self.graph.edge[u][v]] for u,v in self.graph.edges()]),
                      open('graph.json', 'w'), indent=2 )

        d = json.load(open('graph.json'))
        self.graph.add_nodes_from(d['nodes'])
        self.graph.add_edges_from(d['edges'])
        
    #結果の表示
    def relation(self):
        try:
            self.graph.remove_edge(self.word1, self.word2)
            data = nx.dijkstra_path(self.graph, self.word1, self.word2)
            wait = pow(1 - self.model.similarity(self.word1, self.word2),2)
            self.graph.add_edge(self.word1, self.word2, weight=wait)
        
            new_data = []
            for i in range(len(data)):
                new_data.append(data[i])
                if(i+1 < len(data)):
                    new_data.append(self.category(data[i], data[i+1]))
        
            return new_data
        except Exception as e:
            error_word = str(e).replace("word '","").replace("' not in vocabulary","")
            return error_word + "は登録されていない単語です"
        
