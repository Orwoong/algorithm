# Claude Code 스킬 설정 가이드

## 🎯 개요

이 가이드는 알고리즘 에이전트를 Claude Code에 통합하여 `/review-algo`, `/hint-algo` 같은 명령어로 사용하는 방법을 설명합니다.

## 📦 설치 방법

### 1단계: Claude Code 설정 파일 위치 확인

Claude Code 설정 파일은 다음 위치에 있습니다:

**macOS/Linux:**
```bash
~/.config/claude/settings.json
```

**Windows:**
```
%APPDATA%\Claude\settings.json
```

### 2단계: MCP 서버 설정 추가

Claude Code 설정 파일(`~/.config/claude/settings.json`)을 열어서 `mcpServers` 섹션에 다음을 추가합니다:

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

**⚠️ 중요**: 경로를 본인의 프로젝트 경로로 수정하세요!

### 3단계: Claude Code 재시작

설정을 저장한 후 Claude Code를 재시작합니다.

```bash
# Claude Code 종료 후 재시작
claude code
```

## 🚀 사용 방법

### 방법 1: 도구 직접 호출

Claude와 대화하면서 다음과 같이 요청하세요:

```
"이 코드를 review_code 도구로 리뷰해줘"
[코드 붙여넣기]
```

```
"이 문제를 analyze_problem 도구로 분석해줘:
N개의 수를 정렬하는 문제"
```

```
"이 코드를 analyze_complexity 도구로 복잡도 분석해줘"
[코드 붙여넣기]
```

```
"이 코드를 provide_hints 도구로 힌트 달라"
[코드 붙여넣기]
```

### 방법 2: 자연어로 요청

Claude가 자동으로 적절한 도구를 선택합니다:

```
"Sovled/Class2/stack.py 파일을 시니어 레벨로 리뷰해줘"
```

```
"이 코드의 시간복잡도를 수학적으로 분석해줘"
```

```
"문제 풀이 힌트 좀 줘 (반례 포함)"
```

## 🔧 사용 가능한 도구

### 1. `review_code` - 코드 리뷰
**용도**: 시니어 레벨 코드 리뷰 (성능, 자료구조, 코드 품질)

**입력**:
- `code`: 리뷰할 Python 코드 (필수)
- `file_path`: 파일 경로 (선택)

**출력**:
- 🔥 성능 이슈
- 📊 자료구조 최적화 제안
- ⚠️ 시니어 레벨 체크
- 💡 추가 최적화 기회

### 2. `analyze_problem` - 문제 분석
**용도**: 방향성 제시 (최소 힌트)

**입력**:
- `problem_text`: 문제 설명 (필수)
- `code`: 현재 코드 (선택)
- `explicit_hint`: 힌트 요청 여부 (선택, 기본: false)

**출력**:
- 📍 방향성
- 🧮 제안 알고리즘
- 📦 제안 자료구조
- ⚠️ 현재 접근의 문제점

### 3. `provide_hints` - 힌트 제공
**용도**: 명시적으로 힌트 + 반례 요청

**입력**:
- `code`: 분석할 코드 (필수)
- `problem_text`: 문제 설명 (선택)

**출력**:
- 💡 구체적 힌트
- 🧪 반례 ("입력 X → 기대값 A, 실제 B")

### 4. `analyze_complexity` - 복잡도 분석
**용도**: 시간/공간 복잡도 상세 분석 + 수학적 설명

**입력**:
- `code`: 분석할 코드 (필수)
- `n_value`: 입력 크기 (선택)

**출력**:
- ⏱️ 시간 복잡도 (Big-O)
- 💾 공간 복잡도
- 📝 라인별 분석
- 📐 수학적 설명
- 🔢 연산 횟수 추정

## 💡 활용 예시

### 예시 1: 코드 리뷰
```
👤 "Sovled/Class2/stack.py를 review_code로 리뷰해줘"

🤖 [review_code 도구 호출]
================================================================================
📋 SENIOR CODE REVIEW REPORT
================================================================================
종합 평가: ✅ 시니어 레벨에 적합한 코드입니다...
```

### 예시 2: 문제 분석
```
👤 "N개의 수를 정렬하는 문제인데 N ≤ 100,000이야.
    analyze_problem으로 방향성 알려줘"

🤖 [analyze_problem 도구 호출]
================================================================================
🎯 PROBLEM ANALYSIS
================================================================================
📍 방향성: N이 10^5 수준 → O(n log n) 이하 알고리즘 필요 | 정렬 기반 접근
```

### 예시 3: 힌트 요청
```
👤 "이 코드가 왜 틀렸는지 provide_hints로 힌트 줘"
[코드]

🤖 [provide_hints 도구 호출]
💡 힌트:
  ⚠️ i+1 인덱스 접근 - 범위 초과 가능성 체크

🧪 반례:
  입력: [1]
  기대값: 1
  실제: IndexError
```

### 예시 4: 복잡도 분석
```
👤 "이 버블 정렬 코드를 n=10000으로 analyze_complexity 해줘"
[코드]

🤖 [analyze_complexity 도구 호출]
시간 복잡도: O(n^2)
예상 연산 횟수: 100,000,000 (1억)
예상 소요 시간: 1.0초
실행 가능 여부: ⚠️ 위험 (최적화 필요)
```

## 🔍 문제 해결

### MCP 서버가 연결되지 않는 경우

1. **Python 경로 확인**:
   ```bash
   which python3
   ```
   설정 파일의 `command`를 실제 python3 경로로 변경

2. **서버 파일 권한 확인**:
   ```bash
   chmod +x /Users/hanjeonghee/PycharmProjects/algorithm/mcp_server/algorithm_agent_server.py
   ```

3. **수동으로 서버 테스트**:
   ```bash
   python3 /Users/hanjeonghee/PycharmProjects/algorithm/mcp_server/algorithm_agent_server.py
   ```

### 도구가 목록에 안 보이는 경우

Claude Code 로그 확인:
```bash
tail -f ~/.config/claude/logs/mcp.log
```

## 📋 전체 설정 예시

`~/.config/claude/settings.json`:

```json
{
  "mcpServers": {
    "algorithm-agent": {
      "command": "python3",
      "args": [
        "/Users/hanjeonghee/PycharmProjects/algorithm/mcp_server/algorithm_agent_server.py"
      ],
      "description": "시니어 개발자를 위한 알고리즘 문제 풀이 에이전트",
      "disabled": false
    }
  },
  "theme": "dark",
  "fontSize": 14
}
```

## 🎓 팁

1. **파일 직접 분석**:
   ```
   "이 파일을 읽고 review_code로 리뷰해줘: Sovled/Class2/stack.py"
   ```
   Claude가 파일을 읽은 후 도구를 호출합니다.

2. **여러 도구 연속 사용**:
   ```
   "이 코드를 analyze_complexity와 review_code로 모두 분석해줘"
   ```

3. **컨텍스트 유지**:
   ```
   "위에서 리뷰한 코드를 이제 analyze_complexity로 분석해줘"
   ```

## 🆘 도움이 필요하면

1. MCP 서버 로그 확인: `~/.config/claude/logs/`
2. 서버 직접 실행하여 오류 확인
3. Claude Code 재시작

---

**설정 완료 후 Claude Code에서 바로 사용 가능합니다!** 🎉
