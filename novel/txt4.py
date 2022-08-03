import requests
import time
from tqdm import tqdm
from bs4 import BeautifulSoup

# 获取正文内容的函数
def get_content(target):
    req = requests.get(url=target)
    req.encoding = 'utf-8'
    html = req.text
    bs = BeautifulSoup(html,'lxml')
    texts = bs.find('div', id='content')
    # 去掉获取的html所含的回车空格等内容，并且存为列表形式
    content = texts.text.strip().split()
    return content


if __name__ == '__main__':
    # 网站主页
    server = 'https://www.xxbiquge.com'
    book_name = '一剑独尊.txt'
    # 小说主页，获取主页中的每个章节名字以及url
    target = 'https://www.xxbiquge.com/84_84063/'
    req = requests.get(url=target)
    req.encoding = 'utf-8'
    html = req.text
    chapter_bs = BeautifulSoup(html,'lxml')
    chapters = chapter_bs.find('div',id='list')
    chapters = chapters.find_all('a')
    # 通过循环，写入每一章小说内容
    for chapter in tqdm(chapters):
        chapter_name = chapter.string
        # 拼接网站主页url 达到获取各个章节的内容
        url = server+chapter.get('href')
        # 调取函数，来获得所有小说内容
        content = get_content(url)
        # 写入txt文本里
        with open(book_name, 'a', encoding='utf-8') as f:
            f.write(chapter_name)
            f.write('\n')
            f.write('\n'.join(content))
            f.write('\n')