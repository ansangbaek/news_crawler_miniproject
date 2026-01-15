import requests
from bs4 import BeautifulSoup
from typing import List
from urllib.parse import urljoin
import logging
import re

logger = logging.getLogger(__name__)

def discover_feeds(page_url: str, timeout: int = 10) -> List[str]:
    """
    page_url(웹페이지)에서 RSS/Atom 피드 링크를 발견해서 절대 URL 목록으로 반환.
    우선순위:
      1) <link rel="alternate" type="application/rss+xml|application/atom+xml"...>
      2) 본문 <a href="...rss|atom|feed|.xml"> 형태 휴리스틱
    """
    headers = {"User-Agent": "Mozilla/5.0 (RSS-Discovery/1.0)"}
    r = requests.get(page_url, headers=headers, timeout=timeout)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    feeds: list[str] = []

    # 1) 표준 feed discovery
    for link in soup.find_all("link", attrs={"rel": re.compile(r"\balternate\b", re.I)}):
        typ = (link.get("type") or "").lower().strip()
        href = (link.get("href") or "").strip()
        if not href:
            continue
        if typ in ("application/rss+xml", "application/atom+xml", "application/rdf+xml", "text/xml", "application/xml"):
            feeds.append(urljoin(page_url, href))

    # 2) 휴리스틱 (일부 사이트는 <a>로만 걸어둠)
    if not feeds:
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if not href:
                continue
            h = href.lower()
            if any(k in h for k in ("rss", "atom", "feed")) or h.endswith((".rss", ".xml")):
                feeds.append(urljoin(page_url, href))

    # 중복 제거(순서 유지)
    uniq = []
    seen = set()
    for f in feeds:
        if f not in seen:
            seen.add(f)
            uniq.append(f)
    return uniq

# url 링크를 dict 전역변수로 모아둠
url_dict = {'boannews': "https://www.boannews.com/"}




def get_rss_urls(key: str):
    """
    url 링크를 찾는 함수

    Args:
        key (str): 저장된 사이트 이름

    Returns:
        str | None: 사이트 url이 있을시 해당 주소, 없을시 None 
    """
    if key in url_dict :
        return discover_feeds(url_dict[key])
    else :
        return None
