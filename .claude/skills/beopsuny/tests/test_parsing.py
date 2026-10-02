#!/usr/bin/env python3
"""
XML 파싱 로직 단위 테스트

이 테스트는 API 키 없이 실행 가능합니다.
tests/fixtures/sample_law.xml 파일을 사용하여 파싱 로직을 검증합니다.

실행 방법:
    python tests/test_parsing.py
    python -m pytest tests/test_parsing.py -v
"""

import sys
import os
import xml.etree.ElementTree as ET

# Add scripts directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')
SAMPLE_LAW_XML = os.path.join(FIXTURES_DIR, 'sample_law.xml')

def test_xml_file_exists():
    """샘플 XML 파일 존재 확인"""
    assert os.path.exists(SAMPLE_LAW_XML), f"샘플 XML 파일 없음: {SAMPLE_LAW_XML}"
    print(f"✓ 샘플 XML 파일 확인: {SAMPLE_LAW_XML}")

def test_parse_xml_basic():
    """기본 XML 파싱 테스트"""
    tree = ET.parse(SAMPLE_LAW_XML)
    root = tree.getroot()
    
    assert root.tag == 'law', f"루트 태그가 'law'가 아님: {root.tag}"
    print(f"✓ XML 루트 태그 확인: {root.tag}")

def test_parse_basic_info():
    """법령 기본정보 파싱 테스트"""
    tree = ET.parse(SAMPLE_LAW_XML)
    root = tree.getroot()
    
    basic_info = root.find('기본정보')
    assert basic_info is not None, "기본정보 태그를 찾을 수 없음"
    
    law_id = basic_info.find('법령ID').text
    law_name = basic_info.find('법령명한글').text
    effective_date = basic_info.find('시행일자').text
    
    assert law_id == '001706', f"법령ID 불일치: {law_id}"
    assert law_name == '민법', f"법령명 불일치: {law_name}"
    assert effective_date == '20250131', f"시행일자 불일치: {effective_date}"
    
    print(f"✓ 법령ID: {law_id}")
    print(f"✓ 법령명: {law_name}")
    print(f"✓ 시행일: {effective_date}")

def test_parse_articles():
    """조문 파싱 테스트"""
    tree = ET.parse(SAMPLE_LAW_XML)
    root = tree.getroot()
    
    articles = root.findall('조문')
    assert len(articles) > 0, "조문을 찾을 수 없음"
    
    print(f"✓ 조문 개수: {len(articles)}개")
    
    # 첫 번째 조문 확인
    first_article = articles[0]
    article_no = first_article.find('조문번호').text
    article_title = first_article.find('조문제목').text
    
    assert article_no == '제750조', f"조문번호 불일치: {article_no}"
    assert article_title == '불법행위의 내용', f"조문제목 불일치: {article_title}"
    
    print(f"✓ 첫 번째 조문: {article_no} {article_title}")

def test_parse_article_content():
    """조문 내용 파싱 테스트"""
    tree = ET.parse(SAMPLE_LAW_XML)
    root = tree.getroot()
    
    article = root.find('.//조문[조문번호="제750조"]')
    assert article is not None, "제750조를 찾을 수 없음"
    
    content = article.find('.//항내용').text
    assert '고의 또는 과실' in content, "조문 내용 불일치"
    assert '손해를 배상할 책임' in content, "조문 내용 불일치"
    
    print(f"✓ 조문 내용 확인: {content[:30]}...")

def test_parse_multiple_paragraphs():
    """복수 항 파싱 테스트"""
    tree = ET.parse(SAMPLE_LAW_XML)
    root = tree.getroot()
    
    article = root.find('.//조문[조문번호="제751조"]')
    assert article is not None, "제751조를 찾을 수 없음"
    
    paragraphs = article.findall('.//항')
    assert len(paragraphs) == 2, f"항 개수 불일치: {len(paragraphs)}"
    
    print(f"✓ 제751조 항 개수: {len(paragraphs)}개")
    
    # 각 항의 번호 확인
    for para in paragraphs:
        para_no = para.find('항번호').text
        para_content = para.find('항내용').text
        print(f"  - {para_no}: {para_content[:30]}...")

def test_format_date():
    """날짜 형식 변환 테스트"""
    # YYYYMMDD → YYYY. M. D. 형식 변환
    date_str = "20250131"
    
    year = date_str[:4]
    month = str(int(date_str[4:6]))
    day = str(int(date_str[6:8]))
    
    formatted = f"{year}. {month}. {day}."
    expected = "2025. 1. 31."
    
    assert formatted == expected, f"날짜 형식 불일치: {formatted}"
    print(f"✓ 날짜 변환: {date_str} → {formatted}")

def test_extract_article_number():
    """조문 번호 추출 테스트"""
    test_cases = [
        ("제750조", "750"),
        ("제15조제1항", "15"),
        ("제401조", "401"),
    ]
    
    for full_text, expected_num in test_cases:
        # 조문 번호 추출 로직
        # "제750조" → "750"
        # "제15조제1항" → "15"
        num = full_text.split("조")[0].replace("제", "")
        assert num == expected_num, f"조문 번호 추출 실패: {full_text} → {num}"
        print(f"✓ 조문 번호 추출: {full_text} → {num}")

def test_markdown_conversion():
    """Markdown 변환 로직 테스트"""
    law_name = "민법"
    article_no = "제750조"
    article_title = "불법행위의 내용"
    content = "고의 또는 과실로 인한 위법행위로 타인에게 손해를 가한 자는 그 손해를 배상할 책임이 있다."
    effective_date = "2025. 1. 31."
    
    # Markdown 형식 생성
    markdown = f"""## {law_name} {article_no} ({article_title})

> {content}

- **시행일**: {effective_date}
- **링크**: https://www.law.go.kr/법령/{law_name}/{article_no}
"""
    
    # 생성된 Markdown 검증
    assert law_name in markdown
    assert article_no in markdown
    assert content in markdown
    assert effective_date in markdown
    
    print("✓ Markdown 변환 성공")
    print(markdown)

def test_article_search():
    """특정 조문 검색 테스트"""
    tree = ET.parse(SAMPLE_LAW_XML)
    root = tree.getroot()
    
    target_article = "제750조"
    article = root.find(f'.//조문[조문번호="{target_article}"]')
    
    assert article is not None, f"{target_article}를 찾을 수 없음"
    
    article_title = article.find('조문제목').text
    print(f"✓ 조문 검색: {target_article} - {article_title}")

def test_law_metadata_extraction():
    """법령 메타데이터 추출 테스트"""
    tree = ET.parse(SAMPLE_LAW_XML)
    root = tree.getroot()
    
    basic_info = root.find('기본정보')
    
    metadata = {
        '법령ID': basic_info.find('법령ID').text,
        '법령명': basic_info.find('법령명한글').text,
        '법령종류': basic_info.find('법령종류').text,
        '공포일자': basic_info.find('공포일자').text,
        '시행일자': basic_info.find('시행일자').text,
        '소관부처': basic_info.find('소관부처').text,
    }
    
    # 필수 필드 확인
    for key, value in metadata.items():
        assert value is not None, f"{key} 없음"
        print(f"✓ {key}: {value}")

def run_all_tests():
    """모든 테스트 실행"""
    test_functions = [
        test_xml_file_exists,
        test_parse_xml_basic,
        test_parse_basic_info,
        test_parse_articles,
        test_parse_article_content,
        test_parse_multiple_paragraphs,
        test_format_date,
        test_extract_article_number,
        test_markdown_conversion,
        test_article_search,
        test_law_metadata_extraction,
    ]
    
    print("=" * 60)
    print("XML 파싱 로직 단위 테스트")
    print("API 키 불필요 - 샘플 XML 파일 사용")
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
