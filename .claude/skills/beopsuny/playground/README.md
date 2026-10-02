# 법순이 Playground - 평가 및 데모 시나리오

이 디렉토리는 beopsuny-skill의 기능을 평가하고 데모하기 위한 시나리오와 샘플 쿼리를 포함합니다.

## 📋 목적

1. **기능 검증**: API 키 없이도 스킬의 핵심 로직 테스트
2. **사용 예제**: 실제 사용 시나리오 기반 샘플 쿼리
3. **CI 통합**: 로컬 환경에서 실행 가능한 테스트
4. **교육 자료**: 새 사용자를 위한 학습 리소스

## ⚠️ 면책 고지

**이 playground의 모든 예제는 교육 및 기술 데모 목적입니다.**
- 실제 법률 자문이 아닙니다
- 구체적인 법률 문제는 변호사와 상담하세요
- 법령과 판례는 수시로 변경될 수 있습니다

## 🎯 시나리오 목록

### 1. 법령 검색 시나리오
- `scenarios/01_law_search.md` - 법령명 정확 검색
- `scenarios/02_keyword_search.md` - 키워드 기반 검색
- `scenarios/03_administrative_rules.md` - 행정규칙 검색

### 2. 판례 검색 시나리오
- `scenarios/04_case_search.md` - 판례 키워드 검색
- `scenarios/05_case_citation.md` - 판례 인용 형식

### 3. 정책 동향 시나리오
- `scenarios/06_policy_tracking.md` - 정부 정책 집행 동향
- `scenarios/07_bill_tracking.md` - 국회 의안 추적

### 4. 복합 시나리오
- `scenarios/08_full_research.md` - 법령→행정규칙→판례→정책 종합 조사

## 🧪 테스트 실행

### API 키 불필요 (항상 실행 가능)
```bash
# 링크 생성 로직 테스트
python tests/test_link_generation.py

# 파싱 로직 테스트
python tests/test_parsing.py

# 캐시 동작 테스트
python tests/test_cache.py
```

### API 키 필요 (환경변수 설정 시 실행)
```bash
# 실제 API 호출 통합 테스트
python tests/test_integration.py

# Skip 노트: BEOPSUNY_OC_CODE 환경변수 없으면 자동 스킵
```

## 📁 디렉토리 구조

```
playground/
├── README.md                    # 이 파일
├── scenarios/                   # 사용 시나리오 예제
│   ├── 01_law_search.md
│   ├── 02_keyword_search.md
│   └── ...
├── sample_queries.md            # 빠른 참조용 쿼리 모음
└── expected_outputs/            # 예상 출력 예제

tests/
├── test_link_generation.py      # 링크 생성 단위 테스트
├── test_parsing.py               # XML/마크다운 파싱 테스트
├── test_cache.py                 # 캐시 메커니즘 테스트
├── test_integration.py           # API 통합 테스트 (키 필요)
└── fixtures/                     # 테스트용 샘플 데이터
    ├── sample_law.xml
    ├── sample_case.xml
    └── mock_api_responses.json
```

## 🚦 CI 실행 가이드

로컬 CI 환경에서 실행 시:

```bash
# 1. 의존성 없음 - Python 표준 라이브러리만 사용
# 2. API 키 불필요 테스트만 실행
python -m pytest tests/ -m "not requires_api"

# 3. API 키 있으면 전체 테스트 실행
export BEOPSUNY_OC_CODE="your_code"
python -m pytest tests/
```

## 📖 학습 순서

1. `sample_queries.md` - 빠른 시작 쿼리 확인
2. `scenarios/01_law_search.md` - 기본 법령 검색 학습
3. `scenarios/03_administrative_rules.md` - 실무 핵심인 행정규칙 이해
4. `scenarios/08_full_research.md` - 종합 리서치 워크플로우

## 🔍 주요 학습 포인트

### 1. 정확한 법령 검색 (`exact` vs `search`)
- `search "상법"` → "보상법", "손해배상법" 등 부분 일치
- `exact "상법"` → 정확히 "상법"만 검색

### 2. 행정규칙의 중요성
- 법률: 큰 틀만 규정
- 행정규칙: 구체적 기준, 절차, 서식, 부과기준

### 3. 정책 집행 스탠스
- 같은 법 조문도 정부 기조에 따라 적용 강도 상이
- 최근 제재 사례로 현 정부 방향 파악

## 📝 기여 가이드

새로운 시나리오나 테스트 추가 시:
1. `scenarios/` 디렉토리에 마크다운 파일 작성
2. API 키 필요 여부 명시
3. 예상 출력 포함
4. 면책 고지 포함

## 🔗 관련 문서

- [SKILL.md](../SKILL.md) - 전체 스킬 문서
- [AGENTS.md](/workspace/AGENTS.md) - AI 에이전트 지침
- [README.md](/workspace/README.md) - 프로젝트 개요
