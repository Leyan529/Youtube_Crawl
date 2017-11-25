import pandas as pd
import crawlData
from io import BytesIO
from urllib.request import urlopen

title = ['Group_Name',
         'Channel_ID',
         'Channel_Name',
         'Channel_Description',
         'SubDescription Count',
         'Vedio Count',
         'View Count',
         'Publish Date',
         'Channel Picture',
         'Vedio Publish Map']

key = ['group_name', 'channel_name', 'channel_id', 'description', 'subscriberCount',
       'videoCount',
       'viewCount', 'publishDate', 'picture'
       ]
pict_index = ['B']

def makeChannelExcel(channeList, groupList):
    df = pd.DataFrame({}, columns=title)
    df = df[title]

    writer = pd.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')
    workbook = writer.book
    worksheet = workbook.add_worksheet('Channel')

    # Add a header format.
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#F7E2BA',
        'border': 1})

    # Write the column headers with the defined format.
    for row_num, value in enumerate(df.columns.values):
        worksheet.write(row_num, 0, value, header_format)

        # Add a value format.
    value_format = workbook.add_format({
        'bold': False,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#E9A05F',
        'border': 1})

    colOffset = 1

    for col_num, dict_item in enumerate(channeList):
        for key_index, dict_key in enumerate(key):
            # print(dict_item[dict_key])
            if dict_key != 'picture':
                worksheet.write(key_index, col_num + colOffset, dict_item[dict_key], value_format)
            else:
                pict_url = dict_item[dict_key]
                image_data = BytesIO(urlopen(pict_url).read())
                worksheet.insert_image(key_index, col_num + colOffset, pict_url, {'image_data': image_data})
    writer.save()
    print(channeList)  # Excel 輸出


def writeImgToExcel(pict_url):
    writer = pd.ExcelWriter('pandas_img.xlsx', engine='xlsxwriter')
    workbook = writer.book
    worksheet = workbook.add_worksheet('Pict')
    # image = crawlData.getPicture(pict_url)
    # image.show()
    image_data = BytesIO(urlopen(pict_url).read())
    worksheet.insert_image('B2', pict_url, {'image_data': image_data})
    writer.save()
