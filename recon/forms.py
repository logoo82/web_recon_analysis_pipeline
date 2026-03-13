#forms.py
#웹사이트를 훑어, 어떤 페이지가 있고, 어떤 입력 지점이 있는 지 모으기
#내부 동작 순서
'''
1. HTML 파싱
2. <form> 태그 모두 찾기
3. 각 form의 action, method, enctype 읽기
4. action을 절대 경로로 바꾸기
5. form 내부의 input 태그 모두 찾기
6. 각 input의 name, type, value 추출
7. form 구조를 dict 자료형으로 만들기
8. 모든 form을 리스트에 담아 반환   
'''
from urllib.parse import urljoin
from bs4 import BeautifulSoup

'''
1. form 내부 input 태그들을 순회
2. name, type, value 추출
3. dict로 저장
4. 리스트 반환
'''


def extract_inputs(form_tag) -> list[dict]:
    inputs = []
    #1. form 내부 input 태그들을 순회
    for input_tag in form_tag.find_all("input"):
        #2. name, type, value 추출
        #3. dict로 저장
        input_info = {
            "name": input_tag.get("name"),
            "type": input_tag.get("type", "text"),
            "value": input_tag.get("value", "")
        }
        inputs.append(input_info)
    
    #4. 리스트 반환
    return inputs

'''
1. HTML 파싱
2. form 태그들 순회
3. action, method, enctype 추출
4. action 절대경로화
5. inputs 추출
6. dict로 저장
7. 리스트 반환
'''

def extract_forms(html: str, base_url:str) -> list[dict]:
    #1. HTML 파싱
    soup = BeautifulSoup(html, 'html.parser')
    
    #결과를 저장할 리스트
    results = []
    
    #2. form 태그 순회
    for form_tag in soup.find_all("form"):
        #3. action, method, enctype 추출
        action = form_tag.get("action", "")
        method = form_tag.get("method", "GET").upper()
        enctype = form_tag.get("enctype", "")

        #4. action 절대경로화
        if action == "":
            absolute_action = base_url
        else:
            absolute_action = urljoin(base_url, action)
        
        #5, 6. inputs 추출 및 form info dict로 저장
        form_info = {
            "action": absolute_action,
            "method": method,
            "enctype": enctype,
            "inputs": extract_inputs(form_tag)
        }
        
        results.append(form_info)
        
        #7. 리스트 반환
    return results

if __name__ == "__main__":
    html = input("html: ")
    base_url = input("base_url: ")
    print(extract_forms(html, base_url))
