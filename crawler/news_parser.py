from bs4 import BeautifulSoup
import feedparser
from .text_get import *


def parse_news(link):
    """
    news의 정보를 분석한다
    Args:
        link (list): rss_link의 list

    Returns:
        list: news의 정보들이 list를 반환
    """
    
    # rss_xml 분석
    feed = feedparser.parse(link)

    db_list = []

    # news의 정보를 담기 위한 반복문
    # 본문에 있는 정보를 추출 하는 과정을 포함
    for entry in feed.entries :
        
        # 본문news link, html_text형식 수집
        news_link = entry.link
        news_html = load_url_text(news_link)
        if news_html == None :
            continue
                
        news_soup = BeautifulSoup(news_html, 'html.parser')

        # div태그의 id속성이 해당하는 정보 뽑아오기("입력 : YYYY-MM-DD" 형식 공백 제외)
        date_link = [a.get_text(strip=True) for a in news_soup.select('div[id="news_util01"]')]
        
        # idx까지의 링크 정보 수집 
        rel_link = [a.get('href') for a in news_soup.select('link[rel="canonical"]')]
        
        # datetime 형식으로 format작업
        write_dt = date_link[0].split('입력 :')[1] + ':00'
        
        # news의 정보를 dict형식으로 list에 추가
        db_dict ={
            'title' : entry.title
            , 'link' : news_link
            , 'rel_link' : rel_link
            , 'write_dt' : write_dt
        }
        db_list.append(db_dict)

    return db_list




