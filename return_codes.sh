#!/bin/bash

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check return code
check_return_code() {
    local cmd="$1"
    local expected="$2"
    local description="$3"
    
    echo -e "${BLUE}Testing:${NC} $description"
    echo -e "${YELLOW}Command:${NC} $cmd"
    
    # Execute command and capture return code
    # Use bash -c to properly handle pipes in eval
    bash -c "$cmd" >/dev/null 2>&1
    local actual=$?
    
    if [ "$actual" -eq "$expected" ]; then
        echo -e "${GREEN}✓ PASS${NC} - Return code: $actual (expected: $expected)"
    else
        echo -e "${RED}✗ FAIL${NC} - Return code: $actual (expected: $expected)"
        FAILED=$((FAILED + 1))
    fi
    echo ""
    
    TOTAL=$((TOTAL + 1))
}

# Initialize counters
TOTAL=0
FAILED=0

echo "========================================"
echo "  CommiZard Return Code Checker"
echo "========================================"
echo ""

# Test 1: Version flag should return 0
check_return_code "commizard -v" 0 "Version flag (-v)"

# Test 2: Version flag (long) should return 0
check_return_code "commizard --version" 0 "Version flag (--version)"

# Test 3: Help flag should return 0
check_return_code "commizard -h" 0 "Help flag (-h)"

# Test 4: Help flag (long) should return 0
check_return_code "commizard --help" 0 "Help flag (--help)"

# Test 5: Run in non-git directory (should return 1)
check_return_code "cd /tmp && commizard <<< 'exit'" 1 "Run outside git repository"

# Test 6: Normal exit should return 0
# Note: These tests may show different results when output is redirected
# Run manually: echo 'exit' | commizard && echo $?
check_return_code "echo 'exit' | commizard 2>/dev/null" 0 "Normal exit with 'exit' command"

# Test 7: Quit command should return 0
check_return_code "echo 'quit' | commizard 2>/dev/null" 0 "Normal exit with 'quit' command"

# Summary
echo "========================================"
echo "  Test Summary"
echo "========================================"
echo -e "Total tests: $TOTAL"
echo -e "${GREEN}Passed: $((TOTAL - FAILED))${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed! ✓${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed! ✗${NC}"
    exit 1
fi