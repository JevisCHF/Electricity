from selenium import webdriver
from lxml import etree
import time, re
from Scrapy_Ipoipo_V1_01.zip_rename import un_zip
from Scrapy_Ipoipo_V1_01.settings import CATES_DICT


# class DL(object):
#
#     def __init__(self):
#         options = webdriver.ChromeOptions()
#         prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'D:\\report zip\\',
#                  "profile.managed_default_content_settings.images": 2}
#         options.add_experimental_option('prefs', prefs)
#
#         self.d = webdriver.Chrome(chrome_options=options)

def get_content():
    download_dir = 'E:\\报告\\report zip\\'
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': download_dir,
             "profile.managed_default_content_settings.images": 2}
    options.add_experimental_option('prefs', prefs)

    d = webdriver.Chrome(chrome_options=options)
    # p = webdriver.PhantomJS(chrome_options=options)
    for n in range(1, 31):
        url = f'http://ipoipo.cn/tags-69_{n}.html'
        d.get(url)
        time.sleep(2)
        page = d.page_source
        html = etree.HTML(page)
        content = html.xpath('//div[@id="imgbox"]/div')

        for con in content:
            contents = {}
            name = con.xpath('./h2/a/text()')[0]
            # title = name[:-5].replace('（', '')
            download_link = con.xpath('./h2/a/@href')[0].replace('post', 'download')
            date = con.xpath('./div/span[2]/text()')[0]
            # print(title, download_link)

            d.get(download_link)
            time.sleep(2)

            page_source = d.page_source
            ht = etree.HTML(page_source)
            title = ht.xpath('//div[@class="con main"]/p[2]/a/text()')[0][:-4]

            d.find_element_by_xpath('//div[@class="con main"]/p[2]/a').click()
            time.sleep(15)

            rename = un_zip(download_dir, 'E:\\报告\\文件', title + '.pdf', CATES_DICT)
            time.sleep(1)
            try:
                # 文章具体路径
                contents['paper'] = rename['new_name']
                contents['abstract'] = None
                contents['title'] = title
                contents['paper_url'] = download_link
                contents['date'] = date
                contents['author'] = None
                contents['paper_from'] = '并购家'
                contents['parent_id'] = rename['root_id']
                # 清洗位
                contents['cleaning_status'] = 0
                # print(contents)
                yield contents
            except:
                print('文件无法保存！！！')

    time.sleep(60)
    d.quit()


if __name__ == '__main__':
    # a.get_content()
    # for i in range(5):
    b = get_content()
    for i in b:
        print(i)
