#params.py
#URL과 form에서 서버로 전달될 수 있는 파라미터 이름들을 구조화해서 정리

from urllib.parse import parse_qs, urlparse


#URL에서 query 파라미터 추출
'''
1. URL 파싱
2. query string 파싱
3. 파라미터 이름을 dict로 저장
'''
def extract_query_params(url:str) -> list[dict]:
    params = []
    #1. URL 파싱
    parsed_url = urlparse(url)
    
    #2. query string 파싱
    query_dict = parse_qs(parsed_url.query)
    
    for param_name in query_dict.keys():
        param_info = {
            "name": param_name,
            "source": "query",
            "method": "UNKNOWN",
            "endpoint": url
        }
        
        #3. 파라미터 이름을 dict로 저장
        params.append(param_info)
        
    return params

'''
1. forms 순회
2. 각 forms의 inputs 순회
3. name이 있는 input만 추출
'''

def extract_form_params(forms: list[dict]) -> list[dict]:
    params = []
    
    #1. form 순회
    for form in forms:
        action = form.get("action", "")
        method = form.get("method", "GET").upper()
        
        #2. 각 form의 inputs 순회
        for input_info in  form.get("inputs", []):
            name = input_info.get("name")
            
            if not name:
                continue
            
            param_info = {
                "name": name,
                "source": "form",
                "method": method,
                "endpoint": action
            }
            
            params.append(param_info)
    
    return params
        
        
def merge_params(query_params: list[dict], form_params: list[dict]) -> list[dict]:
    #merge된 parameter
    merged = []
    #중복을 제거하기 위한 집합
    seen = set()
    
    for param in query_params + form_params:
        key = (
            param["name"],
            param["source"],
            param["method"],
            param["endpoint"]
        )
        
        #중복 제거하며 합치기
        if key not in seen:
            seen.add(key)
            merged.append(param)
    
    return merged

if __name__ == "__main__":
    sample_url = "http://target.local/view?id=1&page=2"
    sample_forms = [
        {
            "action": "http://target.local/login",
            "method": "POST",
            "enctype": "",
            "inputs": [
                {"name": "username", "type": "text", "value": ""},
                {"name": "password", "type": "password", "value": ""},
                {"name": None, "type": "submit", "value": "Login"}
            ]
        }
    ]

    query_params = extract_query_params(sample_url)
    form_params = extract_form_params(sample_forms)
    all_params = merge_params(query_params, form_params)

    
    print(all_params)