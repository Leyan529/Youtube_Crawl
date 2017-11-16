# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import condition
import pandas as pd

DEVELOPER_KEY = 'AIzaSyDWX7321N79YcXyFbulSEdU1zh1RIFM2Gg'


def vedio_detail(vedio_id):
    detail = {}
    url = "https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics"
    url = url + '&id=' + vedio_id
    url = url + '&key=' + DEVELOPER_KEY
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    d = json.loads(soup.text)

    detail['name'] = d['items'][0]['snippet']['title']
    detail['id'] = vedio_id
    detail['url'] = "https://www.youtube.com/watch?v=" + vedio_id,
    detail['publishDate'] = d['items'][0]['snippet']['publishedAt'][0:10]
    detail['viewCount'] = d['items'][0]['statistics']['viewCount']
    detail['tags'] = d['items'][0]['snippet']['tags']
    detail['description'] = d['items'][0]['snippet']['description']
    detail['picture'] = d['items'][0]['snippet']['thumbnails']['medium']['url']
    # df = pd.DataFrame([detail], columns=detail.keys())
    # print(df.iloc[0]['viewCount'])
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


# query = search Field , condition = By where ,argu = 條件值 , searchAll(查詢全部) [True:False] , order 排序條件 ,stock 關鍵字查詢[True:False] ,Filter關鍵字
def search(query, condition, value, searchAll, order, stock, filter):
    if query == 'channelId' and condition == 'channelName':
        channelName = value
        return getchannelId_bychannelName(channelName, order)

    elif query == 'video' and condition == 'channelName':
        channel = value
        vedioList = getVideo_byChannel(channel, searchAll, order, stock, filter)
        return vedioList

    elif query == 'channelName' and condition == 'favroiteType':
        typeName = value
        channlList = getChannel_byFavroiteType(typeName, order)
        return channlList


def getChannel_byFavroiteType(typeName, order):
    # to-do
    print(typeName + ' start...\n')
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
        # search(Protocol.video, Protocol.channelName, channelDesc, Protocol.searchAll_False, Protocol.order_ByViewCount,
        #        Protocol.stock_False, None)
    return channeList


def getVideo_byChannel(channel, searchAll, order, stock, filter):
    channelName = channel['title']
    channelId = channel['id']
    print(channelName + "    " + channelId + '      Searching start...\n')
    videos = []
    rowDataList = []
    token = ''
    index = 0
    while True:
        url = 'https://www.googleapis.com/youtube/v3/search?part=snippet'
        if stock == True:
            url = url + '&q=' + filter
        else:
            url = url + '&q=' + "音樂"
        url = url + '&channelId=' + channelId
        url = url + '&max-results=' + '50'
        url = url + '&order=' + order
        url = url + '&type=' + 'video'
        url = url + '&pageToken=' + token
        url = url + '&key=' + DEVELOPER_KEY
        try:
            data = requests.get(url)
            soup = BeautifulSoup(data.text, 'html.parser')
            d = json.loads(soup.text)
            search_result = d['items']
            token = d['nextPageToken']
            for item in search_result:
                if (stock == True and condition.condition_default(item, filter) == True) or (
                                stock == False and condition.condition_normal(item) == True):
                    detail = vedio_detail(item['id']['videoId'])
                    rowData = []
                    for key in detail.keys():
                        rowData.append(detail[key])
                        # print(subDf)
                    rowDataList.append(rowData)
                    print("搜尋到第" + str(index) + "筆資料...")
                    index = index + 1

            if stock == False and (len(rowDataList) > 20 or len(rowDataList) == 0):
                if len(rowDataList) == 0:
                    print(" Searching over... , But can't found data in " + channelName + " Searching.. ")
                elif len(rowDataList) > 0:
                    print(channelName + ' Searching over...\n')
                break
            elif stock == True and (token == None or len(search_result) == 0):
                print(channelName + ' Searching over...\n')
                break
        except:
            print("Can't found data or Error " + channelName)
            break
    df = pd.DataFrame(rowDataList,
                      columns=['name', 'id', 'url', 'publishDate', 'viewCount', 'tags', 'description', 'picture'])
    return df


def getchannelId_bychannelName(channelName, order):
    url = 'https://www.googleapis.com/youtube/v3/search?part=snippet'
    url = url + '&q=' + channelName
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
