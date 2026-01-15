from .db_insert import *
from .db_select import *
from .db_update import *

def save_news(conn, news_list: list) :
    """
    news_table에 data를 저장한다

    Args:
        conn: DB연결 객체
        news_list (list): news의 정보
    """
   

    # auto_increment 방지를 위한 select sql
    select_no_sql = "select no from news where link = %s"
    
    # data insert sql
    insert_sql = "insert into news (title, link, publish_dt) values (%s, %s, %s)"
    
    for news in news_list:

        # select의 필요한 value
        select_no_value = news['rel_link']
        # 이미 존재하는 데이터이므로 title, write_dt비교후 다르면 update실행
        no_result = select(conn, select_no_sql, select_no_value)
        if len(no_result) != 0:
            # 이미있는 news일때 title, 기사시간을 비교후 조건에 맞으면 update되는 쿼리
            update_sql = "update news set title = %s, news_update_dt = %s, db_update_dt = now() where no = %s and (title <> %s or (news_update_dt is null and publish_dt <> %s) or (news_update_dt is not null and news_update_dt <> %s)) "
            update_values = (news['title'], news['write_dt'], no_result[0][0], news['title'], news['write_dt'], news['write_dt'])
            update(conn, update_sql, update_values)
            continue 
                
        
        # insert의 필요한 values
        insert_values = (news['title'], news['rel_link'][0], news['write_dt'])

        # insert 함수 호출
        insert(conn, insert_sql, insert_values)

        
