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


def channel_detail():
    print()


def get_channel_subsubscribers(channel_id):
    url = 'https://www.googleapis.com/youtube/v3/channels?part=statistics'
    url = url + '&id=' + channel_id
    url = url + '&key=' + DEVELOPER_KEY
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    d = json.loads(soup.text)
    return int(d['items'][0]['statistics']['subscriberCount'])


# query = search Field , condition = By where ,argu = 條件值 , forAll(查詢全部) [True:False]
def search(query, condition, value, forAll , order):
    if query == Protocol.channelId and condition == Protocol.channelName:
        channelName = value
        return getchannelId_bychannelName(channelName)

    elif query == Protocol.video and condition == Protocol.channelName:
        channelName = value
        getVideo_byChannelName(channelName,forAll)


    elif query == Protocol.channelName and condition == Protocol.favroiteType:
        typeName = value
        getChannel_byFavroiteType(typeName)


def getChannel_byFavroiteType(typeName):
    channeList = []
    # to-do
    print(typeName + ' Searching start...\n')
    url = 'https://www.googleapis.com/youtube/v3/search?part=snippet'
    url = url + '&q=' + typeName
    url = url + '&max-results=' + '3'
    url = url + '&order=' + 'viewCount'
    url = url + '&type=' + 'channel'
    url = url + '&key=' + DEVELOPER_KEY
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    d = json.loads(soup.text)
    search_result = d['items']
    token = d['nextPageToken']

    for item in search_result:
        # getChannelDetail
        print(item['snippet']['title'] + item['snippet']['channelId'])
        search(Protocol.video, Protocol.channelName, item['snippet']['title'],False ,None)
    #
    return channeList


def getVideo_byChannelName(channelName,forAll):
    print(channelName + ' Searching start...\n')
    videos = []
    channelId = search(Protocol.channelId, Protocol.channelName, channelName , True , None)
    token = ''
    index = 0
    while True:
        url = 'https://www.googleapis.com/youtube/v3/search?part=snippet'
        url = url + '&q=' + channelName
        url = url + '&channelId=' + channelId
        url = url + '&max-results=' + '50'
        url = url + '&order=' + 'date'
        url = url + '&type=' + 'video'
        url = url + '&pageToken=' + token
        url = url + '&key=' + DEVELOPER_KEY
        data = requests.get(url)
        soup = BeautifulSoup(data.text, 'html.parser')
        d = json.loads(soup.text)
        search_result = d['items']
        token = d['nextPageToken']

        for item in search_result:
            if condition.filter(item, channelName) == True:
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
            token = ''
            break


def getchannelId_bychannelName(channelName):
    url = 'https://www.googleapis.com/youtube/v3/search?part=snippet'
    url = url + '&q=' + channelName
    url = url + '&max-results=' + '10'
    if channelName == 'EXO':
        url = url + '&order=' + 'videoCount'
    else:
        url = url + '&order=' + 'relevance'
    url = url + '&type=' + 'channel'
    url = url + '&key=' + DEVELOPER_KEY
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    d = json.loads(soup.text)
    max = {}
    max['number'] = 0
    search_result = d['items']
    for items in search_result:
        subNumber = get_channel_subsubscribers(items['snippet']['channelId'])
        if subNumber > max['number']:
            max['title'] = items['snippet']['channelTitle']
            max['channel'] = items['snippet']['channelId']
            max['number'] = subNumber
    # print(max['title'])
    return max['channel']
