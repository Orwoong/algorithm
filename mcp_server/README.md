# Algorithm Agent MCP Server

Claude Code에서 알고리즘 문제 풀이 에이전트를 `/명령어` 형태로 사용할 수 있게 해주는 MCP (Model Context Protocol) 서버입니다.

## 🎯 기능

이 MCP 서버는 6가지 도구를 제공합니다:

### 1. `review_code` - 시니어 코드 리뷰
- 성능 최적화 (메모리, 처리 속도)
- 자료구조 개선 제안
- 시니어 레벨 체크
- 코드 품질 분석

### 2. `analyze_problem` - 문제 분석
- 알고리즘 방향성 제시
- 적절한 자료구조 제안
- 최소 힌트 제공

### 3. `provide_hints` - 힌트 제공
- 명시적 요청시 상세 힌트
- 반례 제공
- 문제점 정확히 지적

### 4. `analyze_complexity` - 복잡도 분석
- 시간/공간 복잡도 상세 분석
- 수학적 설명 (Big-O 정의, 증명)
- 라인별 복잡도
- 연산 횟수 추정

### 5. `trace_execution` - 실행 흐름 추적 ⭐ NEW
- 변수 흐름 추적 (생성/수정 지점)
- 조건문 분기 분석 (if/elif/else 동작)
- 반복문 iteration 추적
- 절차적 사고력 향상

### 6. `create_trace_template` - 추적 템플릿 생성 ⭐ NEW
- 손으로 채울 수 있는 빈 테이블 생성
- 능동적 학습 지원
- 절차적 사고 훈련

## 📦 구조

```
mcp_server/
├── algorithm_agent_server.py  # MCP 서버 메인
├── pyproject.toml             # 프로젝트 설정
└── README.md                  # 이 파일

agents/                         # 에이전트 모듈 (서버가 사용)
├── code_reviewer.py
├── problem_analyzer.py
├── complexity_analyzer.py
├── execution_tracer.py        # ⭐ NEW
├── main.py                    # CLI 인터페이스
├── USAGE_GUIDE.md             # 사용 가이드
└── __init__.py
```

## 🚀 설치 방법

### 1. Claude Code 설정

`~/.config/claude/settings.json`에 추가:

```json
{
  "mcpServers": {
    "algorithm-agent": {
      "command": "python3",
      "args": [
        "/절대경로/PycharmProjects/algorithm/mcp_server/algorithm_agent_server.py"
      ],
      "description": "시니어 개발자를 위한 알고리즘 문제 풀이 에이전트"
    }
  }
}
```

### 2. Claude Code 재시작

```bash
# Claude Code 재시작
```

## 💻 사용 예시

### Claude Code에서 자연어로 요청

```
👤 "Sovled/Class2/stack.py 파일을 review_code 도구로 리뷰해줘"

👤 "이 코드의 시간복잡도를 analyze_complexity로 분석해줘"

👤 "힌트 좀 줘 - provide_hints 사용해서"

👤 "문제를 analyze_problem으로 분석해줘: N개의 수 정렬"

👤 "이 코드의 실행 흐름을 trace_execution으로 추적해줘"

👤 "create_trace_template으로 추적 템플릿 만들어줘"
```

Claude가 자동으로 적절한 도구를 호출합니다.

### 절차적 사고력 향상 워크플로우 예시

```
👤 "이 코드 읽어줘: Sovled/Class2/stack.py"

👤 "trace_execution 도구로 실행 흐름을 추적해줘"
→ 변수 흐름, 조건문 분기, 반복문 동작 분석

👤 "create_trace_template 도구로 템플릿도 만들어줘"
→ 손으로 채울 수 있는 빈 테이블 생성

👤 "이제 복잡도도 analyze_complexity로 확인해줘"
→ 시간/공간 복잡도 분석
```

## 🔧 MCP 프로토콜 상세

### 지원하는 메소드

1. **initialize**: 서버 초기화
2. **tools/list**: 사용 가능한 도구 목록
3. **tools/call**: 특정 도구 실행

### 통신 방식

- **입력**: stdin (JSON-RPC)
- **출력**: stdout (JSON)
- **프로토콜 버전**: 2024-11-05

## 🧪 테스트

### 수동 테스트

```bash
# 서버 실행
python3 algorithm_agent_server.py

# 요청 예시 (stdin으로 입력)
{"method": "tools/list", "params": {}}
```

### 도구 호출 테스트

```json
{
  "method": "tools/call",
  "params": {
    "name": "review_code",
    "arguments": {
      "code": "def solution():\n    pass"
    }
  }
}
```

## 📋 도구 스키마

### review_code

```json
{
  "name": "review_code",
  "inputSchema": {
    "type": "object",
    "properties": {
      "code": {"type": "string"},
      "file_path": {"type": "string"}
    },
    "required": ["code"]
  }
}
```

### analyze_problem

```json
{
  "name": "analyze_problem",
  "inputSchema": {
    "type": "object",
    "properties": {
      "problem_text": {"type": "string"},
      "code": {"type": "string"},
      "explicit_hint": {"type": "boolean", "default": false}
    },
    "required": ["problem_text"]
  }
}
```

### provide_hints

```json
{
  "name": "provide_hints",
  "inputSchema": {
    "type": "object",
    "properties": {
      "code": {"type": "string"},
      "problem_text": {"type": "string"}
    },
    "required": ["code"]
  }
}
```

### analyze_complexity

```json
{
  "name": "analyze_complexity",
  "inputSchema": {
    "type": "object",
    "properties": {
      "code": {"type": "string"},
      "n_value": {"type": "integer"}
    },
    "required": ["code"]
  }
}
```

### trace_execution ⭐ NEW

```json
{
  "name": "trace_execution",
  "inputSchema": {
    "type": "object",
    "properties": {
      "code": {"type": "string"},
      "test_input": {"type": "string"},
      "max_iterations": {"type": "integer", "default": 20}
    },
    "required": ["code"]
  }
}
```

### create_trace_template ⭐ NEW

```json
{
  "name": "create_trace_template",
  "inputSchema": {
    "type": "object",
    "properties": {
      "code": {"type": "string"}
    },
    "required": ["code"]
  }
}
```

## 🔍 디버깅

### 로그 확인

```bash
# Claude Code MCP 로그
tail -f ~/.config/claude/logs/mcp.log

# 서버 직접 실행하여 오류 확인
python3 algorithm_agent_server.py
```

### 일반적인 문제

1. **Python 경로 오류**
   - `which python3`로 정확한 경로 확인
   - settings.json의 `command` 수정

2. **모듈 import 오류**
   - agents 디렉토리가 있는지 확인
   - `sys.path.insert(0, ...)` 경로 확인

3. **권한 오류**
   - `chmod +x algorithm_agent_server.py`

## 📚 참고 자료

- [MCP 공식 문서](https://modelcontextprotocol.io/)
- [Claude Code MCP 가이드](https://docs.anthropic.com/claude/docs/mcp)

## 🆘 문제 해결

문제가 발생하면:
1. 서버 직접 실행하여 Python 오류 확인
2. Claude Code 로그 확인
3. settings.json 경로 재확인
4. Claude Code 재시작

---

**MCP 서버가 정상 작동하면 Claude Code에서 바로 사용 가능합니다!** 🎉
