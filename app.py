import sys
import logging_config as log_con
from  crawler import *
from repository import *

def main() :
    """
    rss 피드를 수집하여 news를 저장하는 실행 함수
    """


    
    log_con.setup_logging() 
    logger = logging.getLogger(__name__)
    
    logger.info("main실행")

    # 전달하는 인자(key)에 해당하는 url link를 담는 리스트 생성
    # rss[0] : 해당 url link
    rss = get_rss_urls('boannews')

    if rss == None :
        logger.error("get_rss_url failed")
        sys.exit()

    # 인자로 전달하는 url link의 응답 body(text)를 받아옴  
    rss_html = load_url_text(rss[0])

    if rss_html == None :
        sys.exit()

    # 카테고리별 rss 링크 목록 수집
    rss_link_list = parse_rss(rss_html)
    
    if not rss_link_list:
        logger.info("get_rss_link failed")
        sys.exit() 
    

    # 카테고리별 news의 정보 수집
    news_lists = []
    for link in rss_link_list:
        news_lists.append(parse_news(link))
    
    # DB 연결 생성
    conn = create_conn()
    
    if conn == None :
        sys.exit()
    else :
        logger.info("DB연결 성공")


    # DB data 저장  
    for news_list in news_lists:
        for item in save_news(conn, news_list) :
        save_category(conn, news_list)

    # Slack 에 보내기
    send_slack_message(new_items)

    # DB연결 해제
    close(conn)
    logger.info("DB연결 해제")

if __name__ == "__main__" :
    main()







