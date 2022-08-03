import requests
import os
import re

from bs4 import BeautifulSoup
from contextlib import closing
from tqdm import tqdm

# 下载保存的目录，如果没有就创建，有就保存
save_dir = '原神'
if save_dir not in os.listdir('./'):
    os.makedirs(save_dir)

# 目标网址
target_url = 'https://www.dmzj.com/info/yuanshenproject.html'

# 获取漫画章节链接以及章节名字
r = requests.get(target_url)
html = r.text
bs = BeautifulSoup(html, 'lxml')
list_con_li = bs.find('ul', class_='list_con_li')
cartoon_list = list_con_li.find_all('a')
chapter_names = []
chapter_urls = []
for cartoon in cartoon_list:
    href = cartoon.get('href')
    name = cartoon.text
    chapter_names.insert(0, name)
    chapter_urls.insert(0, href)

# 下载漫画，对漫画网站顺序进行一个排序
for i, url in enumerate(tqdm(chapter_urls)):
    download_header = {
        'Referer': url
    }
    name = chapter_names[i]
    # 若爬出的章节名有.，则去掉
    while '.' in name:
        name = name.replace('.', '')
    # 创建章节目录
    chapter_save_dir = os.path.join(save_dir, name)
    if name not in os.listdir(save_dir):
        os.makedirs(chapter_save_dir)
        r = requests.get(url=url)
        html = r.text
        bs = BeautifulSoup(html, 'lxml')
        script_info = bs.script
        pics = re.findall('\d{13,14}', str(script_info))
        # enumerate() 函数用于将一个可遍历的数据对象 [(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]
        for j, pic in enumerate(pics):
            if len(pic) == 13:
                # 猜测其排序后面末位补零，所以添加0
                pics[j] = pic + '0'
        # sorted() 函数对所有可迭代的对象进行排序操作,即5,3,2,4变成2，3,4,5
        pics = sorted(pics, key=lambda x: int(x))
        # 下载别的可能需要更改
        chapterpic_hou = re.findall('\|(\d{6})\|', str(script_info))[0]
        chapterpic_qian = re.findall('\|(\d{5})\|', str(script_info))[0]
        for idx, pic in enumerate(pics):
            # 下载图片的URL，需要下载别的可在这更改
            if pic[-1] == '0':
                url = 'https://images.dmzj.com/img/chapterpic/' + chapterpic_qian + '/' + chapterpic_hou + '/' + pic[
                                                                                                                 :-1] + '.jpg'
            else:
                url = 'https://images.dmzj.com/img/chapterpic/' + chapterpic_qian + '/' + chapterpic_hou + '/' + pic + '.jpg'
            # 给下载图片命名
            pic_name = '%03d.jpg' % (idx + 1)
            pic_save_path = os.path.join(chapter_save_dir, pic_name)
            with closing(requests.get(url, headers=download_header, stream=True)) as response:
                chunk_size = 1024
                content_size = int(response.headers['content-length'])
                if response.status_code == 200:
                    # print('文件大小:%0.2f KB' % (content_size / chunk_size))
                    with open(pic_save_path, 'wb') as file:
                        # iter_content() 迭代响应
                        for data in response.iter_content(chunk_size=chunk_size):
                            file.write(data)
                else:
                    print('异常')