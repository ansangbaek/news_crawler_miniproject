import os
import requests
import json
import logging


logger = logging.getLogger(__name__)

def send_slack_message(new_items):
 
    """
    Slack으로 신규 기사 알림 전송
    
    Args:
        new_items (list): 신규기사 정보

    """
    
    if not new_items:
        return 

    webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    if not webhook_url:
        logger.error("SLACK_WEBHOOK_URL 설정 필요")
        return

    text_lines = [f"*신규 기사 {len(new_items)}건 등록!*"]

    for idx, n in enumerate(new_items, 1):
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

