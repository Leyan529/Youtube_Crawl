import pandas as pd

title=['Group_Name',
      'Channel_ID',
        'Channel_Name' ,
        'Channel_Description',
        'SubDescription Count',
        'Vedio Count',
        'View Count',
        'Publish Date' ,
        'Channel Picture',
        'Vedio Publish Map']

def makeChannelExcel(list):
    df = pd.DataFrame({}, columns=title)
    df = df[title]

    writer = pd.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')
    workbook = writer.book
    for index , channel in enumerate(list):
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

        for col_num, dict_item in enumerate(list):
            for key_index, dict_key in enumerate(title):
                worksheet.write(key_index, col_num + colOffset, dict_item[dict_key], value_format)

    writer.save()
    print(list)  # Excel 輸出