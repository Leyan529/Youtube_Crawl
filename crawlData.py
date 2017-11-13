# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import condition
import Protocol

DEVELOPER_KEY = 'AIzaSyDWX7321N79YcXyFbulSEdU1zh1RIFM2Gg'


def vedio_detail(vedio_id):
    detail = {}
    url = "https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics"
    url = url + '&id=' + vedio_id
    url = url + '&key=' + DEVELOPER_KEY
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    d = json.loads(soup.text)
    viewCount = d['items'][0]['statistics']['viewCount']
    date = d['items'][0]['snippet']['publishedAt'][0:10]
    title = d['items'][0]['snippet']['title']
    detail['viewCount'] = viewCount
    detail['date'] = date
    detail['title'] = title
    return detail


def channel_detail(channelId):
    detail = {}
    url = "https://www.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics"
    url = url + '&id=' + channelId
    url = url + '&key=' + DEVELOPER_KEY
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    d = json.loads(soup.text)
    subscriberCount = d['items'][0]['statistics']['subscriberCount']
    videoCount = d['items'][0]['statistics']['videoCount']
    date = d['items'][0]['snippet']['publishedAt'][0:10]
    title = d['items'][0]['snippet']['title']
    detail['id'] = channelId
    detail['title'] = title
    detail['subscriberCount'] = int(subscriberCount)
    detail['videoCount'] = int(videoCount)
    detail['date'] = date
    return detail


def get_channel_subsubscribers(channel_id):
    url = 'https://www.googleapis.com/youtube/v3/channels?part=statistics'
    url = url + '&id=' + channel_id
    url = url + '&key=' + DEVELOPER_KEY
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    d = json.loads(soup.text)
    return int(d['items'][0]['statistics']['subscriberCount'])


# query = search Field , condition = By where ,argu = 條件值 , searchAll(查詢全部) [True:False] , order 排序條件 ,q 關鍵字查詢[True:False]
def search(query, condition, value, searchAll, order, stock):
    if query == 'channelId' and condition == 'channelName':
        channelName = value
        return getchannelId_bychannelName(channelName,order)

    elif query == 'video' and condition == 'channelName':
        channel = value
        vedioList = getVideo_byChannel(channel, searchAll, order, stock)
        return vedioList

    elif query == 'channelName' and condition == 'favroiteType':
        typeName = value
        channlList = getChannel_byFavroiteType(typeName, order)
        return channlList


def getChannel_byFavroiteType(typeName, order):
    # to-do
    print(typeName + ' Searching start...\n')
    url = 'https://www.googleapis.com/youtube/v3/search?part=snippet'
    url = url + '&q=' + typeName
    url = url + '&max-results=' + '3'
    url = url + '&order=' + order
    url = url + '&type=' + 'channel'
    url = url + '&key=' + DEVELOPER_KEY
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    d = json.loads(soup.text)
    search_result = d['items']
    token = d['nextPageToken']
    channeList = []
    for item in search_result:
        channelDesc = channel_detail(item['snippet']['channelId'])
        channeList.append(channelDesc)
        search(Protocol.video, Protocol.channelName, channelDesc, Protocol.searchAll_False, Protocol.order_ByViewCount,
               Protocol.stock_False)
    return channeList


def getVideo_byChannel(channel, searchAll, order, stock):
    channelName = channel['title']
    channelId = channel['id']
    print(channelName + "    " + channelId + '      Searching start...\n')
    videos = []
    # channelId = search(Protocol.channelId, Protocol.channelName, channelName, Protocol.searchAll_True, None,Protocol.stock_False)
    token = ''
    index = 0
    while True:
        url = 'https://www.googleapis.com/youtube/v3/search?part=snippet'
        if stock == True:
            url = url + '&q=' + channelName
        url = url + '&channelId=' + channelId
        url = url + '&max-results=' + '50'
        url = url + '&order=' + order
        url = url + '&type=' + 'video'
        url = url + '&pageToken=' + token
        url = url + '&key=' + DEVELOPER_KEY
        data = requests.get(url)
        soup = BeautifulSoup(data.text, 'html.parser')
        d = json.loads(soup.text)
        search_result = d['items']
        token = d['nextPageToken']
        for item in search_result:
            if condition.filter(item, channelName) == True or stock != True:
                detail = vedio_detail(item['id']['videoId'])
                videos.append('%s , publish time = %s ,viewCount = %s , %s ,jpg_source = %s , url = %s'
                              % (item['snippet']['title'],
                                 detail['date'],
                                 detail['viewCount'],
                                 item['snippet']['channelId'],
                                 item['snippet']['thumbnails']['high']['url'],
                                 "https://www.youtube.com/watch?v=" + item['id']['videoId']
                                 ))
                print(videos[index])
                index = index + 1

        if token == None or len(search_result) == 0 or len(videos) > 20:
            print(channelName + ' Searching over...\n')
            break


def getchannelId_bychannelName(channelName,order):
    url = 'https://www.googleapis.com/youtube/v3/search?part=snippet'
    url = url + '&q=' + channelName + "official"
    url = url + '&max-results=' + '10'
    # if channelName == 'EXO':
    #     url = url + '&order=' + 'videoCount'
    # else:
    #     url = url + '&order=' + 'relevance'
    url = url + '&order=' + order
    url = url + '&type=' + 'channel'
    url = url + '&key=' + DEVELOPER_KEY
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    d = json.loads(soup.text)
    max = {}
    max['number'] = 0
    search_result = d['items']
    for items in search_result:
        detail = channel_detail(items['snippet']['channelId'])
        subNumber = detail['subscriberCount']
        if int(subNumber) > max['number']:
            max['title'] = detail['title']
            max['channel'] = detail['id']
            max['number'] = detail['subscriberCount']
    print(max['title'])
    return max['channel']
