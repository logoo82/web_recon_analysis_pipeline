# main.py
# 동작
'''
1. 터미널 명령 읽기
2. 어떤 기능을 실행할 지 결정하기
3. crawler.py 호출하기
4. 결과를 저장하고 요약하기
'''

import argparse

from core.result import save_result
from recon.crawler import crawl_target

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="traceprobe")
    subparsers = parser.add_subparsers(dest="command")
    
    crawl_parser = subparsers.add_parser("crawl", help="Crawl target URL")
    crawl_parser.add_argument("--url", required=True, help="Target URL")
    crawl_parser.add_argument("--depth", type=int, default=1, help="Crawl depth")
    crawl_parser.add_argument("--submit-forms", action="store_true", help="Submit same-domain GET/POST forms")
    
    return parser

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    
    if args.command == "crawl":
        result = crawl_target(args.url, depth=args.depth, submit_forms=args.submit_forms)
        output_path = save_result(result)

        print(f"[+] Crawl finished: {output_path}")
        print(f"Visited: {len(result.get('visited', []))}")
        print(f"Links: {len(result.get('links', []))}")
        print(f"Forms: {len(result.get('forms', []))}")
        print(f"Submitted forms: {len(result.get('submitted_forms', []))}")
        print(f"Params: {len(result.get('params', []))}")
        print(f"Errors: {len(result.get('errors', []))}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
    
    
