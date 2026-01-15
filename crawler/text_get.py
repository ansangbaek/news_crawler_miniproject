import requests
import logging

logger = logging.getLogger(__name__)


def load_url_text(url: str) :
    """
    url의 html을 쓰기쉬운 text형식으로 변환한다

    Args:
        url (str): url주소

    Returns:
       str | None: 변환에 성공시 html의 body(text), (요청실패, content-type이 text/html이 아님)None
    """

    i = 0
    
    # 최초 1회 요청이 아닌 조건이 만족할 때 까지 여러번 요청
    # 요청에 성공 할 시, break로 반복문 탈출
    # 조건에 만족하여 else문에 도달 시 연결 실패 코드를 기록 후 조기 return
    while i < 5 :
        response = requests.get(url)
        if response.status_code // 100 == 2:
            break
        i += 1
    else :
        logger.error("연결 오류 코드 :  %s - %s", response.status_code, url)
        return None
   
    
    # 요청 성공 한 객체의 content-type 검증
    content_type = response.headers.get("Content-Type","")

    if 'text/html' not in content_type:
        logger.error("%s content-type : %s",url, content_type)
        return None
    
    return response.text
    
