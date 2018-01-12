#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import rensou

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def hello():
    return render_template("index.html", title="連想ゲーム")

@app.route("/result")
def result(): 
    word1 = request.args.get('text1', '')
    word2 = request.args.get('text2', '')
    rns = rensou.Rensou(word1, word2)
    answer = rns.getResult()
    return "%s"% answer

if __name__ == "__main__":
    app.run()
