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
    if keyword!='':
        result = condition_default(data, keyword)
    else:
        result = condition_normal(data)
    return result

def condition_default(data, filter):
    if data['id']['kind'] == 'youtube#video' and \
            ('MV' in data['snippet']['title'] or 'M/V' in data['snippet']['title']) and \
                    filter in data['snippet']['title'] and \
                    'Teaser' not in data['snippet']['title'] and \
                    'TEASER' not in data['snippet']['title'] and \
                    'INTRO' not in data['snippet']['title'] and \
                    'BEHIND' not in data['snippet']['title'] and \
                    'Dance Ver.' not in data['snippet']['title'] and \
                    'Special Clips' not in data['snippet']['title'] and \
                    'Dance Practice' not in data['snippet']['title'] and \
                    'Choreography' not in data['snippet']['title']:
        return True
    else:
        return False

def condition_normal(data):
    if data['id']['kind'] == 'youtube#video' and \
            ('MV' in data['snippet']['title'] or 'M/V' in data['snippet']['title']) and \
                    'Teaser' not in data['snippet']['title'] and \
                    'TEASER' not in data['snippet']['title'] and \
                    'INTRO' not in data['snippet']['title'] and \
                    'BEHIND' not in data['snippet']['title'] and \
                    'Dance Ver.' not in data['snippet']['title'] and \
                    'Special Clips' not in data['snippet']['title'] and \
                    'Dance Practice' not in data['snippet']['title'] and \
                    'Choreography' not in data['snippet']['title']:
        return True
    else:
        return False

