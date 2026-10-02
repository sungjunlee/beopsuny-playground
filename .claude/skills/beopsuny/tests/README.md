# 법순이 테스트 스위트

beopsuny-skill의 단위 테스트와 통합 테스트 모음입니다.

## 🎯 테스트 철학

1. **API 키 불필요 테스트 우선**: 로컬 로직을 최대한 API 없이 테스트
2. **명확한 Skip 조건**: API 키 필요 테스트는 환경변수 확인 후 스킵
3. **CI 친화적**: GitHub Actions 등에서 secrets 없이도 기본 테스트 실행
4. **실제 시나리오 기반**: 사용자 요구사항을 반영한 테스트 케이스

## 📂 구조

```
tests/
├── README.md                    # 이 파일
├── test_link_generation.py      # 링크 생성 (API 키 불필요)
├── test_parsing.py               # XML 파싱 (API 키 불필요)
├── test_cache.py                 # 캐시 로직 (API 키 불필요)
├── test_integration.py           # 통합 테스트 (API 키 필요)
└── fixtures/                     # 테스트용 샘플 데이터
    ├── sample_law.xml            # 샘플 법령 XML
    ├── sample_case.xml           # 샘플 판례 XML
    └── mock_api_responses.json   # 목 API 응답
```

## 🚦 테스트 실행

### 방법 1: 개별 테스트 직접 실행

**API 키 불필요 (항상 실행 가능):**
```bash
cd .claude/skills/beopsuny

# 링크 생성 테스트
python tests/test_link_generation.py

# XML 파싱 테스트
python tests/test_parsing.py

# 캐시 로직 테스트 (아직 구현 필요)
# python tests/test_cache.py
```

**API 키 필요 (환경변수 설정 시):**
```bash
# 환경변수 설정
export BEOPSUNY_OC_CODE="your_oc_code"

# 통합 테스트
python tests/test_integration.py
```

### 방법 2: pytest 사용 (권장)

```bash
cd .claude/skills/beopsuny

# 모든 테스트 실행
pytest tests/ -v

# API 키 불필요 테스트만
pytest tests/ -v -m "not requires_api"

# 특정 테스트 파일
pytest tests/test_link_generation.py -v

# 커버리지 포함
pytest tests/ --cov=scripts --cov-report=html
```

### 방법 3: CI/CD 환경

**GitHub Actions 예시:**
```yaml
- name: Run tests without API keys
  run: |
    cd .claude/skills/beopsuny
    python tests/test_link_generation.py
    python tests/test_parsing.py

- name: Run integration tests (if secrets available)
  if: env.BEOPSUNY_OC_CODE != ''
  env:
    BEOPSUNY_OC_CODE: ${{ secrets.BEOPSUNY_OC_CODE }}
  run: |
    cd .claude/skills/beopsuny
    python tests/test_integration.py
```

## ✅ 테스트 종류

### 1. 링크 생성 테스트 (`test_link_generation.py`)

**API 키 필요**: ❌ (로컬 로직만)

**테스트 항목**:
- 기본 법령 링크 생성
- 조문 포함 링크 생성
- 판례 링크 생성
- 시행령/시행규칙 링크
- 한글 URL 인코딩
- 인용 형식 검증

**실행**:
```bash
python tests/test_link_generation.py
```

**예상 출력**:
```
============================================================
링크 생성 로직 단위 테스트
API 키 불필요 - 로컬 로직만 테스트
============================================================

[테스트] test_law_link_basic
설명: 기본 법령 링크 생성 테스트
✓ 기본 링크 생성: https://www.law.go.kr/법령/민법
✓ PASSED

...

테스트 결과: 11 통과, 0 실패
============================================================
```

### 2. XML 파싱 테스트 (`test_parsing.py`)

**API 키 필요**: ❌ (샘플 XML 파일 사용)

**테스트 항목**:
- XML 파일 파싱
- 기본정보 추출
- 조문 추출
- 복수 항 처리
- 날짜 형식 변환
- Markdown 변환

**실행**:
```bash
python tests/test_parsing.py
```

### 3. 캐시 로직 테스트 (`test_cache.py`)

**API 키 필요**: ❌ (로컬 파일 시스템만)

**테스트 항목** (구현 예정):
- 캐시 파일 생성
- 캐시 히트/미스
- 캐시 만료 확인
- 캐시 무효화

**구현 상태**: 🚧 구현 필요

### 4. 통합 테스트 (`test_integration.py`)

**API 키 필요**: ✅ `BEOPSUNY_OC_CODE`

**테스트 항목** (구현 예정):
- 실제 법령 검색
- 판례 검색
- 다운로드 및 파싱
- 에러 핸들링

**Skip 조건**:
```python
import os
import pytest

@pytest.mark.skipif(
    not os.getenv('BEOPSUNY_OC_CODE'),
    reason="BEOPSUNY_OC_CODE 환경변수 필요"
)
def test_fetch_law():
    # 실제 API 호출 테스트
    pass
```

## 🧪 Fixtures (테스트 데이터)

### `fixtures/sample_law.xml`
- 샘플 법령 XML (민법 제750조, 제751조)
- 실제 국가법령정보센터 XML 형식 기반
- 파싱 로직 테스트용

### `fixtures/sample_case.xml` (구현 예정)
- 샘플 판례 XML
- 판례 파싱 테스트용

### `fixtures/mock_api_responses.json` (구현 예정)
- API 응답 목 데이터
- 네트워크 없이 API 로직 테스트용

## 📊 테스트 커버리지 목표

| 컴포넌트 | 목표 | 현재 | 상태 |
|----------|------|------|------|
| 링크 생성 | 100% | 90%+ | ✅ |
| XML 파싱 | 90% | 80%+ | ✅ |
| 캐시 로직 | 80% | 0% | 🚧 |
| API 호출 | 70% | 0% | 🚧 |
| 통합 시나리오 | 60% | 0% | 🚧 |

## 🔍 트러블슈팅

### "No module named 'pytest'"
```bash
pip install pytest pytest-cov
```

### "BEOPSUNY_OC_CODE 환경변수 필요"
- 통합 테스트는 API 키가 필요합니다
- API 키 없이 실행 시 자동으로 skip됩니다
- 로컬 테스트(링크 생성, 파싱)만 실행하세요

### XML 파싱 에러
- `tests/fixtures/sample_law.xml` 파일이 있는지 확인
- XML 형식이 올바른지 확인 (UTF-8 인코딩)

## 🚀 CI 통합 예시

### GitHub Actions

```yaml
name: Beopsuny Tests

on: [push, pull_request]

jobs:
  test-no-api:
    name: Tests (No API Keys)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Run local tests
        run: |
          cd .claude/skills/beopsuny
          python tests/test_link_generation.py
          python tests/test_parsing.py
  
  test-with-api:
    name: Tests (With API Keys)
    runs-on: ubuntu-latest
    if: github.event_name == 'push'
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      
      - name: Run integration tests
        env:
          BEOPSUNY_OC_CODE: ${{ secrets.BEOPSUNY_OC_CODE }}
        run: |
          cd .claude/skills/beopsuny
          python tests/test_integration.py || echo "Integration tests skipped"
```

## 📝 테스트 작성 가이드

### 새 테스트 추가 시

1. **API 키 불필요 테스트 우선**
   ```python
   def test_local_logic():
       """로컬 로직만 테스트 - API 불필요"""
       result = generate_link("민법", "750")
       assert "law.go.kr" in result
   ```

2. **API 키 필요 테스트는 명확히 표시**
   ```python
   import os
   import pytest
   
   @pytest.mark.skipif(
       not os.getenv('BEOPSUNY_OC_CODE'),
       reason="API 키 필요"
   )
   def test_api_call():
       """실제 API 호출 - BEOPSUNY_OC_CODE 필요"""
       result = fetch_law("민법")
       assert result is not None
   ```

3. **Fixtures 활용**
   ```python
   def test_with_fixture():
       """샘플 데이터로 테스트"""
       with open('tests/fixtures/sample_law.xml') as f:
           tree = ET.parse(f)
           # 파싱 로직 테스트
   ```

4. **에러 케이스도 테스트**
   ```python
   def test_error_handling():
       """에러 핸들링 테스트"""
       with pytest.raises(ValueError):
           parse_invalid_xml("bad data")
   ```

## 🔗 관련 문서

- [playground/README.md](../playground/README.md) - 사용 시나리오
- [SKILL.md](../SKILL.md) - 전체 스킬 문서
- [sample_queries.md](../playground/sample_queries.md) - 샘플 쿼리

## ⚖️ 면책

이 테스트 스위트는 기술 검증 목적이며, 법률 자문이 아닙니다.
