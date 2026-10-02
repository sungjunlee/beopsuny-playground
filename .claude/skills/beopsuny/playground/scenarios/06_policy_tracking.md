# 시나리오 6: 정부 정책 집행 스탠스 파악 ⭐

## 목표
법령 조문을 넘어 정부의 실제 집행 스탠스와 제재 동향을 파악하는 방법을 학습합니다.

## ⚠️ 면책
이 시나리오는 기술 데모 목적이며, 실제 법률 자문이 아닙니다.

## 왜 정책 집행 스탠스가 중요한가?

### 실무자 피드백
> "법령 조문보다 **정부의 실제 집행 스탠스**가 실무에 더 중요합니다.  
> 공정거래위원회, 고용노동부, 금융위원회 등의 최근 제재 동향을 파악해야 합니다."

### 같은 법, 다른 적용

| 상황 | 법령 조문 | 실제 적용 |
|------|----------|----------|
| **강화 기조** | "과태료를 부과할 수 있다" | 최대 금액 부과, 검찰 고발 |
| **완화 기조** | "과태료를 부과할 수 있다" | 경고 처분, 시정 명령 |

**예시**:
- 2024년 공정위: 플랫폼 불공정거래 집중 단속 → 과징금 대폭 증가
- 2023년 금융위: 내부통제 미흡 사례 중점 제재 → 임원 문책 강화

## 사용자 요구사항

> "하도급법 위반 시 과징금이 얼마나 나올까요? 최근 공정위의 제재 사례도 알고 싶습니다."

## 워크플로우

### 1단계: 법령 조문 확인 (기본)

```bash
python scripts/fetch_law.py exact "하도급법"
```

**예상 결과**: 법률 조문에서 과징금 범위 확인 (예: "매출액의 2% 이하")

### 2단계: 행정규칙 확인 (구체적 기준)

```bash
python scripts/fetch_law.py search "하도급법 과징금 부과기준" --type admrul
```

**예상 결과**: 위반 유형별 과징금 산정 기준 고시

### 3단계: 정부 정책 동향 파악 ⭐ (실제 집행)

#### 방법 A: 부처별 보도자료 수집

**API 키 필요**: ❌ (RSS 피드 공개)

**실행**:
```bash
# 공정거래위원회 보도자료
python scripts/fetch_policy.py rss ftc

# "과징금" 키워드 필터링
python scripts/fetch_policy.py rss ftc --keyword 과징금

# 최근 7일 동향 요약
python scripts/fetch_policy.py summary --days 7
```

**예상 출력**:
```
=== 공정거래위원회 보도자료 ===

[1] 2026-10-01: 대규모 플랫폼사업자 A사에 과징금 100억 원 부과
  - 하도급대금 부당 감액
  - 링크: https://korea.kr/news/...

[2] 2026-09-28: 공정위, 하도급법 위반 집중 점검 실시
  - 2026년 4분기 중점 단속 대상 발표
  - 링크: https://korea.kr/news/...

[3] 2026-09-20: 공정거래위원회 정책 방향 발표
  - 플랫폼 불공정거래 단속 강화
  - 링크: https://korea.kr/news/...
```

**파악 가능한 정보**:
- ✅ 최근 제재 규모 (과징금 100억 원)
- ✅ 집중 단속 분야 (플랫폼 하도급)
- ✅ 정책 기조 (단속 강화)

#### 방법 B: 법령해석례 검색

**API 키 필요**: ✅ `BEOPSUNY_OC_CODE`

**실행**:
```bash
python scripts/fetch_policy.py interpret "하도급"
```

**예상 출력**:
```
=== 법령해석례 검색 결과 ===

[1] 법제처 해석례 - 하도급대금 지급 기한 (2025-11-15)
  - 질의: 하도급대금을 60일 후 지급하는 계약이 유효한지?
  - 회신: 하도급법 제13조 위반으로 무효
  - 링크: https://www.law.go.kr/법령해석/(...)

[2] 법제처 해석례 - 부당 특약 (2025-09-20)
  - 질의: "하자 발생 시 원사업자는 책임 없음" 특약의 효력
  - 회신: 하도급법 제3조의3 위반으로 무효
```

### 4단계: 웹검색으로 최근 제재 사례 확인

**API 키 필요**: ❌ (WebSearch 활용)

**검색 쿼리**:
```
"공정거래위원회 제재" 하도급법 2024 2025
"공정위 과징금" 하도급 최근
```

**파악 가능한 정보**:
- 실제 부과된 과징금 규모
- 위반 유형별 제재 수위
- 임원 문책 여부 (검찰 고발, 과태료)

## 💼 부처별 조사 가이드

### 공정거래위원회 (FTC)

**관련 법령**: 공정거래법, 하도급법, 가맹사업법

**조사 방법**:
```bash
# 보도자료
python scripts/fetch_policy.py rss ftc

# 키워드 필터
python scripts/fetch_policy.py rss ftc --keyword 하도급
python scripts/fetch_policy.py rss ftc --keyword 가맹
python scripts/fetch_policy.py rss ftc --keyword 불공정
```

**주요 관심사항**:
- 플랫폼 불공정거래 단속
- 하도급대금 지급 지연
- 가맹점 불공정 계약
- 과징금 부과 규모

### 고용노동부 (MOEL)

**관련 법령**: 근로기준법, 산업안전보건법, 최저임금법

**조사 방법**:
```bash
python scripts/fetch_policy.py rss moel --keyword 임금
python scripts/fetch_policy.py rss moel --keyword 해고
python scripts/fetch_policy.py rss moel --keyword 산재
```

**주요 관심사항**:
- 부당해고 구제 명령
- 임금 체불 사업주 명단 공개
- 중대재해 처벌 동향
- 최저임금 위반 단속

### 금융위원회 (FSC)

**관련 법령**: 자본시장법, 금융소비자보호법

**조사 방법**:
```bash
python scripts/fetch_policy.py rss fsc --keyword 제재
python scripts/fetch_policy.py rss fsc --keyword 과징금
python scripts/fetch_policy.py rss fsc --keyword 내부통제
```

**주요 관심사항**:
- 불완전판매 제재
- 내부통제 미흡 임원 문책
- 전산장애 과태료
- 자금세탁방지 위반

### 개인정보보호위원회 (PIPC)

**관련 법령**: 개인정보보호법

**조사 방법**:
```bash
python scripts/fetch_policy.py rss pipc --keyword 과징금
python scripts/fetch_policy.py rss pipc --keyword 유출
python scripts/fetch_policy.py rss pipc --keyword 제재
```

**주요 관심사항**:
- 개인정보 유출 과징금
- 동의 없는 수집·이용 제재
- 제3자 제공 위반

## 🎯 실무 적용 시나리오

### 시나리오: 하도급법 컴플라이언스

**상황**: 원사업자가 하도급대금 지급 기한 준수 여부 검토

**조사 순서**:

1. **법령 확인**
   ```bash
   python scripts/fetch_law.py exact "하도급법"
   ```
   → 제13조: 하도급대금 60일 이내 지급

2. **행정규칙 확인**
   ```bash
   python scripts/fetch_law.py search "하도급 부과기준" --type admrul
   ```
   → 위반 시 과징금 산정 기준

3. **최근 제재 동향**
   ```bash
   python scripts/fetch_policy.py rss ftc --keyword 하도급
   ```
   → 2026년 4분기 집중 단속 중!

4. **법령해석례**
   ```bash
   python scripts/fetch_policy.py interpret "하도급대금"
   ```
   → 60일 초과 지급 계약은 무효

5. **웹검색**
   ```
   "공정거래위원회 하도급법 제재" 2026
   ```
   → 최근 과징금 100억 원 부과 사례

**결론**: 
- 법령 조문: 60일 이내 지급 의무
- 행정규칙: 위반 시 매출액 2% 이하 과징금
- **정책 기조**: 2026년 집중 단속 중 → 강력 제재 예상 ⚠️

## ✅ 검증 체크리스트

- [ ] 법령 조문만으로 판단하지 않기
- [ ] 행정규칙에서 구체적 기준 확인
- [ ] **부처별 보도자료에서 정책 방향 파악**
- [ ] **최근 제재 사례로 실제 집행 수위 확인**
- [ ] 법령해석례에서 유권해석 확인
- [ ] 웹검색으로 언론 보도 교차 검증

## 📊 정책 기조 파악 체크포인트

### 강화 신호 🔴
- "집중 단속", "중점 점검", "강화"
- 과징금 규모 증가
- 임원 문책 사례 증가
- 검찰 고발 건수 증가

### 완화 신호 🟢
- "자율 개선", "계도 기간", "유예"
- 경고 처분 비율 증가
- 과징금 감경 사례 증가

### 현상 유지 🟡
- 특별한 언급 없음
- 과징금 규모 전년 유사

## 🔄 통합 워크플로우

```bash
# === 종합 리서치 체크리스트 ===

# 1. 법령 (법적 근거)
python scripts/fetch_law.py exact "하도급법"

# 2. 행정규칙 (구체적 기준)
python scripts/fetch_law.py search "하도급 과징금" --type admrul

# 3. 정책 동향 (집행 스탠스) ⭐
python scripts/fetch_policy.py rss ftc --keyword 하도급
python scripts/fetch_policy.py interpret "하도급"

# 4. 판례 (판단 기준)
python scripts/fetch_law.py cases "하도급법 위반"

# 5. 국회 동향 (법 개정 가능성)
python scripts/fetch_bill.py track "하도급법"
```

## 📝 출력 템플릿

```markdown
## 하도급법 위반 과징금 분석

### 1. 법령 근거
- **하도급법 제13조**: 하도급대금을 60일 이내 지급
- **제30조**: 위반 시 매출액의 2% 이하 과징금

### 2. 행정규칙 (구체적 기준)
- **"하도급거래 공정화에 관한 법률 위반에 대한 과징금 부과기준"** (공정위 고시)
- 위반 유형별 과징금 산정 공식
- 가중/감경 사유

### 3. 정책 집행 동향 ⭐
- **2026년 4분기**: 공정위 하도급법 집중 점검 (2026-09-28 보도자료)
- **최근 제재 사례**: A사 100억 원 과징금 부과 (2026-10-01)
- **정책 기조**: 플랫폼 하도급거래 단속 강화 ⚠️

### 4. 법령해석례
- **법제처 해석 (2025-11-15)**: 60일 초과 지급 계약은 무효

### 5. 판례
- 대법원 2025. 3. 15. 선고 2024다12345 판결
  - 하도급대금 지급 지연에 대한 손해배상 책임 인정

### 종합 판단
- 법적 의무: 60일 이내 지급 (명확)
- 위반 시 제재: 매출액 2% 이하 과징금 (원칙)
- **현재 집행 수위**: 강화 기조 → 최대한도 부과 예상 🔴

---

⚠️ **참고**: 이 정보는 일반적인 법률 정보 제공 목적이며, 구체적인 법률 문제는 변호사와 상담하시기 바랍니다.
```

## 🚀 고급 활용

### 부처 간 정책 비교
```bash
# 노동 vs 공정거래 집행 강도 비교
python scripts/fetch_policy.py rss ftc --keyword 과징금 > ftc.txt
python scripts/fetch_policy.py rss moel --keyword 과태료 > moel.txt
```

### 시계열 동향 분석
```bash
# 최근 30일 vs 이전 30일 비교
python scripts/fetch_policy.py summary --days 30
python scripts/fetch_policy.py summary --from 20260801 --to 20260831
```

## 🔗 관련 시나리오

- [03_administrative_rules.md](03_administrative_rules.md) - 행정규칙 검색
- [07_bill_tracking.md](07_bill_tracking.md) - 국회 의안 추적
- [08_full_research.md](08_full_research.md) - 종합 리서치

## 📚 참고 자료

- 정책브리핑(korea.kr) - 부처별 RSS 피드
- 공정위 보도자료: https://www.ftc.go.kr
- 고용노동부 보도자료: https://www.moel.go.kr
- 금융위원회 보도자료: https://www.fsc.go.kr
- 개인정보보호위원회: https://www.pipc.go.kr
