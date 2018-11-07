import math
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from bs4 import BeautifulSoup
import re
import requests
import urllib, urllib.error
import os
import argparse
import sys
import json
import time

accessFreq = 2

def testModule():
    
    name = "あnikingo"
    encodedName = urllib.parse.quote(name)
    print(encodedName)


def get_soup(url,header):

    #Request オブジェクトを作成
    url = urllib.request.Request(url,headers=header)

    #urlopenでリクエストを送り、http.client.HTTPResponse オブジェクトを取得、スープへパース
    return BeautifulSoup(urllib.request.urlopen(url),'html.parser')

def dlImage(save_directory, i, img , Type):
    try:
        Type = Type if len(Type) > 0 else 'jpg'
        print("Downloading image {} ({}), type is {}".format(i, img, Type))

        #画像のダウンロード・データとして格納
        raw_img = urllib.request.urlopen(img).read()

        #画像を保管するためのファイルストリームを開く
        f = open(os.path.join(save_directory , "img_"+str(i)+"."+Type), 'wb')

        #ファイルストリーム経由で画像データをファイルに保存
        f.write(raw_img)
        f.close()

    except Exception as e:
        print ("could not load : " + img)
        print (e)

#query = "python"
#save_directory = os.getcwd() + "/img"
#max_images = 3

def main(args):
    parser = argparse.ArgumentParser(description='Options for scraping Google images')
    parser.add_argument('-s', '--search', default='banana', type=str, help='search term')
    parser.add_argument('-n', '--num_images', default=10, type=int, help='num of images to scrape')
    parser.add_argument('-o', '--directory', default=os.getcwd() + "/img", type=str, help='output directory')
    args = parser.parse_args()

    ## 複数のキーワードを"+"で繋げる
    #splitでスペース区切りを自動でリストに分ける
    query = args.search.split()

    dirName = '_'.join(query)

    query = [urllib.parse.quote(s) for s in query]

    #"+"を区切り文字に再連結
    query = '+'.join(query)

    print(query)

    #最大画像数
    max_images = args.num_images

    # 画像をフォルダーでグループする
    save_directory = args.directory + '/' + dirName
    if not os.path.exists(save_directory):
        os.makedirs(save_directory) 


    url="https://www.google.co.jp/search?q="+query+"&source=lnms&tbm=isch"
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

    soup = get_soup(url, header)

    #imgデータ用のリストを作成
    ActualImages = []

    #画像ダウンロードのための情報があるタグすべて抽出、リスト化
    imgArea = soup.find_all("div",{"class":"rg_meta"})

    #画像ファイルのリンクとファイル形式情報を取得
    for tag in imgArea:

        #取得したsoupオブジェクトのテキスト部がjson形式なため、pythonのデータ形式へ脱直列化
        jsonDict = json.loads(tag.text)

        #画像リンク(ou要素)と画像形式(ity要素)を取得
        link , Type =jsonDict["ou"]  ,jsonDict["ity"]

        #imgデータのリストとして作成
        ActualImages.append((link,Type))


    #各画像ファイル情報に対し、ダウンロードを実行
    for i , (img , Type) in enumerate( ActualImages[0:max_images]):
        dlImage(save_directory, i, img, Type)
        #アクセス頻度を制限
        time.sleep(accessFreq)


if __name__ == '__main__':
    from sys import argv
    try:
        main(argv)
        #testModule()
    except KeyboardInterrupt:
        pass
    sys.exit()

