# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import condition
import pandas as pd
import Protocol
import requests as req
from PIL import Image
from io import BytesIO

DEVELOPER_KEY = 'AIzaSyDWX7321N79YcXyFbulSEdU1zh1RIFM2Gg'


def vedio_detail(vedio_id):
    detail = {'name': '', 'vedio_id': '', 'url': '', 'publishDate': '', 'viewCount': '', 'tags': '', 'description': '',
              'picture': '', 'Is DownLoad?': ''}
    try:
        url = "https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics"
        url = url + '&id=' + vedio_id
        url = url + '&key=' + DEVELOPER_KEY
        data = requests.get(url)
        soup = BeautifulSoup(data.text, 'html.parser')
        d = json.loads(soup.text)

        detail['name'] = d['items'][0]['snippet']['title']
        detail['vedio_id'] = vedio_id
        detail['url'] = "https://www.youtube.com/watch?v=" + vedio_id
        detail['publishDate'] = d['items'][0]['snippet']['publishedAt'][0:10]
        detail['viewCount'] = d['items'][0]['statistics']['viewCount']
        detail['tags'] = d['items'][0]['snippet']['tags']
        detail['description'] = d['items'][0]['snippet']['description']
        detail['picture'] = d['items'][0]['snippet']['thumbnails']['medium']['url']
        detail['Is DownLoad?'] = 'N'
    except:
        vedio_detail_error = True
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
    detail['group_name'] = ''
    detail['channel_name'] = d['items'][0]['snippet']['title']
    detail['channel_id'] = channelId
    detail['description'] = d['items'][0]['snippet']['description']
    detail['subscriberCount'] = int(d['items'][0]['statistics']['subscriberCount'])
    detail['videoCount'] = int(d['items'][0]['statistics']['videoCount'])
    detail['viewCount'] = int(d['items'][0]['statistics']['viewCount'])
    detail['publishDate'] = d['items'][0]['snippet']['publishedAt'][0:10]
    detail['picture'] = d['items'][0]['snippet']['thumbnails']['default']['url']
    return detail


def get_channel_subsubscribers(channel_id):
    url = 'https://www.googleapis.com/youtube/v3/channels?part=statistics'
    url = url + '&id=' + channel_id
    url = url + '&key=' + DEVELOPER_KEY
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    d = json.loads(soup.text)
    return int(d['items'][0]['statistics']['subscriberCount'])


def getPicture(url):
    response = req.get(url)
    image = Image.open(BytesIO(response.content))
    return image


# query = search Field , condition = By where ,argu = 條件值 , searchAll(查詢全部) [True:False] , order 排序條件 ,stock 關鍵字查詢[True:False] ,Filter關鍵字
def search(query, condition, value, searchAll, order, stock, filter):
    if query == 'channel' and condition == 'channelName':
        channelName = value
        return getchannel(channelName, order)

    elif query == 'video' and condition == 'channelName':
        channel = value
        vedioList = getVideo(channel, searchAll, order, stock, filter)
        return vedioList

    elif query == 'channlList' and condition == 'favroiteType':
        typeName = value
        channlList = getChannelByType(typeName, order)
        return channlList


def getChannelByType(typeName, order):
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
    # token = d['nextPageToken']
    channeList = []
    # dfList=[]
    for item in search_result:
        channelDesc = channel_detail(item['snippet']['channelId'])
        # channeList.append(channelDesc)
        rowData = []
        for key in channelDesc.keys():
            rowData.append(channelDesc[key])
        channeList.append(rowData)

    df = pd.DataFrame(channeList,
                      columns=['channel_name', 'channel_id', 'description', 'subscriberCount', 'videoCount',
                               'viewCount', 'publishDate', 'picture'
                               ])
    # print(df)
    print(typeName + "搜尋完成")
    return df


def getVideo(channel, searchAll, order, stock, filter):
    channelName = channel['channel_name']
    channelId = channel['channel_id']
    print(channelName + "    " + channelId + '      Searching start...\n')
    print("搜尋" + channelName + "下的MV影片...")
    videos = []
    rowDataList = []
    token = ''
    index = 1
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
                    rowDataList.append(rowData)
                    print("搜尋到第" + str(index) + "筆MV影片...")
                    index = index + 1

            if stock == False and (len(rowDataList) > 20 or len(rowDataList) == 0):
                if len(rowDataList) == 0:
                    print("找不到任何MV影片在" + channelName + "頻道之下...")
                elif len(rowDataList) > 0:
                    print(channelName + '該頻道所有MV影片已搜尋完成，搜尋完畢...\n')
                break
            elif stock == True and (token == None or len(search_result) == 0):
                print(channelName + '該頻道所有MV影片已搜尋完成\n')
                break
        except:
            # print("找不到任何MV影片在" + channelName + "頻道之下...")
            print("error")
            break
    df = pd.DataFrame(rowDataList,
                      columns=['name', 'id', 'url', 'publishDate', 'viewCount', 'tags', 'description', 'picture',
                               'Is DownLoad?'])
    return df


def getchannel(group, order):
    print("搜尋" + group + "頻道中...")
    url = 'https://www.googleapis.com/youtube/v3/search?part=snippet'
    url = url + '&q=' + group
    url = url + '&max-results=' + '5'
    if group == 'BTS':
        order = Protocol.order_ByViewCount
    url = url + '&order=' + order
    url = url + '&type=' + 'channel'
    url = url + '&key=' + DEVELOPER_KEY
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    d = json.loads(soup.text)
    search_result = d['items']
    channeList = []
    i = 1
    for items in search_result:
        detail = channel_detail(items['snippet']['channelId'])
        print("找到相似的頻道，為第" + str(i) + "筆")
        i = i + 1
        rowData = []
        for key in detail.keys():
            rowData.append(detail[key])
        channeList.append(rowData)

    df = pd.DataFrame(channeList,
                      columns=['group_name', 'channel_name', 'channel_id', 'description', 'subscriberCount',
                               'videoCount',
                               'viewCount', 'publishDate', 'picture'
                               ])
    channel = df.loc[df['subscriberCount'].idxmax()]
    print("搜尋完成，" + group + "的頻道為" + channel['channel_name'])
    # channel['group_name'] = group
    return channel
