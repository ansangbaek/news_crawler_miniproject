from .db_insert import *
from .db_select import *



def save_category(conn, news_list: list) :
    """
    news_category table에 data를 저장한다
    
    Args:
        conn: DB연결 객체
        news_list (list): news의 정보
    
    """



    # 같은 link의 정보를 가진 news테이블의 no을 가져오기 위한 select sql
    select_sql = "select no from news where link = %s"

    # news_category 테이블에 insert 하기위한 sql 
    insert_sql = "insert into news_category (no, category_id) values (%s, %s) on duplicate key update category_id = values(category_id)"

    for news in news_list:
        
        # 카테고리 파악을 위한 link의 11번째 index 추출
        value = news['link'][-11]
        
        # 문자열 중 '1' ~ '6' 이 아니면 건너뜀
        if not (value.isdigit() and 1 <= int(value) <= 6) :
            continue

        cat_id = "cat00" + value
        
        # select에 필요한 값 저장           
        select_values = (news['rel_link'])

        # select sql 실행
        result = select(conn, select_sql, select_values)
        
        # select에 실패했거나 값이 없으면 건너뜀
        if len(result) == 0:
            continue 
        
        # insert에 필요한 값 저장
        insert_values = (result[0][0], cat_id)
        # insert 실행
        insert(conn, insert_sql, insert_values)
        
