from bs4 import BeautifulSoup


def parse_rss(html) :
    """
    rss의 html의 정보를 분석한다
    Args:
        html (str): html_body(text)형식

    Returns:
        list: link의 list를 반환 
    """
    soup  = BeautifulSoup(html, 'html.parser')
    
    # input태그의 name속성이 rss인 값(rss_link) 수집
    links = [a.get('value') for a in soup.select('input[name="rss"]')]

    link_list = []

    # rss 전체 링크를 돌면서 "뉴스 카테고리"에 해당하는 링크만 추출
    for link in links:
        if '?' not in link or ('mkind' in link or 'skind' in link) :
            continue
        else :
            link_list.append(link)

    return link_list
