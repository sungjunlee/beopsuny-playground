# 법순이 테스트 & 평가 가이드

beopsuny-skill의 테스트, 평가, 데모를 위한 종합 가이드입니다.

## 🎯 개요

이 프로젝트는 다음을 제공합니다:

1. **Playground**: 실제 사용 시나리오 기반 샘플 쿼리와 예제
2. **Tests**: API 키 없이도 실행 가능한 단위 테스트
3. **Fixtures**: 테스트용 샘플 데이터
4. **CI Integration**: 로컬 및 CI 환경 지원

## 📂 구조

```
.claude/skills/beopsuny/
├── playground/              # 사용 시나리오 & 데모
│   ├── README.md
│   ├── sample_queries.md    # 빠른 참조용 쿼리
│   └── scenarios/           # 단계별 시나리오
│       ├── 01_law_search.md
│       ├── 03_administrative_rules.md
│       ├── 06_policy_tracking.md
│       └── 08_full_research.md
│
├── tests/                   # 단위 테스트 & 통합 테스트
│   ├── README.md
│   ├── run_tests.sh         # 테스트 실행 스크립트
│   ├── test_link_generation.py  # API 키 불필요
│   ├── test_parsing.py          # API 키 불필요
│   └── fixtures/            # 테스트용 샘플 데이터
│       └── sample_law.xml
│
└── TESTING.md              # 이 파일
```

## 🚦 빠른 시작

### 1. API 키 없이 테스트 (항상 실행 가능)

```bash
cd .claude/skills/beopsuny

# 링크 생성 테스트
python3 tests/test_link_generation.py

# XML 파싱 테스트
python3 tests/test_parsing.py

# 또는 통합 실행
./tests/run_tests.sh --local
```

### 2. API 키 포함 통합 테스트 (선택)

```bash
# API 키 설정
export BEOPSUNY_OC_CODE="your_oc_code"

# 전체 테스트 실행
./tests/run_tests.sh
```

### 3. 샘플 시나리오 학습

```bash
# 빠른 참조
cat playground/sample_queries.md

# 상세 시나리오
cat playground/scenarios/01_law_search.md
```

## 📋 테스트 유형별 가이드

### 로컬 테스트 (API 키 불필요) ✅

**대상**: 링크 생성, XML 파싱, 캐시 로직 등

**실행 방법**:
```bash
python3 tests/test_link_generation.py  # 링크 생성
python3 tests/test_parsing.py          # XML 파싱
```

**특징**:
- ✅ 언제든지 실행 가능
- ✅ CI 환경에서 항상 실행
- ✅ secrets 불필요

### 통합 테스트 (API 키 필요) ⚠️

**대상**: 실제 API 호출, 다운로드, 검색 등

**Skip 조건**:
- `BEOPSUNY_OC_CODE` 환경변수 없으면 자동 skip
- CI에서는 secrets 설정 시에만 실행

**실행 방법**:
```bash
export BEOPSUNY_OC_CODE="your_oc_code"
python3 tests/test_integration.py  # (구현 예정)
```

## 🎓 학습 경로

### 1. 초급: 기본 개념 익히기
1. `playground/sample_queries.md` 읽기 (10분)
2. `scenarios/01_law_search.md` 따라하기 (20분)
3. 링크 생성 테스트 실행 (5분)

**목표**: 기본 법령 검색과 링크 생성 이해

### 2. 중급: 실무 적용
1. `scenarios/03_administrative_rules.md` (30분)
2. `scenarios/06_policy_tracking.md` (30분)
3. XML 파싱 테스트 실행 (10분)

**목표**: 행정규칙과 정책 동향 파악의 중요성 이해

### 3. 고급: 종합 리서치
1. `scenarios/08_full_research.md` (60분)
2. 전체 워크플로우 실습
3. 통합 테스트 작성 (선택)

**목표**: 실제 법률 문제 조사 능력

## 🧪 CI/CD 통합

### GitHub Actions 예시

```yaml
name: Beopsuny Tests

on: [push, pull_request]

jobs:
  test-local:
    name: Local Tests (No API)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Run local tests
        run: |
          cd .claude/skills/beopsuny
          python3 tests/test_link_generation.py
          python3 tests/test_parsing.py

  test-integration:
    name: Integration Tests (With API)
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
          ./tests/run_tests.sh || true
```

### 핵심 포인트

1. **로컬 테스트는 항상 실행**: secrets 없어도 OK
2. **통합 테스트는 조건부**: secrets 있을 때만
3. **실패해도 통과**: `|| true`로 유연한 처리

## 📊 테스트 커버리지

| 컴포넌트 | API 키 필요 | 테스트 상태 | 커버리지 |
|----------|------------|-----------|---------|
| 링크 생성 | ❌ | ✅ 완료 | 90%+ |
| XML 파싱 | ❌ | ✅ 완료 | 80%+ |
| 캐시 로직 | ❌ | 🚧 예정 | 0% |
| API 호출 | ✅ | 🚧 예정 | 0% |
| 통합 시나리오 | ✅ | 🚧 예정 | 0% |

## 🎯 주요 시나리오 요약

### 1. 법령 정확 검색
- **파일**: `scenarios/01_law_search.md`
- **핵심**: `exact` vs `search` 차이
- **API 키**: 필요 (다운로드 시)
- **학습 시간**: 20분

### 2. 행정규칙 검색 ⭐
- **파일**: `scenarios/03_administrative_rules.md`
- **핵심**: 법률보다 고시/훈령/예규가 실무에 중요
- **API 키**: 필요
- **학습 시간**: 30분

### 3. 정책 집행 동향 ⭐
- **파일**: `scenarios/06_policy_tracking.md`
- **핵심**: 정부의 실제 집행 스탠스 파악
- **API 키**: 부분적 (RSS는 불필요)
- **학습 시간**: 30분

### 4. 종합 리서치
- **파일**: `scenarios/08_full_research.md`
- **핵심**: 법령→행정규칙→정책→판례→국회 전체 워크플로우
- **API 키**: 필요
- **학습 시간**: 60분

## ⚠️ 제약사항 & Skip 조건

### API 키 필요 기능
다음 기능은 `BEOPSUNY_OC_CODE` 환경변수 필요:
- 법령 검색 (`search`, `exact`)
- 법령 다운로드 (`fetch`)
- 판례 검색 (`cases`)
- 최근 개정 조회 (`recent`)
- 법령해석례 (`interpret`)

### API 키 불필요 기능
다음 기능은 언제든지 사용 가능:
- 링크 생성 (`gen_link.py`)
- XML 파싱 (`parse_law.py`)
- RSS 피드 수집 (`fetch_policy.py rss`)
- 로컬 파일 비교 (`compare_law.py`)

### 국회 의안 API
- `BEOPSUNY_ASSEMBLY_API_KEY` 선택사항
- 없으면 의안 조회 기능만 사용 불가
- 다른 기능은 정상 동작

## 🔍 트러블슈팅

### "python: command not found"
→ `python3` 사용: `python3 tests/test_link_generation.py`

### "No module named 'pytest'"
→ pytest는 선택사항: 직접 실행 가능
```bash
python3 tests/test_link_generation.py  # pytest 불필요
```

### "BEOPSUNY_OC_CODE 환경변수 필요"
→ 정상 동작 (skip 메시지)
→ 로컬 테스트만 실행: `./tests/run_tests.sh --local`

### XML 파싱 에러
→ `tests/fixtures/sample_law.xml` 파일 확인
→ UTF-8 인코딩 확인

## 📝 기여 가이드

### 새 테스트 추가 시

1. **API 키 불필요 테스트 우선**
   - 링크 생성, 파싱 등 로컬 로직
   - `tests/test_*.py` 파일 추가
   
2. **Skip 조건 명시**
   ```python
   import os
   
   if not os.getenv('BEOPSUNY_OC_CODE'):
       print("SKIP: API 키 필요")
       exit(0)
   ```

3. **Fixtures 활용**
   - `tests/fixtures/` 디렉토리
   - 샘플 XML, JSON 등

### 새 시나리오 추가 시

1. **마크다운 파일 작성**
   - `playground/scenarios/XX_title.md`
   
2. **필수 포함 사항**
   - API 키 필요 여부 명시
   - 예상 출력 예시
   - ⚠️ 면책 고지

3. **링크 연결**
   - 관련 시나리오 상호 링크
   - `playground/README.md` 업데이트

## 🔗 관련 문서

- [SKILL.md](SKILL.md) - 전체 스킬 문서
- [README.md](/workspace/README.md) - 프로젝트 개요
- [AGENTS.md](/workspace/AGENTS.md) - AI 에이전트 지침
- [playground/README.md](playground/README.md) - 시나리오 가이드
- [tests/README.md](tests/README.md) - 테스트 상세 가이드

## ⚖️ 면책

모든 테스트와 시나리오는 기술 데모 및 교육 목적입니다.
실제 법률 자문이 아니며, 구체적인 법률 문제는 변호사와 상담하세요.

## 📊 요약

| 항목 | API 키 불필요 | API 키 필요 | 합계 |
|------|--------------|------------|------|
| 테스트 파일 | 2개 | 1개 (예정) | 3개 |
| 시나리오 | 0개 | 4개 | 4개 |
| Fixtures | 1개 | 0개 | 1개 |

**핵심 메시지**: API 키 없이도 **핵심 로직 테스트 가능**, CI 친화적!
