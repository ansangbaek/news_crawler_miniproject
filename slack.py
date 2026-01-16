import os
import sys
import requests
import json
import logging_config as log_con
from repository import *
from datetime import datetime, timedelta

log_con.setup_logging()
logger = logging.getLogger(__name__)

def send_slack_message():
 
    """
    Slack으로 신규 기사 알림 전송
    
    Args:
        new_items (list): 신규기사 정보

    """
    
    
    # Slack url가져오기
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    if not webhook_url:
        logger.error("SLACK_WEBHOOK_URL 설정 필요")
        return
    
    


    conn = create_conn()
    
    if conn is None:
        sys.exit()
    else :
        logger.info("DB연결 성공")
    
    # 전날 8시 이후 create_dt찾기위한 format
    now = datetime.now()
    yesterday_8am = datetime(now.year, now.month, now.day, 8, 0, 0) - timedelta(days=1)
    yesterday_8am_str = yesterday_8am.strftime("%Y-%m-%d %H:%M:%S")

    # 전날 8시이후 DB에 들어온 결과 가져오기
    sql = "select title, link, publish_dt from news where db_create_dt > %s"

    new_items = select(conn, sql, (yesterday_8am_str,))
    
    # 필요한 key값
    columns = ['title', 'link', 'publish_dt']     
    
    # dict형식으로 변환
    result = [dict(zip(columns, news)) for news in new_items]


    text_lines = [f"*신규 기사 {len(new_items)}건 등록!*"]


    for idx, n in enumerate(result, 1):
        line = f"{idx}. <{n['link']}|{n['title']}>"
        text_lines.append(line)
        if 'publish_dt' in n:
            text_lines.append(f"   발행일: {n['publish_dt']}")

    message = {"text": "\n".join(text_lines)}


    try:
        response = requests.post(
            webhook_url,
            data=json.dumps(message),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code // 100 != 2:
            logger.error("Slack pase 연결 실패 :", response.status_code)
    except Exception as e:
        logger.error("Slack 전송 실패 : %s", e)
    

    close(conn)

    logger.info("DB연결해제")


if __name__ == "__main__":
    send_slack_message()
