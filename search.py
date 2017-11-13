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
    try:
        token = ''
        # 使用者輸入用模糊查詢dict內的key
        Group_list = [{'Name': 'BTS', 'channelId': 'UC3IZKseVpdzPSBaWxBxundA'},
                      {'Name': 'GFRIEND', 'channelId': 'UCweOkPb1wVVH0Q0Tlj4a5Pw'},
                      {'Name': 'TWICE', 'channelId': 'UCaO6TYtlC8U5ttz62hTrZgg'},
                      {'Name': 'EXO', 'channelId': 'UCEf_Bc-KVd7onSeifS3py9g'},
                      # {'Name': 'super junior', 'channelId': 'UCEf_Bc-KVd7onSeifS3py9g'},
                      {'Name': 'Lovelyz', 'channelId': 'UCEf_Bc-KVd7onSeifS3py9g'}
                      ]
        for item in Group_list:
            item['video_list'] = crawlData.search(Protocol.video, Protocol.channelName, item['Name'])
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))


def favorite():
    try:
        token = ''
        # 使用者輸入用模糊查詢dict內的key
        Group_list = ['KPOP', 'JPOP', 'hiphop', 'Rap', '嘻哈', '抒情']

        for item in Group_list:
            crawlData.search(Protocol.channelName, Protocol.favroiteType, item , True ,None)
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
