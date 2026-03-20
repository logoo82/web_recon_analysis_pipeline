import requests

'''
1. inputs 순회
2. name 없는 것 제외
3. type에 따라 값 넣기
4. hidden은 기존 value 유지
5. text/password는 test값 넣기
'''
# 폼 구조를 실제 제출 가능한 데이터로 바꾸는 역할
def build_form_data(form:dict) -> dict:
    data = {}
    
    for input_info in form.get("inputs", []):
        name = input_info.get("name")
        input_type = input_info.get("type", "text")
        value = input_info.get("value", "")
        
        if not name:
            continue
        
        if input_type == "hidden":
            data[name] = value
        elif input_type in ("text", "password", "search", "email"):
            data[name] = "test"
        else:
            data[name] = value
    return data
    
def submit_form(form:dict) -> dict:
    action = form.get("action", "")
    method = form.get("method", "GET").upper()
    
    data = build_form_data(form)
    
    try:
        # method가 GET이면 params=data
        if method == "GET":
            response = requests.get(action, params = data, timeout = 5, allow_redirects=True)
        # method가 POST이면 data=data
        else:
            response = requests.post(action, data = data, timeout = 5, allow_redirects=True)
        result = {
            "form_action": action,
            "method": method,
            "status_code": response.status_code,
            "final_url": response.url,
            "redirected": len(response.history) > 0,
            "submitted_data": data,
            "content_type": response.headers.get("Content-Type", "")
        }
        return result
    except Exception as e:
        return{
            "form_action": action,
            "method": method,
            "submitted_data": data,
            "error": str(e)
        }
    
if __name__ == "__main__":
    test_form = {
        "action": "http://example.com/search",
        "method": "GET",
        "enctype": "",
        "inputs": [
            {"name": "q", "type": "text", "value": ""}
        ]
    }
    print(submit_form(test_form))