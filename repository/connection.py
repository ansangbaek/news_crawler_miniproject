import logging
import mysql.connector as ms_con


logger = logging.getLogger(__name__)



def create_conn() :
    """
    DB연결 객체를 생성한다

    Returns:
        conn | None: 연결 성공시 연결된 객체, 실패시 None
    """
    try:
        conn = ms_con.connect(
            host="192.168.1.43"
            ,user="ktech"
            ,password="ktech!@#$"
            ,database="boannews"
            ,charset="utf8"
        )
    except Exception as e:
        logger.error("conn 생성 실패 : %s", e)
        conn = None
    
    return conn



def create_cursor(conn) :
    """
    conn을 사용하는 cursor객체를 생성한다

    Args:
        conn: DB연결 객체

    Returns:
        cursor | None: 생성 성공시 cursor, 실패시 None
    """

    try:
        cursor = conn.cursor()
    except Exception as e :
        logger.error("cursor 생성 실패 : %s", e)
        cursor = None

    return cursor






def close(any) :
    """
    생성된 객체를 정리하는 함수

    Args:
        any: DB연결객체, cursor
    """
    if any:
        any.close()
