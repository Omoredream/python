import json
import subprocess

import requests
from bs4 import BeautifulSoup
import os


def geturl(url):
    print('地址解析中')
    bvideohtml = requests.get(url)
    values = bvideohtml.text
    text = BeautifulSoup(values, 'lxml')
    title = text.find('title').contents[0].replace('  ','').replace('/','').replace('|','').replace(':','').replace('*','').replace('?','').replace('<','').replace('>','').replace('\n','').replace('【','').replace('】','').replace(' ','_')
    items = text.find_all('script')[3]
    items = items.contents[0].replace('window.__playinfo__=', '')
    obj = json.loads(items)
    videourl = obj["data"]["dash"]["video"][0]["baseUrl"]
    audiourl = obj["data"]["dash"]["audio"][0]["baseUrl"]
    print("地址解析完成")
    return videourl, audiourl, title


def getvideo(url):
    print('开始发送请求')
    url = geturl(url)
    videourl = url[0]
    audiourl = url[1]
    title = url[2]
    headers = {
        'Referer': 'https://www.bilibili.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'
    }
    print('请求成功返回')
    print('开始下载视频，音频文件')
    print(f'{title}.mp4')
    with open(f'F:/python源码/脚本练习/B站/Video.mp4', 'wb') as video:
        video.write(requests.get(videourl, headers=headers).content)
    with open(f'F:/python源码/脚本练习/B站/audio.mp3', 'wb') as audio:
        audio.write(requests.get(audiourl, headers=headers).content)
    print('下载完成')
    return f'F:/python源码/脚本练习/B站/Video.mp4', f'F:/python源码/脚本练习/B站/audio.mp3', title


def mixvideo(url):
    print('合成视频中')
    file = getvideo(url)
    mp4_file = file[0]
    file_name = file[1]
    title = file[2]
    print(title)
    cmd = f'ffmpeg -i {mp4_file} -i {file_name} -acodec copy -vcodec copy ' \
          f'F:/python源码/脚本练习/B站/{title}.mp4 '
    subprocess.call(cmd, shell=True)
    print("合成完毕")
    os.remove(mp4_file)
    os.remove(file_name)
    print('删除临时文件')


if __name__ == '__main__':
    save_dir = 'B站'
    if save_dir not in os.listdir('./'):
        os.makedirs(save_dir)
    url = input('请输入视频的B站地址:')
    mixvideo(url)