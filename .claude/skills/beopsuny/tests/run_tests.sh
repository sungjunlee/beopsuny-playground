#!/bin/bash
#
# 법순이 테스트 실행 스크립트
# Beopsuny Test Runner
#
# API 키 없이 실행 가능한 테스트를 먼저 실행하고,
# API 키가 있으면 통합 테스트도 실행합니다.
#
# Usage:
#   ./tests/run_tests.sh           # 모든 테스트
#   ./tests/run_tests.sh --local   # 로컬 테스트만
#   ./tests/run_tests.sh --api     # API 테스트만

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 스크립트 디렉토리
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "============================================================"
echo "법순이 (Beopsuny) 테스트 스위트"
echo "============================================================"
echo ""

# 로컬 테스트 (API 키 불필요)
run_local_tests() {
    echo -e "${GREEN}[1/3] 로컬 테스트 (API 키 불필요)${NC}"
    echo "------------------------------------------------------------"
    
    cd "$SKILL_DIR"
    
    local passed=0
    local failed=0
    
    # 링크 생성 테스트
    echo ""
    echo "▶ 링크 생성 테스트..."
    if python3 tests/test_link_generation.py; then
        ((passed++))
        echo -e "${GREEN}✓ test_link_generation.py PASSED${NC}"
    else
        ((failed++))
        echo -e "${RED}✗ test_link_generation.py FAILED${NC}"
    fi
    
    # XML 파싱 테스트
    echo ""
    echo "▶ XML 파싱 테스트..."
    if python3 tests/test_parsing.py; then
        ((passed++))
        echo -e "${GREEN}✓ test_parsing.py PASSED${NC}"
    else
        ((failed++))
        echo -e "${RED}✗ test_parsing.py FAILED${NC}"
    fi
    
    echo ""
    echo "로컬 테스트 결과: $passed 통과, $failed 실패"
    
    return $failed
}

# API 테스트 (API 키 필요)
run_api_tests() {
    echo ""
    echo -e "${GREEN}[2/3] API 통합 테스트 (API 키 필요)${NC}"
    echo "------------------------------------------------------------"
    
    if [ -z "$BEOPSUNY_OC_CODE" ]; then
        echo -e "${YELLOW}⚠ SKIP: BEOPSUNY_OC_CODE 환경변수 없음${NC}"
        echo ""
        echo "API 키 설정 방법:"
        echo "  export BEOPSUNY_OC_CODE=\"your_oc_code\""
        echo "  발급: https://open.law.go.kr"
        return 0
    fi
    
    cd "$SKILL_DIR"
    
    if [ -f "tests/test_integration.py" ]; then
        echo ""
        echo "▶ 통합 테스트..."
        if python3 tests/test_integration.py; then
            echo -e "${GREEN}✓ test_integration.py PASSED${NC}"
            return 0
        else
            echo -e "${RED}✗ test_integration.py FAILED${NC}"
            return 1
        fi
    else
        echo -e "${YELLOW}⚠ test_integration.py 파일 없음 (구현 예정)${NC}"
        return 0
    fi
}

# pytest 실행 (설치되어 있으면)
run_pytest() {
    echo ""
    echo -e "${GREEN}[3/3] pytest 실행 (선택사항)${NC}"
    echo "------------------------------------------------------------"
    
    if ! command -v pytest &> /dev/null; then
        echo -e "${YELLOW}⚠ SKIP: pytest 미설치${NC}"
        echo "설치: pip install pytest pytest-cov"
        return 0
    fi
    
    cd "$SKILL_DIR"
    
    echo ""
    echo "▶ pytest 실행..."
    
    if [ -n "$BEOPSUNY_OC_CODE" ]; then
        # API 키 있으면 전체 테스트
        pytest tests/ -v --tb=short
    else
        # API 키 없으면 로컬 테스트만
        pytest tests/ -v --tb=short -m "not requires_api" 2>/dev/null || \
        pytest tests/ -v --tb=short
    fi
}

# 메인 실행
main() {
    local mode="${1:-all}"
    local exit_code=0
    
    case "$mode" in
        --local)
            run_local_tests || exit_code=$?
            ;;
        --api)
            run_api_tests || exit_code=$?
            ;;
        --pytest)
            run_pytest || exit_code=$?
            ;;
        *)
            run_local_tests || exit_code=$?
            run_api_tests || exit_code=$?
            run_pytest || true  # pytest는 실패해도 무시
            ;;
    esac
    
    echo ""
    echo "============================================================"
    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}✓ 테스트 완료${NC}"
    else
        echo -e "${RED}✗ 일부 테스트 실패 (exit code: $exit_code)${NC}"
    fi
    echo "============================================================"
    
    return $exit_code
}

# 스크립트 실행
main "$@"
