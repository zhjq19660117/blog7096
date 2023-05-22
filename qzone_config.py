# qzone_spider QQ空间动态分享 参数设置和基础工具函数
import pandas as pd

# 参数区
data_qzone = {
    'user': [],
    'date': [],
    'info': [],
    'title': [],
    'note': [],
    'link': []
}
df_header = ['user', 'date', 'info', 'title', 'note', 'link']
df_qzone = pd.DataFrame(data_qzone)

# QQ空间动态分享记录缓存变量
# users = [], dates = [], infos = [], titles = [], notes = [], links = []


# 工具函数区
def is_zero(xpath_li):
    # 判断temp.xpath('.//div[@class="f-nick"]/a/text()') 解析内容是否为空值
    # 如果为空，则返回‘0’，如果不为空，则返回解析内容
    qzone_single_info = xpath_li
    # print(len(qzone_single_info))
    # print(type(qzone_single_info))

    if len(xpath_li.strip()) == 0:
        return '0'
    else:
        # print(f'Qzone_tag: {qzone_single_info}')
        return qzone_single_info


def is_exitcsv(csv_file):
    # 首先打开csv文件：qzone_usermain.csv，如果文件为空,则新建一个。
    try:
        df_file = pd.read_csv(csv_file, names=['U','D','I','T','N','L'], header=0, encoding='utf_8_sig')
    except FileNotFoundError as e:
        print('New CSV File: qzone_usermain.csv', e)
        df_qzone.to_csv(csv_file, header=df_header, index=False, encoding='utf_8_sig')
        df_file = pd.read_csv(csv_file, names=['U','D','I','T','N','L'], header=0, encoding='utf_8_sig')

    # 返回一个从 qzone_usermain.csv 数据文件中读取的 DataFrame数据集：df_file
    return df_file


def save_csv(df_data, df_file, csv_file):
    # df_data 是从QQ空间动态分享网页爬取的新增数据，为 DataFrame数据集
    # df_file 是从 qzone_usermain.csv 数据文件中读取的 DataFrame数据集
    # 将拼接后的QQ空间动态分享数据集从新写入到：csv_file(qzone_usermain.csv)文件中
    # print(f'save_csv: {len(df_data)}')
    try:
        df_qzone = pd.concat([df_file, df_data], axis=0)
        df_qzone.to_csv(csv_file, header=df_header, index=False, encoding='utf_8_sig')
    except ValueError as e:
        '''
        print(f'User:{df_data["user"]}\n')
        print(f'Date:{df_data["date"]}\n')
        print(f'Info:{df_data["info"]}\n')
        print(f'Title:{df_data["title"]}\n')
        print(f'Note:{df_data["note"]}\n')
        print(f'Link:{df_data["link"]}\n')
        print(f'Header:{df_header}\n')   
        
        '''
        print(f'Data:{df_qzone}')
        print(f'Write To Qzone CSV File: {csv_file} Error', e)
        pass
    except IOError as e:
        print(e)
        pass
    except IndexError as e:
        print(e)
        pass
