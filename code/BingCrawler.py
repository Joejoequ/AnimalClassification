# a script for crawling data from BING
import os
import sys

import cv2
import requests
from lxml import etree
import re
import time

urllist = []
animalList = ['butterfly', 'cat', 'chicken', 'cow', 'dog', 'elephant', 'spider', 'squirrel', 'sheep', 'horse']
keyword = animalList[2]+" animal"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}
picpath = './' + keyword
totalpic = 150

count = 1


def save_img(url):
    global count
    # img_name = url[-10:]
    # name = re.sub('/', '', img_name)
    global urllist
    filename = ''
    if url.replace("https", "http") not in urllist:
        urllist.append(url.replace("https", "http"))
    else:
        return

    try:
        res = requests.get(url, headers=headers)
    except OSError:
        print('Error Url:', url)
    else:
        filename = picpath + '/' + str(count) + '.jpg'
        with open(filename, 'wb')as f:
            try:
                print(count, ': ', url)
                f.write(res.content)

                img = cv2.imread(filename,1)

                if img is None:
                    raise OSError
                else:
                    count += 1


            except OSError:
                print('Url image can not be saved：', url)

    if (count > totalpic):
        sys.exit()


# all url in this page
def parse_img(url):
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    data = response.content.decode('utf-8', 'ignore')
    html = etree.HTML(data)
    conda_list = html.xpath('//a[@class="iusc"]/@m')
    all_url = []
    for i in conda_list:
        img_url = re.search('"murl":"(.*?)"', i).group(1)
        all_url.append(img_url)
    return all_url


def main():
    if not os.path.exists(picpath): os.makedirs(picpath)
    i = 0
    while True:
        url = 'https://www.bing.com/images/async?q=' + keyword + '&first=' + str(
            i) + '&count=35&relp=35&scenario=ImageBasicHover&datsrc=N_I&layout=RowBased&mmasync=1'

        img_data = parse_img(url)
        for img_url in img_data:
            save_img(img_url)

        i += 1


if __name__ == '__main__':
    main()
