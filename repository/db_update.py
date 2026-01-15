import logging
from .connection import *

logger = logging.getLogger(__name__)

def update(conn, sql, values) :
    """
    update 쿼리를 실행한다

    Args:
        conn: DB연결된 객체
        sql (str): select 쿼리문
        values (_type_): 바인딩 parameter

    Returns:
        void | None: (cursor 생성실패, update실패) None
        
    """

    # conn을 사용할 cursor생성
    cursor = create_cursor(conn)

    if cursor == None:
        return
    

    # sql문 실행 실패시 log에 원인과 sql작성
    try:
        cursor.execute(sql, values)
    except Exception as e:
        conn.rollback()
        logger.error("update 실패 : %s - %s", e, sql)
        return
    
    conn.commit()
    close(cursor)