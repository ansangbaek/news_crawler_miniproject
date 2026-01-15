import logging
from .connection import *

logger = logging.getLogger(__name__)


def delete_data(conn) :
    """
    DB에 14일이 경과된 data를 삭제하는 함수
    
    Args:
        conn: DB연결 객체
    """
    
    cursor = create_cursor(conn)
    if cursor == None :
        return
    
    # data 삭제용 sql 
    sql = "delete from news where publish_dt <= (now() - interval 14 day)"
   
    try:
        cursor.execute(sql)
    except Exception as e:
        conn.rollback()
        logger.error("delete 실패 : %s", e)
        return
    
    deleted = cursor.rowcount
    logger.info("delete %s개",deleted)
        
    conn.commit()
    close(cursor) 
            
    
        
 
