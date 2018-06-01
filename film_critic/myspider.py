# -*- coding: utf-8 -*-
import requests
from lxml import etree
import time
import re
import json
from urllib.request import urlretrieve
import os

# from app import db
# from app.models import Movie


# 爬取豆瓣电影信息
# 日期：2018-5-12

# 当前文件路径
basedir = os.path.abspath(os.path.dirname(__file__))

class MySpider():
    # 获取普通电影URL列表，一页20个
    URL = 'https://movie.douban.com/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
    is_playing_url = 'https://movie.douban.com/cinema/nowplaying/shaoguan/'

    def get_movie_url(self, page):
        url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=热门&sort=recommend&page_limit=20&page_start={}'
        urls = 'https://movie.douban.com/subject/{}'
        for pages in range(0, page):
            url = url.format(pages * 20)
            request = requests.get(url, headers=self.headers)
            request.encoding = 'utf-8'
            json_ = json.loads(request.text)
            movie_url = []
            for i in range(0, 20):
                movie_url.append(urls.format(json_['subjects'][i]['id']))
        return movie_url

    # 获取正在热映电影URL，共15个
    def get_is_playing_movie_url(self, url):
        playing_url = 'https://movie.douban.com/subject/{}'
        request = requests.get(url, headers=self.headers)
        request.encoding = 'utf-8'
        html = etree.HTML(request.content)
        id_list = html.xpath('//div[@id="nowplaying"]//ul[@class="lists"]//li[@class="list-item"]/@id')
        playing_url_list = []
        for movie_id in id_list:
            playing_url_list.append(playing_url.format(movie_id))
        return playing_url_list

    # 获取电影详细信息
    def movie_info(self, url):
        request = requests.get(url, headers=self.headers)
        request.encoding = 'utf-8'
        html = etree.HTML(request.content)
        name = html.xpath('//*[@id="content"]/h1/span[1]/text()')
        director = html.xpath('//*[@id="info"]/span[1]/span[2]//a/text()')
        scriptwriter = html.xpath('//*[@id="info"]/span[2]/span[2]//a/text()')
        actor = html.xpath('//*[@id="info"]/span[@class="actor"]/span[@class="attrs"]//a//text()')
        tags = html.xpath('//*[@id="info"]//span[@property="v:genre"]/text()')
        runtime = html.xpath('//*[@id="info"]/span[@property="v:runtime"]/text()')
        country_ = html.xpath('//*[@id="info"]/text()')  # 国家和语言
        # print(country_)
        # country = re.split(r'/|\n| ', "".join(country_))
        # while ' / 'or '\n        ' in country_:
        #     country_.remove(' / ', '\n        ')
        country = [x for x in country_ if x != ' ' and x != ' / ' and
                   x != '\n        ' and x != '\n        \n        ' and
                   x != '\n        \n        \n        ']  # 国家和语言
        # print(country)

        year = html.xpath('//*[@id="info"]/span[@property="v:initialReleaseDate"]/text()')
        release_year = re.sub(r'\(.*\)$', "", year[0])

        description_ = html.xpath('//*[@id="link-report"]/span//text()')
        description = "".join(description_)
        pic = html.xpath('//*[@id="mainpic"]/a/img/@src')

        dict_movie = {}
        dict_movie['name'] = name[0]  # 电影名
        dict_movie['director'] = director  # 导演
        dict_movie['scriptwriter'] = scriptwriter  # 编剧
        dict_movie['actor'] = actor  # 主演
        dict_movie['tags'] = tags  # 类型
        dict_movie['country'] = country[0]  # 国家
        dict_movie['language'] = country[1]  # 语言
        dict_movie['runtime'] = runtime[0]  # 时长
        dict_movie['release_year'] = release_year  # 年份
        dict_movie['description'] = description  # 简介
        dict_movie['pic'] = pic[0]  # 插图
        dict_movie['other_name'] = country[2]   #别名
        return dict_movie



    # 获取插图
    def get_pic(self, url, name):
        if os.path.exists(basedir + 'app/static/images/{}.jpg'.format(name)):
            print(name + ' 插图已经存在')
        else:
            urlretrieve(url, basedir + 'app/static/images/{}.jpg'.format(name))
            print(name + ' 下载成功')

    # 数据库存储
    def main(self,page):
        playing_url = self.get_is_playing_movie_url(self.is_playing_url)  # 获取正在热映电影URL，共15个
        movie_url = self.get_movie_url(page)  # 获取普通电影URL，输入为页数，一页20个电影

        for url in playing_url+movie_url:
            info = self.movie_info(url)
            movie = Movie(
                name=info['name'],
                actor=info['actor'],
                director=info['director'],
                scriptwriter=info['scriptwriter'],
                language=info['language'],
                release_year=info['release_year'],
                runtime=info['runtime'],
                evaluate=info['evaluate'],
                country=info['country'],
                description=info['description'],
                picture=info['picture'],
                other_name=info['other_name'],
            )
            movie.add_tags_by_name(info['tags'])
            db.session.add(movie)
            db.session.commit()
            print(info['name'] + '添加成功')
            self.get_pic(info['pic'], info['name'])
            print(info)
            time.sleep(1)


if __name__ == '__main__':
    info = MySpider()
    # 获取普通电影URL，输入为页数，一页20个电影 info.main(page)
    info.main(1)
