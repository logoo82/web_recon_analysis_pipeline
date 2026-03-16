#links.py
#웹페이지의 링크 추출
#내부 동작 순서
''' 
1. HTML 파싱
2. <a> 태그 찾기
3. href 값 꺼내기
4. 상대 경로를 절대 경로로 변환
5. 중복 제거
6. 리스트 반환
'''

from urllib.parse import urldefrag, urljoin, urlparse

from bs4 import BeautifulSoup

# 웹 페이지의 html 문자열
##html = input("html: ")
# 현재 페이지의 기준 url


# 추출한 href 문자열에서 None, 빈 문자열 값은 제외
def should_skip_href(href:str) -> bool:
    if not href:
        return True
    
    href = href.strip()
    
    if href == "":
        return True
    
    #mailto: 이메일, tel: 전화번호, #: 현재 페이지 상단으로 이동등 불필요한 정보 제거
    #javascript를 제거하는 이유: 서버의 URL을 추출하는 데에는 HTML 동작을 담당하는 JS는 필요 없기 때문
    skip_prefixes = ("#", "javascript:", "mailto:", "tel:")
    if href.startswith(skip_prefixes):
        return True
    
    return False


'''
1. HTML 파싱
2. a 태그 찾기
3. href 추출
4. 제외 규칙 적용
5. 절대경로 변환
6. fragment 제거
7. http/https만 남기기
8. 중복 제거 후 반환
'''
def extract_links(html: str, base_url: str) -> list[str]:
    #1. HTMl 파싱
    soup = BeautifulSoup(html, 'html.parser')
    
    # 결과를 보관할 리스트
    results = []
    # 중복을 제거하기 위한 집합
    seen = set()
    
    #2. a태그 찾기
    #3. href 추출
    for link in soup.find_all('a', href=True):
        href = link['href'].strip()

        #4. 제외 규칙 적용
        if should_skip_href(href):
            continue
        
        #5. 절대경로 변환
        absolute_url = urljoin(base_url, href)
        #6 #fragment 제거: HTTP 요청에서 서버로 전송되지 않기 때문
        absolute_url, _ = urldefrag(absolute_url)
        
        #7. http/https만 남기기
        parsed_url = urlparse(absolute_url)
        if parsed_url.scheme not in ("http", "https"):
            continue
        
        #8. 중복 제거 후 반환
        if absolute_url not in seen:
            seen.add(absolute_url)
            results.append(absolute_url)
    
    return results    
        
if __name__ == "__main__":
    html_text = input("html:" )
    base_url = input("base_url: ")
    print(extract_links(html_text, base_url))
