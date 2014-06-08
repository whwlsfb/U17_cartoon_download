#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import requests
import base64
import binascii
from bs4 import BeautifulSoup

'''
下载有妖气漫画 cartoon_url换成对应的漫画主页
在同目录下生成 Cartoon/'漫画名称'/ 文件夹
包括漫画文件和 info.log 所下载漫画章节信息
删除info.log 文件内容时最后留一行空白

'''
def get_page_img(page_url):
    img_temp = []
    cartoon_html = requests.get(page_url).content
    img_url_list = re.findall(r'"src":"(.*?)"', cartoon_html)
    for each in img_url_list:
        img_temp.append(base64.b64decode(each))
    # 返回某一章所有图片列表
    return img_temp


def get_cartoon(url):
# 遍历所有章节 返回漫画名称 所有章目信息 所漫画信息
    soup = BeautifulSoup(requests.get(url).content)
    title = soup.find('title').string
    img_list = cpt = chapter = {}
    a = soup.find('ul', class_='cf chapter_list_display')
    # 获取章节列表
    all_chapter = a.find_all('li')
    x = 1
    for each in all_chapter:
        cpt['%s_cpt_title' % x] = each.a['title']
        cpt['%s_cpt_url' % x] = each.a['href']
        page_url = each.a['href']
        img_list['%s_img_list' % x] = get_page_img(page_url)
        x = x + 1
    chapter['chapter_info'] = cpt
    chapter['img_info'] = img_list
    # 返回漫画名称 章节{'章节信息'{'章节名称','章节地址'}
    #                   '章节图片列表'{第一章图片列表,...}}
    return (title, chapter)


def download_chapter(title, chapter, start_chapter, end_chapter, cpt_log, new):
# 遍历需要下载的章节
    for n in range(start_chapter, end_chapter):
        i = 1
        chapter_name = chapter['chapter_info']['%s_cpt_title' % n]
        print('Download…… Chapter %s-----%s' %
             (n, chapter_name.encode('utf-8')))
        cpt_log = cpt_log + 'Chapter %s-----' % n + chapter_name + '\n'
        # 遍历章节图片列表 下载每一章图片
        for each in chapter['img_info']['%s_img_list' % n]:
            img = requests.get(each).content
            with open('Cartoon/%s/%s---%s.jpg' % (title, chapter_name, i), 'wb') as f:
                        f.write(img)
            i = i + 1
    # 判断是否更新以决定log写入方式
    if (new == 0):
        x = 'a'
        i = 'Update done!'
    else:
        x = 'w'
        i = 'All done!'
    # 写入 info.log 日志
    with open('Cartoon/%s/info.log' % title, '%s' % x) as f:
        f.write(cpt_log.encode('utf-8'))
    print('%s' % i)


def main(title, chapter, max_chapter=None):
    print('Start Check!')
    if os.path.exists('Cartoon/%s' % title):
    # 文件存在即读取info.log 获得已存在章节信息
    # chapter_num 已更新章节 local_chapter_num 本地已下载章节
        try:
            with open('Cartoon/%s/info.log' % title, 'r') as f:
                local_chapter_num = len(f.readlines()) - 1
        except:
            with open('Cartoon/%s/info.log' % title, 'w') as f:
                local_chapter_num = 0
        chapter_num = len(chapter['img_info']) / 3
    # 判断是否需要下载更新章节
        update = chapter_num - local_chapter_num
        if (update > 0):
            print('%s  have new chapter!' % title.encode('utf-8'))
            print('Start Update...')
            cpt_log = ''
            start = local_chapter_num + 1
            end = chapter_num + 1
            download_chapter(title, chapter, start, end, cpt_log, 0)
        else:
            print('No chapter to update!')
    else:
    # 创建目录
        os.makedirs('Cartoon/%s' % title)
        print('Start Download %s...' % title.encode('utf-8'))
    # info.log 文件首行
        cpt_log = '    %s   Tables\n' % title
        start = 1
        end = len(chapter) / 3 + 1
        if max_chapter is not None:
            if end > max_chapter:
                end = max_chapter + 1
        download_chapter(title, chapter, start, end, cpt_log, 1)


def download_url(url, max_chapter=None):
    title, chapter = get_cartoon(url)
    main(title, chapter, max_chapter)


if (__name__ == '__main__'):
    # 漫画地址
    print ('Start……')
    cartoon_url = 'http://www.u17.com/comic/5553.html'
    download_url(cartoon_url)
