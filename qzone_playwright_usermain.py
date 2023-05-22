'''
    程序功能描述: 采用 playwright 爬取 QQ 空间文章数据
    开发者: Cobra1966
    时间: 2022-08-06
    最后修改: 2023-04-05
	在HUAWEI笔记本完成代码进一步优化：D:\Cobra1966\Python\example\
	          qzone_playwright_usermain.py ,
			  qzone_config.py
    2月份在DELL笔记本上完成了初步优化
	          文件名及路径: /home/cobra1966/PyworkspaceOne/qzone-spider/
			  qzone_playwright_usermain.py,
			  qzone_config.py
'''

# 引用爬取QQ空间网站必须的库
from playwright.sync_api import Playwright, sync_playwright, expect
import pandas as pd
# import time
import sys
import getpass
from urllib import parse
# import os
import qzone_config as qc

# 构建 Qzone_getmain 爬取类
class QzonegetMain(object):

    # 设置手动加载QQ空间动态主页记录器字典 record_qzone_main
    # record_qzone_main = {
    #     "num": 0,
    #     "get_qzone1": 0,
    #     "get_qzone2": 0
    # }

    
    # 初始化函数: __init__
    def __init__(self, **kargs):
        self.username = kargs["username"]
        self.password = kargs["password"]
        # 打开 QQ空间数据文件(qzone_usermain.csv)， 并转成 Pandas.DataFrame数据集
        self.csv_file = kargs["csv_file"]
        self.df_file = qc.is_exitcsv(self.csv_file)

        # QQ空间动态分享网址：
        self.qzone_url = f"https://qzone.qq.com/"
        self.html_page = None
        # username, password, qzone_url
        self.data_qzone = qc.data_qzone
        self.df_header = qc.df_header
        self.df_qzone = qc.df_qzone
        self.qzone_dic = dict()
        # self.record_qzone_main = QzonegetMain.record_qzone_main

        # 若有相同的数据记录，j则为：True，反之为：False
        self.j = False
		
		# 已经读取的每页数据计数器
        self.page_count = 1

    
    def write_one_qzone_dic(self, single_info):
        # 将QQ空间单个记录不断增加到 self.data_qzone 字典缓存变量中
        self.data_qzone["user"].append(single_info["qz_ni"])
        self.data_qzone["date"].append(single_info["qz_ti"])
        # 判断 single_info["qz_in"] 内容是否包含逗号(，), 如果有就用"下划线"(_)替换
		# if ',' in single_info["qz_in"]:
        #     self.data_qzone["info"].append(single_info["qz_in"]).replace(',', '_')
        self.data_qzone["info"].append(single_info["qz_in"])
        self.data_qzone["title"].append(single_info["qz_te"])
        self.data_qzone["note"].append(single_info["qz_nt"])
        self.data_qzone["link"].append(single_info["qz_li"])

        # 结尾 write_one_qzone_dic()

    
    # 清空self.data_qzone字典中的6个列表(list):['user'],['date']...
    def clear_data_qzone(self):
        # 清空 self.data_qzone 字典中6个列表的值
        self.data_qzone["user"].clear()
        self.data_qzone["date"].clear()
        self.data_qzone["info"].clear()
        self.data_qzone["title"].clear()
        self.data_qzone["note"].clear()
        self.data_qzone["link"].clear()

        # 结尾 clear_data_qzone()

    
    def write_all_qzone_dic(self):
        # 将本次获取的所有QQ空间动态分享内容存入 qzone_dic 字典缓存变量中，并返回
        '''
        qzone_dic = {
            'user': self.data_qzone["user"],
            'date': self.data_qzone["date"],
            'info': self.data_qzone["info"],
            'title': self.data_qzone["title"],
            'note': self.data_qzone["note"],
            'link': self.data_qzone["link"]
        }
        
        '''
        qzone_dic = {
            'U': self.data_qzone["user"],
            'D': self.data_qzone["date"],
            'I': self.data_qzone["info"],
            'T': self.data_qzone["title"],
            'N': self.data_qzone["note"],
            'L': self.data_qzone["link"]
        }

        # 返回一页的QQ空间数据--字典缓存变量：qzone_dic
        return qzone_dic


    def write_qzone_playwright(self, page1, rows):
        # Playwright 爬取QQ空间一页的用户文章分享数据，并存入CSV文件的模块
        # 此模块的参数：page1:QQ空间用户主页数据网页缓冲区, rows: 读取li标签数据集, j: 数据查重标记
        single_info = dict()
        
        # 调用判断函数：qc.iszero()判断
        # 用户名(qz_ni) 是否为空值
        # 分享时间(qz_ti) 是否为空值
        # 分享笔记(qz_in) 是否为空值(极少情况没有这一项元素标签)
        # 原文章来源(qz_te) 是否为空值
        # 原文章注释(qz_nt) 是否为空值
        # 原文章的链接(qz_li) 是否为空值
        
        # 暂停 9 秒，等待读取正文数据
        page1.wait_for_timeout(6000)
        qzone_count = rows.count()
        # print(f'Get Recard\'s={qzone_count}')
        # print(rows.all_text_contents())
        # 利用 range() 函数的倒序功能实现分批爬取数据，并提升查重效率
        for i in range(qzone_count, 0, -1):
            try:
                # print(rows.nth(i).inner_text())
                # 用户昵称: class="f-nick" 
                single_info["qz_ni"] = qc.is_zero(rows.nth(i-1).locator("div.f-nick").inner_text())
            except BaseException as e:
                single_info["qz_ni"] = '0'

            try:
                # 分享文章时间:
                # qzone_date = rows.nth(i-1).locator("div.info-detail").inner_text()
                single_info["qz_ti"] = qc.is_zero(rows.nth(i-1).locator("div.info-detail").inner_text())
            except BaseException as e:
                single_info["qz_ti"] = '0'

            try:
                # 分享精粹
                # qzone_info = rows.nth(i-1).locator("div.f-info").inner_text()
                re_info = qc.is_zero(rows.nth(i-1).locator("div.f-info").inner_text())
                if ',' in re_info:
                    single_info["qz_in"] = re_info.replace(',', '_')
                else:
                    single_info["qz_in"] = re_info
                if "\'" in single_info["qz_in"]:
                    single_info["qz_in"] = single_info["qz_in"].replace("\'", '')

            except BaseException as e:
                single_info["qz_in"] = '0'

            try:
                # 原文章标题
                # qzone_title = rows.nth(i-1).locator("div.txt-box >> h4").inner_text()
                single_info["qz_te"] = qc.is_zero(rows.nth(i-1).locator("div.txt-box >> h4").inner_text())
            except BaseException as e:
                single_info["qz_te"] = '0'

            try:
                # 原文章简介
                # qzone_note = rows.nth(i-1).locator("div.txt-box >> a.f-name").inner_text()
                single_info["qz_nt"] = qc.is_zero(rows.nth(i-1).locator("div.txt-box >> a.f-name").inner_text())
            except BaseException as e:
                single_info["qz_nt"] = '0'

            try:
                # 原文章链接
                # qzone_link = rows.nth(i-1).locator("div.txt-box >> a.f-name").get_attribute('href')
                single_info["qz_li"] = qc.is_zero(rows.nth(i-1).locator("div.txt-box >> a.f-name").get_attribute('href'))
                if "\'" in single_info["qz_in"]:
                    single_info["qz_in"] = single_info["qz_in"].replace("\'", '')

            except BaseException as e:
                single_info["qz_li"] = '0'


                # 好友点评
                # comment = rows.nth(i-1).locator("div.f-single-foot").text_content()

            # 通过对df_file(DataFrame)数据集进行查重，如无则添加所有信息到列表，以下相同
            # 例子01：df1[df1["info"].isin(["学习lxml实例笔记5"])]
            self.page_count += 1
            if len(self.df_file[self.df_file["I"].isin([single_info["qz_in"]])]) > 0 and len(self.df_file[self.df_file["T"].isin([single_info["qz_te"]])]) > 0:
                self.j = True
                print(f'此QQ空间分享文章的记录数据重复-CSV...{self.page_count - i}')
                break
            # elif single_info["qz_in"] in self.data_qzone["info"] and single_info["qz_te"] in self.data_qzone["title"]:
            #     self.j = True
            #     print(f'此QQ空间分享文章的记录数据重复-SELF...')
            else:
                # 重复标记：j
                self.j = False
                # 添加QQ动态空间一条记录数据到列表: self.data_qzone
                # 调用函数: write_one_qzone_dic
                self.write_one_qzone_dic(single_info)

                # 显示记录的分享精粹
                print(f'info: {single_info["qz_in"]}')
                
        
        # 存入本页所有不重复的QQ空间动态分享记录字典变量, 并转换成DataFrame格式
        # 调用保存QQ空间动态分享内容所有记录到字典缓存变量(qzone_dic)的函数
        self.qzone_dic = self.write_all_qzone_dic()
        
        # 将爬取的QQ空间动态分享数据写入 CSV(qzone_usermain.csv) 文件的函数：save_csv(df_mem, df_file, csv_file)
        # df_mem: 爬取此页的最新字典数据集，df_file: CSV 文件中的原有数据集，csv_file: 文件名
        # 由于第一个记录是空记录，判断如果只有一个记录则不用写入到文件中
        if len(self.qzone_dic['U']) == 1 and len(self.qzone_dic['U'][0]) <= 0:
            print(f'Only one blank recode, Don\'t written ...')
        else:
            # 转存为 pandas.DataFrame 数据集
            df_mem = pd.DataFrame(self.qzone_dic)

            # 保存此页的QQ空间动态分享数据到 CSV(qzone_usermain.csv) 文件里
            qc.save_csv(df_mem, self.df_file, self.csv_file)

        return len(self.qzone_dic['U'])
        # write_qzone_playwright() 结尾

    
    # 用 Playwright 爬取QQ空间网站数据的主程序
    def run(self, playwright: Playwright) -> None:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()

        # Open new page
        page = context.new_page()
        
        # 2023年2月14日 QQ空间网又有调整，优化代码如下：
        # Go to https://qzone.qq.com/
        
        page.goto(f"{self.qzone_url}")

        # page.goto("https://qzone.qq.com/")
        page.frame_locator("iframe[name=\"login_frame\"]").get_by_role("link", name="密码登录").click()
        page.frame_locator("iframe[name=\"login_frame\"]").get_by_label("支持QQ号/邮箱/手机号登录").fill(f"{self.username}")
        page.frame_locator("iframe[name=\"login_frame\"]").get_by_label("支持QQ号/邮箱/手机号登录").press("Tab")
        page.frame_locator("iframe[name=\"login_frame\"]").get_by_label("请输入密码").fill(f"{self.password}")
        page.frame_locator("iframe[name=\"login_frame\"]").get_by_role("button", name="登录").click()
        page.get_by_role("link", name="主页", exact=True).click()
        # page.frame_locator("iframe[title=\"主人动态内容区\"]").locator("#ifeedsContainer").click()


        # Click text=Qzone
        # with page.expect_popup() as popup_info:
        #     page.locator("text=Qzone").click()
        # page1 = popup_info.value

        # 选择 用户名和密码登录界面
        # Click a:has-text("密码登录")
        # page1.frame_locator("iframe[name=\"login_frame\"]").locator("a:has-text(\"密码登录\")").click()

        # # Fill input[name="u"] QQ=self.username
        # page1.frame_locator("iframe[name=\"login_frame\"]").locator("input[name=\"u\"]").fill(f"{self.username}")

        # # Press Tab
        # page1.frame_locator("iframe[name=\"login_frame\"]").locator("input[name=\"u\"]").press("Tab")

        # # Fill input[name="p"] QQ=self.password
        # page1.frame_locator("iframe[name=\"login_frame\"]").locator("input[name=\"p\"]").fill(f"{self.password}")
        
        # # Click input:has-text("登录")
        # # 
        # page1.frame_locator("iframe[name=\"login_frame\"]").locator("input:has-text(\"登录\")").click()
        # # qzone_url = f'https://user.qzone.qq.com/{self.username}'
        
        # 等待 6秒, 获取此用户的QQ空间网页数据 ...
        page.wait_for_timeout(6000)
        # page.locator("#main_feed_container").click()
        # print(f'Frist...')
        # 暂停 3 秒，等待读取正文数据
        page.wait_for_timeout(3000)
        # Click #menuContainer >> text=主页
        page.locator("#menuContainer >> text=主页").click()
        # expect(page1).to_have_url("https://user.qzone.qq.com/{qq_number}/main")
        # 
        # Click a:has-text("顶部")
        # page1.locator("a:has-text(\"顶部\")").click()
        while True:
            page.wait_for_timeout(6000)
            rows = page.frame_locator("#QM_Feeds_Iframe").locator("#host_home_feeds >> li.f-single.f-s-s")

            # 调用 QQ空间数据存储函数
            save_page_num = self.write_qzone_playwright(page, rows)

            # print(f'self.data_qzone = {self.data_qzone["info"]}')
            # 实现 QQ空间网页的自动翻页，并继续爬取数据
            self.page_count -= 1
            print(f"已经读取有效数据={self.page_count}\n")
            qzone_goto = input(f'Read Recard={rows.count()}, 保存记录={save_page_num}, 按(q)退出，其他键翻页继续...')
            if qzone_goto.strip() == 'q':
                break
            
            # 清空 self.data_qzone, self.qzone_dic
            self.clear_data_qzone()
            self.qzone_dic.clear()

            # 重新读取 CSV 文件，更新 self.df_file 数据
            self.df_file = qc.is_exitcsv(self.csv_file)
            
            # 控制翻页，等待读取正文数据
            for i in range(19):
                rows.last.press("PageDown")
                # 等待 1 秒
                page.wait_for_timeout(1000)
            page.wait_for_timeout(3000)

        # 当结束爬取QQ空间数据, 则关闭 Browser、Context、page 缓存区
        page.close()

        # Close context, browser
        context.close()
        browser.close()
    
        # run() 结尾


# 主入口程序
if __name__ == "__main__":
    # url = f"https://www.qq.com/"
    # 如果输入 1164726081, 2598570897, 1720968127 三个QQ号和密码，则登录QQ空间网站
    # 如果输入为空（或直接回车），则打印警告信息，并退出。
    txt_name = input("请输入QQ空间用户号(1720968127):")
    url = parse.quote(txt_name)
    if str.strip(url) == '':
        print(r'警告：用户名和密码不能为空...')
        sys.exit()
        pass
    else:
        txt_pswd = getpass.getpass("请输入QQ空间用户密码(...):")

        # 创建 QQ空间爬虫类:QzonegetMain 实例对象: Qzond
        Qzond = QzonegetMain(username=txt_name, password=txt_pswd, csv_file=r'qzone_usermain.csv')
        with sync_playwright() as playwright:
            Qzond.run(playwright)
