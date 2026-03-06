# Claude Code에서 알고리즘 에이전트 사용하기

## 🎉 이제 Claude Code에서 바로 사용 가능합니다!

MCP 서버를 통해 Claude Code 대화창에서 자연어로 에이전트를 호출할 수 있습니다.

---

## 📋 사용 가능한 도구 (총 6개)

| 도구 이름 | 기능 | 사용 예시 |
|----------|------|----------|
| `review_code` | 시니어 코드 리뷰 | "이 코드 리뷰해줘" |
| `analyze_problem` | 문제 분석 | "이 문제 방향성 알려줘" |
| `provide_hints` | 힌트 제공 | "힌트 좀 줘" |
| `analyze_complexity` | 복잡도 분석 | "시간복잡도 분석해줘" |
| **`trace_execution`** ⭐ | **실행 흐름 추적** | **"실행 흐름 추적해줘"** |
| **`create_trace_template`** ⭐ | **추적 템플릿** | **"추적 템플릿 만들어줘"** |

---

## 🚀 사용 방법

### 1. 코드 읽기 + 실행 흐름 추적

```
👤 "Sovled/Class2/stack.py 파일 읽어줘"

👤 "trace_execution 도구로 실행 흐름 추적해줘"
```

Claude가 자동으로 파일을 읽고 `trace_execution` 도구를 호출합니다.

**결과:**
- 📊 코드 구조 분석
- 📝 변수 흐름 추적 (라인별 생성/수정)
- 🔀 조건문 분기 분석 (if/elif/else)
- 🔄 반복문 iteration 설명
- 💡 학습 추천사항

### 2. 추적 템플릿 생성

```
👤 "create_trace_template 도구로 템플릿 만들어줘"
```

**결과:**
손으로 채울 수 있는 빈 테이블 생성
```
| Step | Line | n            | arr          | result       |
|------|------|--------------|--------------|--------------|
|   1  |      |              |              |              |
```

### 3. 전체 분석 워크플로우

```
👤 "Sovled/Class2/fizz_buzz.py 파일 분석해줘"

Claude: "파일을 읽어드렸습니다. 어떤 분석을 원하시나요?"

👤 "먼저 trace_execution으로 실행 흐름 추적하고,
    그 다음 analyze_complexity로 복잡도 분석해줘"

Claude: [두 도구를 순차적으로 실행]
```

---

## 💡 실전 활용 예시

### 절차적 사고력 훈련

```
👤 "이 코드의 for문이 어떻게 도는지 모르겠어"

👤 "trace_execution 도구로 반복문 분석해줘"

→ 각 iteration에서 변수가 어떻게 변하는지 상세 설명

👤 "create_trace_template으로 연습 템플릿도 만들어줘"

→ 손으로 직접 채워볼 수 있는 테이블 생성
```

### 조건문 분기 이해

```
👤 "if/elif/else 분기가 헷갈려"

👤 "trace_execution으로 조건문 분석해줘"

→ 각 조건의 True/False 케이스와 실행 블록 설명
```

### 디버깅

```
👤 "코드가 예상과 다르게 동작해"

👤 "trace_execution으로 변수 흐름 추적해줘"

→ 각 라인에서 변수가 생성/수정되는 지점 추적
```

---

## 🎯 도구 선택 가이드

### 언제 `trace_execution`을 사용할까?

✅ **이럴 때 사용:**
- for문을 돌 때 변수 값이 어떻게 변하는지 모르겠을 때
- 조건문의 분기가 헷갈릴 때
- 절차적 실행 순서가 머릿속에 안 그려질 때
- 변수가 어디서 생성/수정되는지 추적하고 싶을 때

❌ **이럴 때는 다른 도구:**
- 시간복잡도가 궁금하다 → `analyze_complexity`
- 코드 최적화가 필요하다 → `review_code`
- 문제 방향성을 모르겠다 → `analyze_problem`

### 언제 `create_trace_template`을 사용할까?

✅ **이럴 때 사용:**
- 손으로 직접 코드를 따라가며 연습하고 싶을 때
- 능동적 학습을 위한 템플릿이 필요할 때
- 반복문/조건문 흐름을 종이에 정리하고 싶을 때

---

## 🔧 MCP 서버 관리

### 서버 상태 확인

```bash
# MCP 서버 목록 확인
/mcp
```

### 서버 재시작이 필요한 경우

1. Claude Code 종료
2. Claude Code 다시 시작
3. `/mcp` 명령으로 확인

### 서버 위치

```
/Users/hanjeonghee/PycharmProjects/algorithm/mcp_server/algorithm_agent_server.py
```

---

## 📚 자세한 내용

- **CLI 사용법**: `agents/USAGE_GUIDE.md`
- **MCP 서버 상세**: `mcp_server/README.md`
- **에이전트 코드**: `agents/execution_tracer.py`

---

## 🎓 학습 팁

### 매일 루틴

1. **아침**: 어제 푼 문제 다시 보기
   ```
   "이 코드 trace_execution으로 분석해줘"
   ```

2. **오후**: 새 문제 풀기
   ```
   "문제 방향성 analyze_problem으로 알려줘"
   → 코드 작성
   "trace_execution으로 흐름 확인해줘"
   "analyze_complexity로 복잡도 체크해줘"
   ```

3. **저녁**: 복습
   ```
   "create_trace_template으로 템플릿 만들어줘"
   → 손으로 직접 채우며 복습
   ```

### 레벨별 활용

#### 초급 (절차적 흐름 이해 필요)
- `trace_execution` 매일 사용
- `create_trace_template`으로 연습
- 손으로 첫 3번 iteration 직접 쓰기

#### 중급 (최적화 필요)
- `trace_execution`으로 병목 지점 파악
- `analyze_complexity`로 복잡도 확인
- `review_code`로 개선점 찾기

#### 고급 (시니어 레벨 목표)
- `review_code` 중심
- `analyze_complexity`로 정확한 복잡도 계산
- `trace_execution`은 필요시만 사용

---

## 🤝 도움말

문제가 생기면:

1. `/mcp` 명령으로 서버 상태 확인
2. Claude Code 재시작
3. 에러 메시지를 Claude에게 보여주기

---

**🚀 이제 Claude Code에서 바로 "trace_execution 도구로 분석해줘"라고 말하면 됩니다!**
