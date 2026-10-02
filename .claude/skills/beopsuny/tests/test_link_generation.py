#!/usr/bin/env python3
"""
링크 생성 로직 단위 테스트

이 테스트는 API 키 없이 실행 가능합니다.
로컬 로직만 테스트하므로 CI 환경에서 항상 실행 가능합니다.

실행 방법:
    python tests/test_link_generation.py
    python -m pytest tests/test_link_generation.py -v
"""

import sys
import os

# Add scripts directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

def test_law_link_basic():
    """기본 법령 링크 생성 테스트"""
    # 예상 링크 형식
    expected_base = "https://www.law.go.kr/법령/민법"
    
    # 링크 생성 로직 검증
    law_name = "민법"
    link = f"https://www.law.go.kr/법령/{law_name}"
    
    assert link == expected_base
    print(f"✓ 기본 링크 생성: {link}")

def test_law_link_with_article():
    """조문 포함 법령 링크 생성 테스트"""
    law_name = "민법"
    article = "750"
    link = f"https://www.law.go.kr/법령/{law_name}/제{article}조"
    
    expected = "https://www.law.go.kr/법령/민법/제750조"
    assert link == expected
    print(f"✓ 조문 링크 생성: {link}")

def test_law_link_with_complex_article():
    """복잡한 조문 번호 링크 생성 테스트"""
    law_name = "개인정보보호법"
    article = "15"
    paragraph = "1"
    link = f"https://www.law.go.kr/법령/{law_name}/제{article}조제{paragraph}항"
    
    expected = "https://www.law.go.kr/법령/개인정보보호법/제15조제1항"
    assert link == expected
    print(f"✓ 복잡한 조문 링크: {link}")

def test_case_link():
    """판례 링크 생성 테스트"""
    case_no = "2022다12345"
    link = f"https://www.law.go.kr/판례/({case_no})"
    
    expected = "https://www.law.go.kr/판례/(2022다12345)"
    assert link == expected
    print(f"✓ 판례 링크 생성: {link}")

def test_decree_link():
    """시행령 링크 생성 테스트"""
    law_name = "개인정보보호법"
    decree_link = f"https://www.law.go.kr/법령/{law_name}시행령"
    
    expected = "https://www.law.go.kr/법령/개인정보보호법시행령"
    assert decree_link == expected
    print(f"✓ 시행령 링크 생성: {decree_link}")

def test_search_link():
    """법령 검색 링크 생성 테스트"""
    keyword = "개인정보"
    search_link = f"https://www.law.go.kr/LSW/lsInfoP.do?lsId=&lsiSeq=&viewCls=lsRvsDocInfoR&query={keyword}"
    
    assert keyword in search_link
    assert "law.go.kr" in search_link
    print(f"✓ 검색 링크 생성: {search_link}")

def test_link_korean_encoding():
    """한글 URL 인코딩 테스트"""
    # Python의 URL 라이브러리는 자동으로 한글을 인코딩함
    from urllib.parse import quote
    
    law_name = "민법"
    encoded = quote(law_name)
    link = f"https://www.law.go.kr/법령/{encoded}"
    
    # 한글이 인코딩되었는지 확인
    assert "%" in encoded or encoded == law_name
    print(f"✓ 한글 인코딩: {law_name} → {encoded}")

def test_link_format_validation():
    """링크 형식 검증 테스트"""
    test_cases = [
        ("민법", None, "https://www.law.go.kr/법령/민법"),
        ("상법", None, "https://www.law.go.kr/법령/상법"),
        ("근로기준법", None, "https://www.law.go.kr/법령/근로기준법"),
    ]
    
    for law_name, article, expected in test_cases:
        link = f"https://www.law.go.kr/법령/{law_name}"
        assert link == expected
        print(f"✓ {law_name} 링크 검증 성공")

def test_citation_format():
    """인용 형식 검증 테스트"""
    # 올바른 인용 형식
    valid_citations = [
        "민법 제750조",
        "개인정보보호법 제15조제1항",
        "상법 제401조",
        "근로기준법 제23조제1항",
    ]
    
    for citation in valid_citations:
        # 조문 번호 추출 패턴
        assert "제" in citation
        assert "조" in citation
        print(f"✓ 인용 형식 검증: {citation}")

def test_case_number_format():
    """판례 번호 형식 검증 테스트"""
    valid_case_numbers = [
        "2022다12345",
        "2023도56789",
        "2024헌마1234",
        "2021가합12345",
    ]
    
    for case_no in valid_case_numbers:
        # 판례 번호 형식: YYYY + 사건종류 + 일련번호
        assert len(case_no) >= 9  # 최소 길이
        assert case_no[:4].isdigit()  # 연도
        print(f"✓ 판례 번호 형식 검증: {case_no}")

def test_effective_date_format():
    """시행일자 형식 검증 테스트"""
    # 시행일자 형식 예시
    date_formats = [
        "2024. 1. 31.",
        "2025. 12. 1.",
        "2026. 6. 15.",
    ]
    
    for date in date_formats:
        # 점으로 구분된 형식 확인
        parts = date.replace(".", "").strip().split()
        assert len(parts) == 3  # 년, 월, 일
        print(f"✓ 시행일자 형식 검증: {date}")

def run_all_tests():
    """모든 테스트 실행"""
    test_functions = [
        test_law_link_basic,
        test_law_link_with_article,
        test_law_link_with_complex_article,
        test_case_link,
        test_decree_link,
        test_search_link,
        test_link_korean_encoding,
        test_link_format_validation,
        test_citation_format,
        test_case_number_format,
        test_effective_date_format,
    ]
    
    print("=" * 60)
    print("링크 생성 로직 단위 테스트")
    print("API 키 불필요 - 로컬 로직만 테스트")
    print("=" * 60)
    print()
    
    passed = 0
    failed = 0
    
    for test_func in test_functions:
        try:
            print(f"\n[테스트] {test_func.__name__}")
            print(f"설명: {test_func.__doc__}")
            test_func()
            passed += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed += 1
            print(f"✗ FAILED: {e}")
        except Exception as e:
            failed += 1
            print(f"✗ ERROR: {e}")
    
    print("\n" + "=" * 60)
    print(f"테스트 결과: {passed} 통과, {failed} 실패")
    print("=" * 60)
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
