# 🚀 Algorithm Agent for Claude Code

시니어 개발자를 위한 백준 알고리즘 문제 풀이 전문 에이전트 시스템

**Claude Code에서 바로 사용 가능한 통합 버전입니다!**

## ✨ 특징

Claude Code와 대화하면서 다음 기능을 **자연어**로 사용할 수 있습니다:

- 🔍 **시니어 코드 리뷰** - 성능 최적화, 자료구조 개선, 품질 체크
- 🎯 **문제 분석** - 알고리즘 방향성 제시 (힌트 최소화)
- 💡 **힌트 제공** - 명시적 요청시 반례 및 상세 힌트
- ⏱️ **복잡도 분석** - 시간/공간 복잡도 + 수학적 설명

## 🎬 빠른 시작

### 1️⃣ 자동 설정 (추천)

```bash
cd /Users/hanjeonghee/PycharmProjects/algorithm
./setup_claude_mcp.sh
```

### 2️⃣ Claude Code 재시작

```bash
# Claude Code 종료 후 재실행
```

### 3️⃣ 바로 사용!

Claude Code에서 다음과 같이 대화하세요:

```
👤 "Sovled/Class2/stack.py 파일을 review_code 도구로 리뷰해줘"

👤 "이 코드의 시간복잡도를 analyze_complexity로 분석해줘"
   [코드 붙여넣기]

👤 "N개의 수를 정렬하는 문제인데 analyze_problem으로 방향성 알려줘"

👤 "이 코드를 provide_hints로 힌트 달라"
   [코드 붙여넣기]
```

Claude가 자동으로 적절한 도구를 호출합니다!

## 📦 프로젝트 구조

```
algorithm/
├── agents/                          # 에이전트 모듈
│   ├── __init__.py
│   ├── code_reviewer.py            # 시니어 코드 리뷰어
│   ├── problem_analyzer.py         # 문제 분석가
│   ├── complexity_analyzer.py      # 복잡도 분석가
│   ├── main.py                     # 독립 실행용
│   └── README.md
│
├── mcp_server/                      # Claude Code 통합
│   ├── algorithm_agent_server.py   # MCP 서버
│   ├── pyproject.toml
│   └── README.md
│
├── Sovled/                          # 백준 문제 풀이
│   └── Class2/
│       ├── stack.py
│       ├── fizz_buzz.py
│       └── ...
│
├── setup_claude_mcp.sh             # 자동 설정 스크립트 ⭐
├── CLAUDE_SETUP.md                 # 상세 설정 가이드
├── claude_code_config.json         # 설정 템플릿
└── README.md                       # 이 파일
```

## 🎯 에이전트 기능 상세

### 1. 시니어 코드 리뷰 (`review_code`)

**목적**: 성장을 위한 엄격한 코드 리뷰

**분석 항목**:
- 🔥 성능 이슈 (input() vs readline, 정렬 중복, 비효율적 연산)
- 📊 자료구조 최적화 (list → set, Counter, deque 등)
- ⚠️ 시니어 레벨 체크 (매직 넘버, 변수명, 예외처리)
- 💡 추가 최적화 기회

**예시 출력**:
```
================================================================================
📋 SENIOR CODE REVIEW REPORT
================================================================================

종합 평가: 🔴 여러 최적화 기회가 있습니다. 시니어 레벨이라면 반드시 개선이 필요합니다.

🔥 성능 이슈
[1] 입력 처리 비효율 [HIGH]
    상세: input() 대신 sys.stdin.readline() 사용 필요
    이유: 다중 입력시 약 2-3배 성능 차이
    해결: import sys; input = sys.stdin.readline

📊 자료구조 최적화 제안
[1] list → set or dict
    이유: in 연산: list O(n) vs set O(1)
    영향: 대용량 데이터시 수백배 차이
    예시: allowed = set([1, 2, 3])
```

### 2. 문제 분석 (`analyze_problem`)

**목적**: 방향성만 제시 (스스로 생각하게)

**분석 항목**:
- 📍 방향성 (시간복잡도 기반 알고리즘 선택)
- 🧮 제안 알고리즘 (DP, Greedy, Graph 등)
- 📦 제안 자료구조
- ⚠️ 현재 접근의 문제점 (코드가 있을 때)

**예시 출력**:
```
================================================================================
🎯 PROBLEM ANALYSIS
================================================================================

📍 방향성
N이 10^5 수준 → O(n log n) 이하 알고리즘 필요 | 정렬 기반 접근 고려

🧮 제안 알고리즘
Sort, Search

📦 제안 자료구조
  • Hash (set/dict/Counter)
    이유: O(1) 검색/카운팅
    힌트: collections.Counter 고려
```

### 3. 힌트 제공 (`provide_hints`)

**목적**: 명시적 요청시에만 상세 힌트 + 반례

**제공 정보**:
- 💡 구체적 힌트 (문제점 지적)
- 🧪 반례 ("입력 X → 기대값 A, 실제 B")

**예시 출력**:
```
💡 힌트
  ⚠️ i+1 인덱스 접근 - 범위 초과 가능성 체크
  ⚠️ 빈 리스트 접근 가능성 - 예외처리 필요

🧪 반례 체크
  [조건문 반례]
    힌트: 조건의 경계값과 반대 케이스를 테스트해보세요
    예시: if x > 0 이면 → x=0, x=-1 케이스 확인

  [일반 체크리스트]
    1. 최소 입력 (N=1, 빈 배열 등)
    2. 최대 입력 (시간초과 체크)
    3. 모든 값이 동일
```

### 4. 복잡도 분석 (`analyze_complexity`)

**목적**: 상세한 수학적 복잡도 분석

**분석 항목**:
- ⏱️ 시간 복잡도 (Big-O)
- 💾 공간 복잡도
- 📝 라인별 복잡도
- 📐 수학적 설명 (Big-O 정의, 증명)
- 🔢 연산 횟수 추정

**예시 출력**:
```
================================================================================
⏱️ TIME & SPACE COMPLEXITY ANALYSIS
================================================================================

📊 종합 결과
시간 복잡도: O(n^2)
공간 복잡도: O(n)
🔴 최적화 가능 - 개선 여지 있음

📝 라인별 분석
L  8 | O(n)         | for i in range(n):
      → n번 반복 (연산: n)
L  9 | O(n)         | for j in range(n-1):
      → n-1번 반복 (연산: n-1)

📐 시간복잡도 수학적 분석

Big-O 표기법: 입력 크기 n이 충분히 클 때, 알고리즘의 최악 수행시간
정의: T(n) = O(f(n)) ⟺ ∃c, n₀ > 0, ∀n ≥ n₀: T(n) ≤ c·f(n)

O(n^2) - 이차 시간
  이중 중첩 루프
  ∑(i=1 to n) ∑(j=1 to n) 1 = n²
  주의: n=10,000이면 100,000,000 연산 (1억)

🔢 실제 연산 횟수 추정
입력 크기 n = 10,000
예상 연산 횟수: 100,000,000
예상 소요 시간: 1.0초
실행 가능 여부: ⚠️ 위험 (최적화 필요)
```

## 💻 사용 방법

### Claude Code에서 (추천)

```
# 코드 리뷰
"이 파일을 review_code로 리뷰해줘: Sovled/Class2/stack.py"

# 문제 분석
"N개의 수를 정렬하는 문제인데 N ≤ 100,000이야.
 analyze_problem으로 방향성 알려줘"

# 힌트 요청
"이 코드가 왜 틀렸는지 provide_hints로 반례 포함해서 알려줘"
[코드]

# 복잡도 분석
"이 코드를 n=100000으로 analyze_complexity 해줘"
[코드]
```

### 터미널에서 독립 실행

```bash
# 코드 리뷰
python3 agents/main.py review Sovled/Class2/stack.py

# 문제 분석
python3 agents/main.py analyze "N개의 수를 정렬하시오"

# 힌트 제공
python3 agents/main.py hint Sovled/Class2/fizz_buzz.py

# 복잡도 분석
python3 agents/main.py complexity Sovled/Class2/prime_number.py 100000

# 전체 분석
python3 agents/main.py all Sovled/Class2/stack_progression.py
```

## 🔧 설치 상세

### 자동 설정 스크립트

```bash
./setup_claude_mcp.sh
```

스크립트가 자동으로:
1. Python 경로 확인
2. Claude Code 설정 파일 업데이트
3. 실행 권한 설정

### 수동 설정

`~/.config/claude/settings.json`에 추가:

```json
{
  "mcpServers": {
    "algorithm-agent": {
      "command": "python3",
      "args": [
        "/Users/hanjeonghee/PycharmProjects/algorithm/mcp_server/algorithm_agent_server.py"
      ],
      "description": "시니어 개발자를 위한 알고리즘 문제 풀이 에이전트"
    }
  }
}
```

자세한 내용은 [CLAUDE_SETUP.md](CLAUDE_SETUP.md)를 참고하세요.

## 💡 추천 워크플로우

### 1. 문제 풀이 전
```
"이 문제를 analyze_problem으로 분석해줘:
 N개의 수를 정렬하는데 N ≤ 100,000"
```
→ 방향성 파악 (O(n log n) 알고리즘 필요)

### 2. 코드 작성 중 막혔을 때
```
"이 코드를 provide_hints로 힌트 줘"
[코드]
```
→ 반례 및 문제점 확인

### 3. 코드 완성 후
```
"이 코드를 review_code로 리뷰해줘"
[코드]
```
→ 성능 최적화 및 개선점 확인

### 4. 시간초과 발생시
```
"이 코드를 analyze_complexity로 분석해줘"
[코드]
```
→ 복잡도 확인 및 최적화 방향 파악

## 🔍 문제 해결

### MCP 서버가 연결되지 않는 경우

1. **서버 직접 테스트**:
   ```bash
   python3 mcp_server/algorithm_agent_server.py
   ```

2. **Python 경로 확인**:
   ```bash
   which python3
   ```
   설정 파일의 `command`를 실제 경로로 변경

3. **권한 확인**:
   ```bash
   chmod +x mcp_server/algorithm_agent_server.py
   ```

4. **Claude Code 재시작**

### 도구가 목록에 안 보이는 경우

- Claude Code 완전 종료 후 재시작
- `~/.config/claude/settings.json` 문법 확인
- 로그 확인: `~/.config/claude/logs/`

## 📚 문서

- [CLAUDE_SETUP.md](CLAUDE_SETUP.md) - Claude Code 설정 가이드
- [agents/README.md](agents/README.md) - 에이전트 모듈 상세
- [mcp_server/README.md](mcp_server/README.md) - MCP 서버 상세

## 🎓 학습 철학

이 에이전트들은 다음 원칙을 따릅니다:

1. **자율성 존중** - 답을 주지 않고 방향성만 제시
2. **시니어 레벨 기준** - 높은 기준으로 코드 품질 평가
3. **수학적 이해** - 복잡도의 수학적 근거 제공
4. **성장 중심** - 개선과 학습을 위한 피드백

## 📝 요구사항

- Python 3.9+
- Claude Code (최신 버전 권장)
- 외부 라이브러리 불필요 (표준 라이브러리만 사용)

## 🚀 향후 계획

- [ ] 더 많은 알고리즘 패턴 인식
- [ ] 백준 API 연동 (문제 자동 다운로드)
- [ ] 자동 테스트 케이스 생성
- [ ] 최적화 제안의 정확도 개선

## 📄 라이선스

MIT License

---

**만든이**: 시니어 개발자를 위한 성장 도구
**버전**: 1.0.0
**마지막 업데이트**: 2026-02-02

**Claude Code와 함께 알고리즘 실력을 향상시키세요!** 🚀
