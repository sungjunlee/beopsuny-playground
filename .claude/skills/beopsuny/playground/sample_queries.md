# 샘플 쿼리 모음 - 빠른 참조

이 문서는 beopsuny-skill의 주요 기능을 빠르게 테스트할 수 있는 샘플 쿼리 모음입니다.

⚠️ **면책**: 이 쿼리들은 기술 데모 목적이며, 실제 법률 자문이 아닙니다.

## 🔍 법령 검색

### 정확한 법령명 검색 (권장)
```bash
# 정확히 "민법"만 검색
python scripts/fetch_law.py exact "민법"

# "상법"과 관련 시행령/시행규칙
python scripts/fetch_law.py exact "상법"

# 개인정보보호법 + 관련 행정규칙
python scripts/fetch_law.py exact "개인정보보호법" --with-admrul
```

**예상 동작**: 정확히 일치하는 법령만 반환, 관련 시행령/시행규칙 목록 표시

### 키워드 검색
```bash
# "개인정보" 키워드 검색 (법령만)
python scripts/fetch_law.py search "개인정보" --type law

# 날짜순 정렬
python scripts/fetch_law.py search "민법" --sort date

# 최근 시행 법령
python scripts/fetch_law.py recent --days 30
```

**예상 동작**: 키워드를 포함하는 모든 법령 반환 (부분 일치)

## 📜 행정규칙 검색 ⭐

> **실무 핵심**: 법률만 보지 말고 행정규칙(고시/훈령/예규)을 함께 확인하세요!

```bash
# 개인정보 관련 행정규칙
python scripts/fetch_law.py search "개인정보" --type admrul

# 과징금 부과기준 고시
python scripts/fetch_law.py search "과징금 부과기준" --type admrul

# 금융위원회 규정
python scripts/fetch_law.py search "금융위원회" --type admrul

# 근로기준법 관련 행정규칙
python scripts/fetch_law.py search "근로기준법" --type admrul
```

**예상 동작**: 고시, 훈령, 예규 등 실무 적용 규정 반환 (~23,500건 DB)

**왜 중요한가**: 
- 법률: "과징금을 부과할 수 있다" (범위만 규정)
- 행정규칙: "위반 유형별 구체적 과징금 산정 기준" (실제 적용 기준)

## ⚖️ 판례 검색

```bash
# 불법행위 관련 판례
python scripts/fetch_law.py cases "불법행위 손해배상"

# 대법원 판례만
python scripts/fetch_law.py cases "근로계약 해고" --court 대법원

# 특정 기간 판례
python scripts/fetch_law.py cases "개인정보" --from 20240101
```

**예상 동작**: 키워드 관련 판례 목록, 판례 번호, 요지 반환

## 🔗 링크 생성

```bash
# 법령 링크 (law.go.kr)
python scripts/gen_link.py law "민법" --article 750

# 판례 링크
python scripts/gen_link.py case "2022다12345"

# 시행령/시행규칙 링크
python scripts/gen_link.py decree "개인정보보호법"

# 법령 검색 링크
python scripts/gen_link.py search "개인정보보호법"
```

**예상 동작**: 검증 가능한 law.go.kr 직접 링크 생성
**API 키 필요**: 없음 (로컬 로직만 사용)

## 🏛️ 국회 의안 조회

```bash
# 상법 개정안 추적
python scripts/fetch_bill.py track "상법"

# 최근 30일 발의 법안
python scripts/fetch_bill.py recent --days 30

# 계류 중인 민법 관련 의안
python scripts/fetch_bill.py pending --keyword "민법"

# 특정 의안 표결 현황
python scripts/fetch_bill.py votes --bill-no 2205704
```

**예상 동작**: 국회에 발의된 법률안 검색, 진행 상황, 표결 결과
**API 키 필요**: `BEOPSUNY_ASSEMBLY_API_KEY` (선택사항)
**Skip 조건**: API 키 없으면 에러 메시지와 함께 안내

## 📊 정책 동향 파악 ⭐ NEW

> **실무자 피드백**: "법령 조문보다 정부의 실제 집행 스탠스가 더 중요합니다"

```bash
# 공정거래위원회 보도자료
python scripts/fetch_policy.py rss ftc

# 키워드 필터링
python scripts/fetch_policy.py rss ftc --keyword 과징금

# 고용노동부 임금 관련 보도자료
python scripts/fetch_policy.py rss moel --keyword 임금

# 법령해석례 검색
python scripts/fetch_policy.py interpret "해고"

# 최근 7일 정책 동향 요약
python scripts/fetch_policy.py summary --days 7
```

**예상 동작**: RSS 피드에서 부처별 보도자료 수집, 정책 방향 파악
**API 키 필요**: `BEOPSUNY_OC_CODE` (법령해석례 검색 시)
**Skip 조건**: API 키 없으면 RSS만 수집 (법령해석례는 스킵)

## 📥 법령 다운로드 & 파싱

```bash
# 민법 다운로드 (XML)
python scripts/fetch_law.py fetch --name "민법"

# 시행령 포함 다운로드
python scripts/fetch_law.py fetch --name "민법" --with-decree

# 판례 다운로드
python scripts/fetch_law.py fetch --case "2022다12345"

# 다운로드한 법령 파싱 (XML → Markdown)
python scripts/parse_law.py data/raw/민법_001706.xml

# 특정 조문만 파싱
python scripts/parse_law.py data/raw/민법_001706.xml --article 750
```

**예상 동작**: 
1. XML 파일 `data/raw/`에 저장
2. 파싱 시 Markdown 형식으로 `data/parsed/`에 저장
**API 키 필요**: `BEOPSUNY_OC_CODE` (다운로드 시)

## 🔄 개정 비교

```bash
# 최근 30일 시행 법령
python scripts/fetch_law.py recent --days 30

# 특정 기간 공포 법령
python scripts/fetch_law.py recent --from 20251101 --to 20251130 --date-type anc

# 두 버전 비교
python scripts/compare_law.py data/raw/old.xml data/raw/new.xml --name "민법"
```

**예상 동작**: 개정 전후 조문 비교, 신설/삭제/변경 내용 표시

## 🧪 API 키 없이 실행 가능한 쿼리

다음 쿼리들은 **로컬 로직만 사용**하므로 API 키 없이도 실행 가능합니다:

```bash
# ✅ 링크 생성 (로컬 문자열 처리)
python scripts/gen_link.py law "민법" --article 750
python scripts/gen_link.py case "2022다12345"

# ✅ 파싱 (로컬 XML 파일 처리)
python scripts/parse_law.py tests/fixtures/sample_law.xml

# ✅ 비교 (로컬 XML 파일 비교)
python scripts/compare_law.py tests/fixtures/old.xml tests/fixtures/new.xml

# ✅ 법령 인덱스 조회 (로컬 YAML 파일)
grep -i "민법" .claude/skills/beopsuny/config/law_index.yaml
```

## 🔒 API 키 필요한 쿼리

다음 쿼리들은 **외부 API 호출**이 필요합니다:

```bash
# ❌ BEOPSUNY_OC_CODE 필요
python scripts/fetch_law.py search "민법"
python scripts/fetch_law.py cases "불법행위"
python scripts/fetch_law.py fetch --name "민법"
python scripts/fetch_law.py recent --days 30

# ❌ BEOPSUNY_ASSEMBLY_API_KEY 필요 (선택)
python scripts/fetch_bill.py track "상법"
python scripts/fetch_bill.py recent --days 30
```

**Skip 조건**: 
- API 키 없으면 명확한 에러 메시지 표시
- 에러 메시지에 API 키 발급 방법 안내
- 프로그램은 graceful하게 종료

## 📋 종합 리서치 워크플로우

실제 법률 리서치 시 권장 순서:

```bash
# 1. 법령 정확 검색
python scripts/fetch_law.py exact "개인정보보호법" --with-admrul

# 2. 관련 행정규칙 확인
python scripts/fetch_law.py search "개인정보 과징금" --type admrul

# 3. 판례 검색
python scripts/fetch_law.py cases "개인정보 침해 손해배상"

# 4. 국회 개정안 확인
python scripts/fetch_bill.py track "개인정보보호법"

# 5. 정부 집행 동향 파악
python scripts/fetch_policy.py rss pipc --keyword 제재
python scripts/fetch_policy.py interpret "개인정보"

# 6. 법령 다운로드 및 상세 분석
python scripts/fetch_law.py fetch --name "개인정보보호법" --with-decree
python scripts/parse_law.py data/raw/개인정보보호법_*.xml --article 15
```

## 🎓 학습 경로

1. **초급**: 링크 생성 → 정확한 법령 검색
2. **중급**: 키워드 검색 → 판례 검색 → 다운로드
3. **고급**: 행정규칙 → 정책 동향 → 종합 리서치

## 🔍 트러블슈팅

### API 키 에러
```bash
# 에러: "OC code is required"
# 해결: 환경변수 설정
export BEOPSUNY_OC_CODE="your_code"
```

### 해외 접근 차단
```bash
# 에러: "403 Forbidden" 또는 timeout
# 해결: 프록시 설정 (docs/PROXY_SETUP.md 참조)
export BEOPSUNY_PROXY_TYPE=cloudflare
export BEOPSUNY_PROXY_URL="https://your-worker.workers.dev"
```

### XML 파싱 에러
```bash
# 에러: "mismatched tag" 또는 "not well-formed"
# 원인: Claude Desktop 네트워크 egress 설정
# 해결: Settings > Network egress에서 law.go.kr 도메인 허용
```

## 📚 다음 단계

- 시나리오별 상세 가이드: `scenarios/` 디렉토리
- 통합 테스트: `tests/test_integration.py`
- 실전 예제: `scenarios/08_full_research.md`
