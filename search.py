# -*- coding: utf-8 -*-
# !/usr/bin/python

# This sample executes a search request for the specified search term.
# Sample usage:
#   python search.py --q=surfing --max-results=10
# NOTE: To use the sample, you must provide a developer key obtained
#       in the Google APIs Console. Search for "REPLACE_ME" in this code
#       to find the correct place to provide that key..

import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import crawlData
from skimage import io
import Protocol
import time
import factory



def showImg(img_src):
    image = io.imread(img_src)
    io.imshow(image)
    io.show()


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = 'AIzaSyDWX7321N79YcXyFbulSEdU1zh1RIFM2Gg'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                developerKey=DEVELOPER_KEY)


def mv_download():
    # try:
    start = float(time.time())
    channelList =[]
    for index,item in enumerate(Protocol.Group_list):
        channelDf = crawlData.search(Protocol.channel, Protocol.channelName, item['Name'],
                                     Protocol.searchAll_True, Protocol.order_ByRelevance, None, None)
        channelDf['group_name'] = item['Group'] #塞入團名
        item['channel'] = channelDf
        dict = channelDf.to_dict()
        channelList.append(dict)
        vedioListDf = crawlData.search(Protocol.video, Protocol.channelName, channelDf,
                              Protocol.searchAll_True, Protocol.order_ByDate, Protocol.stock_True,
                              item['Filter'])
        item['vedioList'] = vedioListDf
        # print(vedioListDf)
    factory.makeChannelExcel(channelList)
    end = float(time.time())
    print("執行時間 : " + str(end - start) + " s")
    # except HttpError as e:
    #     print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))


def favorite():
    try:
        start = float(time.time())
        for index, item in enumerate(Protocol.Type_list):
            favoriteType = item['TYPE']
            if favoriteType == 'K-POP channel':
                channeListDf = crawlData.search(Protocol.channlList, Protocol.favroiteType, favoriteType,
                                              Protocol.searchAll_True, Protocol.order_ByViewCount, Protocol.stock_False,
                                              None)
            else:
                channeListDf = crawlData.search(Protocol.channlList, Protocol.favroiteType, favoriteType,
                                              Protocol.searchAll_True, Protocol.order_ByRelevance, Protocol.stock_False,
                                              None)

            Protocol.Type_list[index]['ChannelList'] = channeListDf

            for i in range(0,len(channeListDf)):
                channelDf = channeListDf.loc[i]
                channelDict = channelDf.to_dict()
                vedioListdf = crawlData.search(Protocol.video, Protocol.channlList, channelDict, Protocol.searchAll_False,
                                      Protocol.order_ByRelevance,
                                      Protocol.stock_False, None)
                Protocol.ChannelWithListVedio_EexcelOutput.append({'type': favoriteType, 'channelDf': channelDf})
                print(vedioListdf) #用Excel 獨立輸出 vedioListdf_withFavorite
            print(Protocol.ChannelWithListVedio_EexcelOutput) #由List 取得對應的Key後，用Excel 輸出
        end = float(time.time())
        print("執行時間 : " + str(end - start) + " s")
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
