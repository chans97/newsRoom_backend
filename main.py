import json
from time import sleep
from typing import Optional
from fastapi import FastAPI, Depends, Path, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from database import engineconn
from models import NEWSROOM_USER,SCRAPE_KEYWORD,SCRAPED_NEWS
from apiRes import ApiRes
from crawling_news import crawling_news
from utils.parse_datetime_str import parse_datetime_str


#to-do : 무한 스크롤로 다음 페이지까지 다 긁어오기

app = FastAPI()

engine = engineconn()
session = engine.sessionmaker()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True, # cookie 포함 여부를 설정한다. 기본은 False
    allow_methods=["*"],    # 허용할 method를 설정할 수 있으며, 기본값은 'GET'이다.
    allow_headers=["*"],	# 허용할 http header 목록을 설정할 수 있으며 Content-Type, Accept, Accept-Language, Content-Language은 항상 허용된다.
)


@app.get("/api/news/{keyword}/{start}")
def response_crawled_news_list(keyword:str,start:int):
 
    api_res = ApiRes()
    result=''

    try:
        result = crawling_news(keyword,start)
    except Exception as e:
        print(e)
        api_res.set_success(False)

    api_res.set_success(True)
    api_res.update_data({"result":result})
    return api_res


@app.post("/api/login")
async def login(request: Request):

    api_res = ApiRes()
    request_body = await request.body()
    data = json.loads(request_body)
    company_id = data["company_id"]
    newsroom_user=''

    # 로그인 처리
    try:
        # company_id 를 통해서 newsroom_user 객체 찾기 
        newsroom_user = session.query(NEWSROOM_USER).filter_by(company_id=company_id).first()
        
        # 만약 newsroom_user가 null이면 newsroom_user가 없다는 것이기 때문에 newsroom_user를 새로 생성
        if not newsroom_user:
            newsroom_user = NEWSROOM_USER(
                company_id=company_id,
            )
            session.add(newsroom_user)
            session.commit()
            newsroom_user = session.query(NEWSROOM_USER).filter_by(company_id=company_id).first()
        

    except Exception as e: 
        print(e)
        api_res.set_success(False)
        return api_res

    api_res.set_success(True)
    api_res.update_data({"newsroom_user":newsroom_user})
    return api_res



@app.get("/api/keywordlist")
def keywordlist(user_id):       

    api_res = ApiRes()
    user_id = user_id
    newsroom_user=''
    try:
        # company_id 를 통해서 newsroom_user 객체 찾기 
        newsroom_user = session.query(NEWSROOM_USER).filter_by(user_id=user_id).first()
        api_res.set_success(True)
    except Exception as e:
        api_res.set_success(False)
        print(e)
    
    if newsroom_user:
        scrape_keywords = session.query(SCRAPE_KEYWORD).filter_by(newsroom_user=newsroom_user.user_id).all()
        keywords = [keyword  for keyword in scrape_keywords]
        api_res.update_data({'keywords': keywords})
    else:
        api_res.set_success(False)

    return api_res

@app.get("/api/scraped_news")
def scraped_news_list(keyword_id):

    api_res = ApiRes()
    keyword_id = keyword_id
    scraped_news=''
    try:
        # keyword_id 를 통해서 scraped_news 객체 찾기 
        scraped_news = session.query(SCRAPED_NEWS).filter_by(keyword=keyword_id).all()
        api_res.set_success(True)
        api_res.update_data({'scraped_news': scraped_news})
    except Exception as e:
        api_res.set_success(False)
        print(e)
    
    return api_res

@app.post("/api/scrape_news")
async def scrape_news(request: Request):

    request_body = await request.body()
    data = json.loads(request_body)
    api_res = ApiRes()

    user_id = data["user_id"]
    keyword_name = data["keyword"]
    keyword = session.query(SCRAPE_KEYWORD).filter_by(newsroom_user=user_id, keyword=keyword_name).first()
    try:
        if not keyword:
            keyword = SCRAPE_KEYWORD(keyword=keyword_name, newsroom_user=user_id)
            session.add(keyword)
            session.commit()
            keyword= session.query(SCRAPE_KEYWORD).filter_by(newsroom_user=user_id, keyword=keyword_name).first()
            
        scraped_news = SCRAPED_NEWS(
            title=data['title'],
            summary=data['summary'],
            broadcaster=data['broadcaster'],
            url=data['url'],
            created_at=parse_datetime_str(data['created_at']),
            keyword=keyword.getID(),
            user=user_id
        )
    except Exception as e:
        print(e)
        api_res.set_success(False)      
        return api_res 

    session.add(scraped_news)
    session.commit()
    api_res.set_success(True)
    api_res.update_data({'scraped_news': scraped_news.__dict__})

    return api_res


@app.post("/api/delete/scrape_news")
async def delete_scraped_news(request: Request):    
    request_body = await request.body()
    data = json.loads(request_body)
    api_res = ApiRes()
    is_no_more_news = False

    # SCRAPED_NEWS id 값으로 해당 객체를 가져옵니다.
    scraped_news_id = data["scraped_news_id"]
    scraped_news = session.query(SCRAPED_NEWS).get(scraped_news_id)

    if not scraped_news:
        api_res.set_success(False)
        api_res.set_error("해당 SCRAPED_NEWS가 존재하지 않습니다.")
        return api_res

    try:
        # SCRAPE_KEYWORD에서 해당 SCRAPED_NEWS가 속한 키워드 객체를 가져옵니다.
        keyword = session.query(SCRAPE_KEYWORD).filter_by(id=scraped_news.keyword).first()
        # 해당 SCRAPED_NEWS가 속한 키워드에 속한 다른 SCRAPED_NEWS가 없다면, 키워드를 삭제합니다.
        num_scraped_news = session.query(SCRAPED_NEWS).filter_by(keyword=keyword.getID()).count()


        if num_scraped_news == 1:
            session.delete(keyword)
            is_no_more_news = True
        session.delete(scraped_news)
        session.commit()

    except Exception as e:
        print(e)
        api_res.set_success(False)
        api_res.set_error("SCRAPED_NEWS 삭제에 실패했습니다.")
        return api_res

    api_res.set_success(True)
    api_res.update_data({"is_no_more_news":is_no_more_news})
    return api_res
