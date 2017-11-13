import re


def filter(data, keyword):
    # result = ''
    # if keyword == 'BTS':
    #     result = condition_BTS(data)
    # elif keyword == 'GFRIEND':
    #     result = condition_GFRIEND(data)
    # elif keyword == 'TWICE':
    #     result = condition_TWICE(data)
    # else:
    result = condition_default(data)
    return result


def condition_BTS(data):
    if data['id']['kind'] == 'youtube#video' and \
                    'BTS' in data['snippet']['title'] and \
                    'Official MV' in data['snippet']['title'] and \
                    'Teaser' not in data['snippet']['title'] and \
                    'TEASER' not in data['snippet']['title'] and \
                    'Choreography Version' not in data['snippet']['title']:
        return True
    else:
        return False
        # BTS
        # search_result['snippet']['channelTitle'] = ibighit
        # search_result['snippet']['channelId'] = UC3IZKseVpdzPSBaWxBxundA


def condition_GFRIEND(data):
    if data['id']['kind'] == 'youtube#video' and \
                    'GFRIEND' in data['snippet']['title'] and \
                    'MV' in data['snippet']['title'] and \
                    'Teaser' not in data['snippet']['title'] and \
                    'TEASER' not in data['snippet']['title'] and \
                    'Choreography' not in data['snippet']['title']:
        return True
    else:
        return False
        # GFriend
        # search_result['snippet']['channelTitle'] = 1theK (원더케이)
        # search_result['snippet']['channelId'] = UCweOkPb1wVVH0Q0Tlj4a5Pw


def condition_TWICE(data):
    if data['id']['kind'] == 'youtube#video' and \
                    'TWICE' in data['snippet']['title'] and \
                    'M/V' in data['snippet']['title'] and \
                    'Teaser' not in data['snippet']['title'] and \
                    'TEASER' not in data['snippet']['title'] and \
                    'INTRO' not in data['snippet']['title'] and \
                    'BEHIND' not in data['snippet']['title'] and \
                    'Dance Ver.' not in data['snippet']['title'] and \
                    'Choreography' not in data['snippet']['title']:
        return True
    else:
        return False
        # TWICE
        # search_result['snippet']['channelTitle'] = jypentertainment
        # search_result['snippet']['channelId'] = UCaO6TYtlC8U5ttz62hTrZgg


def condition_default(data):
    if data['id']['kind'] == 'youtube#video' and \
            ('MV' in data['snippet']['title'] or 'M/V' in data['snippet']['title'])and \
                    'Teaser' not in data['snippet']['title'] and \
                    'TEASER' not in data['snippet']['title'] and \
                    'INTRO' not in data['snippet']['title'] and \
                    'BEHIND' not in data['snippet']['title'] and \
                    'Dance Ver.' not in data['snippet']['title'] and \
                    'Choreography' not in data['snippet']['title']:
        return True
    else:
        return False
        # TWICE
        # search_result['snippet']['channelTitle'] = jypentertainment
        # search_result['snippet']['channelId'] = UCaO6TYtlC8U5ttz62hTrZgg
