import logging
from .connection import *

logger = logging.getLogger(__name__)


def insert(conn, sql, values) :
    """
    insert 쿼리를 실행 한다

    Args:
        conn: DB연결 객체
        sql (str): insert 쿼리문
        values (tuple): 바인딩 parameter

    Returns:
        void | None: (cursor 생성실패, insert실패) None

   """

    # conn을 사용할 cursor생성
    cursor = create_cursor(conn)

    if cursor == None:
        return False
    

    # sql문 실행 실패시 log에 원인과 sql 작성
    try:
        cursor.execute(sql, values)
    except Exception as e:
        conn.rollback()
        logger.error("insert 실패 : %s - %s", e, sql)
        return False
    
    conn.commit()
    close(cursor)
    
    return True






        

