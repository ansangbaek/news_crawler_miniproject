import logging
from .connection import *

logger = logging.getLogger(__name__)


def select(conn, sql, values) :
    """
    select 쿼리를 실행한다

    Args:
        conn: DB연결된 객체
        sql (str): select 쿼리문
        values (_type_): 바인딩 parameter

    Returns:
        str | None: 성공시 select결과, (cursor생성실패, select실패, select결과없음)None
    """

    # conn을 사용할 cursor생성
    cursor = create_cursor(conn)

    if cursor == None :
        return  None


    # select실행후 실패시 log에 원인과 sql문 작성
    try:
        cursor.execute(sql, values)
    except Exception as e:
        logger.error("select 실패 : %s - %s", e, sql)
        return None

    
    # cursor의 결과 반환 
    row = cursor.fetchone()

   
    # 반환 받은 결과가 없으면 return None
    if row is None:
        return None

    
    # 반환받은 실제 결과
    result = row[0]

    close(cursor)
    return result
