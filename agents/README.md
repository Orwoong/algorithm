# Algorithm Problem Solving Agents

시니어 개발자를 위한 백준 알고리즘 문제 풀이 전문 에이전트 시스템

## 📋 개요

이 프로젝트는 알고리즘 문제 풀이 과정에서 **성장**에 초점을 맞춘 3가지 전문 에이전트를 제공합니다:

1. **Senior Code Reviewer** - 시니어 레벨 코드 리뷰
2. **Problem Analyzer** - 최소 힌트 문제 분석
3. **Time Complexity Analyzer** - 수학적 복잡도 분석

## 🎯 에이전트 상세

### 1. Senior Code Reviewer (`code_reviewer.py`)

**목적**: 시니어 개발자를 위한 엄격하고 정확한 코드 리뷰

**특징**:
- 성능 최적화 (메모리, 처리 속도)에 집중
- 더 효율적인 자료구조 제안
- 시니어 레벨에 맞지 않는 패턴 지적
- 직접적이고 명확한 피드백

**분석 항목**:
- 🔥 성능 이슈 (입력 처리, 정렬, 리스트 연산)
- 📊 자료구조 최적화 (list → set, Counter, deque 등)
- ⚠️ 시니어 레벨 체크 (매직 넘버, 변수명, 예외처리)
- 💡 추가 최적화 기회

**예제**:
```python
from agents import SeniorCodeReviewer

reviewer = SeniorCodeReviewer()
review = reviewer.review(your_code)
print(reviewer.format_review(review))
```

### 2. Problem Analyzer (`problem_analyzer.py`)

**목적**: 방향성 제시 + 필요시에만 힌트 제공

**원칙**:
- **기본 모드**: 방향성만 제시 (알고리즘/자료구조 종류)
- **명시적 요청시**: 구체적 힌트 + 반례 제공

**분석 항목**:
- 📍 방향성 (시간복잡도 기반 알고리즘 선택)
- 🧮 제안 알고리즘 (DP, Greedy, Graph, etc.)
- 📦 제안 자료구조 (적절한 자료구조)
- ⚠️ 현재 접근의 문제점 (코드가 있을 때)
- 💡 힌트 (명시적 요청시만)
- 🧪 반례 (명시적 요청시만)

**예제**:
```python
from agents import ProblemAnalyzer

analyzer = ProblemAnalyzer()

# 방향성만
result = analyzer.analyze(problem_text=problem, code=None, explicit_hint_request=False)

# 힌트 + 반례
result = analyzer.analyze(problem_text=problem, code=your_code, explicit_hint_request=True)

print(analyzer.format_analysis(result, explicit_hint=True))
```

### 3. Time Complexity Analyzer (`complexity_analyzer.py`)

**목적**: 상세한 시간/공간 복잡도 분석 + 수학적 설명

**분석 항목**:
- ⏱️ 시간 복잡도 (Big-O 표기법)
- 💾 공간 복잡도
- 📝 라인별 복잡도 분석
- 📐 수학적 설명 (Big-O 정의, 증명)
- 🔢 실제 연산 횟수 추정 (n값 제공시)
- ⚠️ 최적화 가능 여부

**수학적 개념**:
- Big-O 정의 및 증명
- 각 복잡도별 수학적 근거
- 성장률 비교 및 실제 연산 횟수

**예제**:
```python
from agents import ComplexityAnalyzer

analyzer = ComplexityAnalyzer()
result = analyzer.analyze(your_code, n_value=100000)
print(analyzer.format_analysis(result))
```

## 🚀 사용법

### 통합 인터페이스 사용

```bash
# 코드 리뷰
python agents/main.py review Sovled/Class2/stack.py

# 문제 분석 (방향성만)
python agents/main.py analyze "N개의 수를 정렬하시오"

# 힌트 제공 (반례 포함)
python agents/main.py hint Sovled/Class2/fizz_buzz.py

# 복잡도 분석
python agents/main.py complexity Sovled/Class2/prime_number.py 100000

# 모든 분석 실행
python agents/main.py all Sovled/Class2/stack_progression.py
```

### 개별 에이전트 사용

```python
# 1. 코드 리뷰
from agents import SeniorCodeReviewer

reviewer = SeniorCodeReviewer()
with open('your_code.py', 'r') as f:
    code = f.read()

review = reviewer.review(code)
print(reviewer.format_review(review))
```

```python
# 2. 문제 분석
from agents import ProblemAnalyzer

analyzer = ProblemAnalyzer()

# 방향성만 제시
result = analyzer.analyze(
    problem_text="N개의 수를 정렬",
    code=None,
    explicit_hint_request=False
)
print(analyzer.format_analysis(result, explicit_hint=False))

# 상세 힌트 + 반례
with open('your_code.py', 'r') as f:
    code = f.read()

result = analyzer.analyze(
    problem_text="N개의 수를 정렬",
    code=code,
    explicit_hint_request=True  # 명시적 요청
)
print(analyzer.format_analysis(result, explicit_hint=True))
```

```python
# 3. 복잡도 분석
from agents import ComplexityAnalyzer

analyzer = ComplexityAnalyzer()
with open('your_code.py', 'r') as f:
    code = f.read()

result = analyzer.analyze(code, n_value=100000)
print(analyzer.format_analysis(result))
```

## 📊 출력 예시

### Code Review 출력
```
================================================================================
📋 SENIOR CODE REVIEW REPORT
================================================================================

종합 평가: 🔴 여러 최적화 기회가 있습니다. 시니어 레벨이라면 반드시 개선이 필요합니다.

🔥 성능 이슈 (Performance Issues)
--------------------------------------------------------------------------------

[1] 입력 처리 비효율 [HIGH]
    상세: input() 대신 sys.stdin.readline() 사용 필요
    이유: 다중 입력시 약 2-3배 성능 차이
    해결: import sys; input = sys.stdin.readline

📊 자료구조 최적화 제안 (Data Structure Optimization)
--------------------------------------------------------------------------------

[1] list → set or dict
    이유: in 연산: list O(n) vs set O(1)
    영향: 대용량 데이터시 수백배 차이
    예시: allowed = set([1, 2, 3])  # list 대신 set
...
```

### Problem Analysis 출력
```
================================================================================
🎯 PROBLEM ANALYSIS
================================================================================

📍 방향성 (Direction)
--------------------------------------------------------------------------------
N이 10^5 수준 → O(n log n) 이하 알고리즘 필요 | 정렬 기반 접근 고려

🧮 제안 알고리즘 (Suggested Algorithms)
--------------------------------------------------------------------------------
Sort, Search

📦 제안 자료구조 (Suggested Data Structures)
--------------------------------------------------------------------------------
  • Hash (set/dict/Counter)
    이유: O(1) 검색/카운팅
    힌트: collections.Counter 고려
...
```

### Complexity Analysis 출력
```
================================================================================
⏱️ TIME & SPACE COMPLEXITY ANALYSIS
================================================================================

📊 종합 결과
--------------------------------------------------------------------------------
시간 복잡도: O(n^2)
공간 복잡도: O(n)
🔴 최적화 가능 - 개선 여지 있음

📐 시간복잡도 수학적 분석

Big-O 표기법: 입력 크기 n이 충분히 클 때, 알고리즘의 최악 수행시간
정의: T(n) = O(f(n)) ⟺ ∃c, n₀ > 0, ∀n ≥ n₀: T(n) ≤ c·f(n)

O(n^2) - 이차 시간
  이중 중첩 루프
  ∑(i=1 to n) ∑(j=1 to n) 1 = n²
  버블/삽입/선택 정렬
  주의: n=10,000이면 100,000,000 연산 (1억)
...
```

## 💡 활용 팁

### 1. 문제 풀이 전
```bash
# 문제 분석으로 방향성 파악
python agents/main.py analyze "문제 설명"
```

### 2. 코드 작성 중 막혔을 때
```bash
# 힌트 + 반례 요청
python agents/main.py hint your_code.py
```

### 3. 코드 완성 후
```bash
# 전체 분석 (복잡도 + 리뷰 + 분석)
python agents/main.py all your_code.py
```

### 4. 시간초과 발생시
```bash
# 복잡도 분석으로 원인 파악
python agents/main.py complexity your_code.py 100000
```

## 🎓 학습 철학

이 에이전트들은 다음 원칙을 따릅니다:

1. **자율성 존중**: 답을 주지 않고 방향성만 제시
2. **시니어 레벨 기준**: 높은 기준으로 코드 품질 평가
3. **수학적 이해**: 복잡도의 수학적 근거 제공
4. **실용성**: 실제 백준 제출시 유용한 피드백

## 📝 요구사항

- Python 3.7+
- 외부 라이브러리 없음 (표준 라이브러리만 사용)

## 🔧 확장 가능성

각 에이전트는 독립적으로 동작하며, 필요에 따라:
- 새로운 분석 패턴 추가
- 문제 유형별 특화 분석
- 실제 백준 API 연동 (문제 자동 다운로드)
- 자동 테스트 케이스 생성

등으로 확장 가능합니다.

## 📄 라이선스

MIT License

---

**만든이**: 시니어 개발자를 위한 성장 도구
**버전**: 1.0.0
**마지막 업데이트**: 2026-02-02
