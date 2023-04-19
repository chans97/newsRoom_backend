from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # cookie 포함 여부를 설정한다. 기본은 False
    allow_methods=["*"],    # 허용할 method를 설정할 수 있으며, 기본값은 'GET'이다.
    allow_headers=["*"],	# 허용할 http header 목록을 설정할 수 있으며 Content-Type, Accept, Accept-Language, Content-Language은 항상 허용된다.
)


def scraped_news(keyword):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(f'https://search.naver.com/search.naver?where=news&ie=utf8&sm=nws_hty&query={keyword}',headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')


    news_list = soup.select(".list_news>li")
    news_dict_list = []
    id = 0
    for news in news_list:
        id = id+1
        news_dict = {}
        news_dict.update(
        {
            "title":news.select_one("div.news_wrap.api_ani_send > div > a").text,
            "summary":news.select_one("div.news_wrap.api_ani_send > div > div.news_dsc > div > a").text,
            "broadcaster":news.select_one("div > div.news_info > div.info_group > a").text.replace("언론사 선정",""),
            "broadcastTime":news.select_one("div > div.news_info > div.info_group > span.info").text
        }
        )
        news_dict_list.append(news_dict)
    
    
    return news_dict_list  

@app.get("/api/news/{keyword}")
def response_scraped_news(keyword:str):
    result = scraped_news(keyword)

    return {"result": result}