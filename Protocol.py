# Search


channel = 'channel'
channelName = 'channelName'
channlList = 'channlList'
video = 'video'
favroiteType = 'favroiteType'

searchAll_False = False
searchAll_True = True

stock_False = False
stock_True = True

order_ByViewCount = 'viewCount'
order_ByDate = 'date'
order_ByVideoCount = 'videoCount'
order_ByRelevance = 'relevance'
order_ByRating = 'rating'

# 使用者輸入用模糊查詢dict內的key
Group_list = [{'Group':'GFRIEND','Name': 'GFRIEND Official', 'channelId': 'UCRDd3x33kfF0IW6g2MRUkRw', 'Filter': 'GFRIEND MV'},
              # order_ByRelevance
              {'Group':'BTS','Name': 'BTS', 'channelId': 'UC3IZKseVpdzPSBaWxBxundA', 'Filter': 'BTS'},  # order_ByRelevance
              {'Group':'TWICE','Name': 'TWICE Official', 'channelId': 'UCaO6TYtlC8U5ttz62hTrZgg', 'Filter': 'TWICE'},
              # order_ByRelevance
              {'Group':'EXO','Name': 'EXO SMTOWN', 'channelId': 'UCEf_Bc-KVd7onSeifS3py9g', 'Filter': 'EXO'},  # order_ByRelevance
              {'Group':'Red Velvet','Name': 'Red Velvet Official', 'channelId': 'UCEf_Bc-KVd7onSeifS3py9g', 'Filter': 'Red Velvet'},
              # order_ByRelevance
              {'Group':'Lovelyz','Name': 'Lovelyz woolliment', 'channelId': 'UCoQIdt0bWPv3-_xuybJvTjQ', 'Filter': 'Lovelyz'}
              # order_ByRelevance
              ]

# 使用者輸入用模糊查詢dict內的key
Type_list = [{'TYPE': 'K-POP channel'},
             {'TYPE': '日本流行歌'},
             {'TYPE': 'HIP HOP'},
             {'TYPE': '饒舌'},
             {'TYPE': '嘻哈'},
             {'TYPE': 'C-POP'},
             ]

# 查詢回來的channel list vedio，儲存其DataFrame => 將來輸出成Excel用
# {'type':None,'channelDf': None, 'vedioListdf': None}
ChannelWithListVedio_EexcelOutput = []
