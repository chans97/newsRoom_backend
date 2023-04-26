
import requests
from bs4 import BeautifulSoup

def crawling_news(keyword,start):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(f'https://search.naver.com/search.naver?where=news&ie=utf8&sm=nws_hty&query={keyword}&start={start}',headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    news_list = soup.select(".list_news>li")
    news_dict_list = []
    print(start)
    id = start
    for news in news_list:
        news_dict = {}
        news_dict.update(
        {
            "title":news.select_one("div.news_wrap.api_ani_send > div > a").text,
            "summary":news.select_one("div.news_wrap.api_ani_send > div > div.news_dsc > div > a").text,
            "broadcaster":news.select_one("div > div.news_info > div.info_group > a").text.replace("언론사 선정",""),
            "broadcastTime":news.select_one("div > div.news_info > div.info_group > span.info").text,
            "url":news.select_one("div.news_wrap.api_ani_send > div > a").attrs["href"],
            "news_id":id
        }
        )
        id = id+1
        news_dict_list.append(news_dict)
    
    
    return news_dict_list  

def crawling_recently_news(keyword,start):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(f'https://search.naver.com/search.naver?sm=tab_hty.top&where=news&sort=1&query={keyword}&start={start}',headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    news_list = soup.select(".list_news>li")
    news_dict_list = []
    print(start)
    id = start
    for news in news_list:
        news_dict = {}
        news_dict.update(
        {
            "title":news.select_one("div.news_wrap.api_ani_send > div > a").text,
            "summary":news.select_one("div.news_wrap.api_ani_send > div > div.news_dsc > div > a").text,
            "broadcaster":news.select_one("div > div.news_info > div.info_group > a").text.replace("언론사 선정",""),
            "broadcastTime":news.select_one("div > div.news_info > div.info_group > span.info").text,
            "url":news.select_one("div.news_wrap.api_ani_send > div > a").attrs["href"],
            "news_id":id
        }
        )
        id = id+1
        news_dict_list.append(news_dict)
    
    
    return news_dict_list  