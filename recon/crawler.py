#crawler.py
#시작 URL에서 페이지를 방문하고, 그 페이지에서 링크, 폼, 파라미터를 모으는 흐름을 관리
#내부 동작 순서
'''
1. 시작 URL을 방문 후보 목록에 넣음
2. 하나 꺼냄
3. 이미 방문했거나 depth 초과면 건너뜀
4. HTTP 요청으로 HTML 가져옴
5. links.py 호출 -> 링크 추출
6. forms.py 호출 -> 폼 추출
7. params.py 호출 -> query/form 파라미터 정리
8. 새 링크를 다음 방문 후보에 추가
9. 결과를 누적
10. 방문 후보가 없으면 종료
'''


from urllib.parse import urlparse

import requests

from .forms import extract_forms
from .links import extract_links
from .params import extract_form_params, extract_query_params, merge_params


def crawl_target(start_url: str, depth: int = 1) -> dict:
    results = {
        "visited": [],
        "links": [],
        "forms": [],
        "params": [],
        "errors": []
    }
    
    # 이미 방문한 URL 저장용
    visited = set()
    seen_links = set()
    seen_forms = set()
    seen_params = set()
    
    # 방문할 URL과 depth를 같이 저장한다.
    to_visit = [(start_url, 0)]
    
    #시작 URL의 도메인 저장
    start_domain = urlparse(start_url).netloc
    
    while to_visit:
        current_url, current_depth = to_visit.pop(0)
        
        # depth 초과면 건너뜀
        if current_depth > depth:
            continue
        # 이미 방문했으면 건너뜀
        if current_url in visited:
            continue
        
        visited.add(current_url)
        results["visited"].append(current_url)
        # 요청 보내기
        try:
            response = requests.get(current_url, timeout = 5)
            # 응답 상태 확인
            response.raise_for_status()
            html = response.text
        except Exception as e:
            results["errors"].append(
                {
                    "url": current_url,
                    "error": str(e)
                }
            )
            continue
        
        #링크 추출
        links = extract_links(html, current_url)
        #폼 추출
        forms = extract_forms(html, current_url)
        
        # query/form params 추출
        query_params = extract_query_params(current_url)
        
        for link in links:
            query_params.extend(extract_query_params(link))
        form_params = extract_form_params(forms)
        # merged params 생성
        merged_params = merge_params(query_params, form_params)
        
        # 결과 누적
        for link in links:
            if link not in seen_links:
                seen_links.add(link)
                results["links"].append(link)
        
        for form in forms:
            form_key = (
                form["action"],
                form["method"],
                form["enctype"],
                tuple(
                    (inp.get("name"), inp.get("type"))
                    for inp in form.get("inputs", [])
                )
            )
            if form_key not in seen_forms:
                seen_forms.add(form_key)
                results["forms"].append(form)

        for param in merged_params:
            param_key = (
                param["name"],
                param["source"],
                param["method"],
                param["endpoint"]
            )
            if param_key not in seen_params:
                seen_params.add(param_key)
                results["params"].append(param)
                
        for link in links:
            parsed_link = urlparse(link)
            if parsed_link.netloc == start_domain and link not in visited:
                to_visit.append((link, current_depth + 1))
    
    return results

if __name__ == "__main__":
    start_url = input("start_url: ")
    depth = int(input("depth: "))
    
    result = crawl_target(start_url, depth)
    print(result)
        
        