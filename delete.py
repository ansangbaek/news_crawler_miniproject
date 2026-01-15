import sys
from repository import *
import logging_config as log_con


def delete_main():
    """
    14일이지난 함수를 삭제하기 위한 실행함수

    Args:
        conn (_type_): _description_
    """
    log_con.setup_logging()
    logger = logging.getLogger(__name__)


    # DB 연결 생성
    conn = create_conn()
    if conn is None:
        sys.exit()
    
    # 삭제 함수 호출
    delete_data(conn)

    # 연결 종료
    close(conn)


if __name__ == "__main__" :
    delete_main()

