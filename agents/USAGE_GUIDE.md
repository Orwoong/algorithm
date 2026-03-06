# Algorithm Agents 사용 가이드

## 🎯 절차적 사고력 향상을 위한 실행 흐름 추적 에이전트

코드의 실행 흐름과 변수 값의 변화를 추적하여 절차적 사고력을 향상시키는 새로운 에이전트가 추가되었습니다!

---

## 📋 전체 에이전트 목록

| 명령어 | 기능 | 용도 |
|--------|------|------|
| `review` | 코드 리뷰 | 성능 최적화 중심 리뷰 |
| `analyze` | 문제 분석 | 문제 방향성 제시 |
| `hint` | 힌트 제공 | 반례 포함 힌트 |
| `complexity` | 복잡도 분석 | 시간/공간 복잡도 분석 |
| **`trace`** | **실행 흐름 추적** | **절차적 사고력 향상** ⭐ NEW |
| **`template`** | **추적 템플릿** | **손으로 직접 추적 연습** ⭐ NEW |
| `all` | 전체 분석 | 모든 분석 한 번에 |

---

## 🔍 새로운 기능: 실행 흐름 추적 (`trace`)

### 목적
- **조건문의 분기**를 명확히 이해
- **반복문의 각 iteration**에서 변수 값 변화 추적
- **절차적 순서**를 머릿속에 그릴 수 있도록 훈련

### 사용법

```bash
# 기본 사용
python3 agents/main.py trace <파일경로>

# 예시
python3 agents/main.py trace Sovled/Class2/stack.py
```

### 제공되는 분석

1. **코드 구조 분석**
   - 총 줄 수, 함수/반복문/조건문 개수
   - 중첩 루프 수, 최대 중첩 깊이

2. **변수 흐름 추적**
   - 각 변수가 어디서 생성되고 수정되는지 라인별 추적
   - 연산자와 표현식 표시

3. **조건문 분기 분석**
   - if/elif/else의 각 분기 조건 설명
   - 조건이 True/False일 때 어떤 블록이 실행되는지 명시
   - 조건 연산자 의미 설명 (>, <, ==, and, or 등)

4. **반복문 분석**
   - for/while 루프의 동작 방식 설명
   - iteration별 변수 변화 예시
   - 반복 범위 및 패턴 설명

5. **학습 추천사항**
   - 코드 복잡도에 따른 맞춤형 학습 팁
   - 절차적 사고력 향상을 위한 연습 방법

---

## 📝 추적 템플릿 생성 (`template`)

### 목적
손으로 직접 코드를 추적하며 **능동적 학습**을 할 수 있도록 빈 템플릿 제공

### 사용법

```bash
python3 agents/main.py template <파일경로>

# 예시
python3 agents/main.py template Sovled/Class2/fizz_buzz.py
```

### 출력 예시

```
| Step | Line | n            | arr          | result       |
|------|------|--------------|--------------|--------------|
|   1  |      |              |              |              |
|   2  |      |              |              |              |
|   3  |      |              |              |              |
...
```

### 사용 방법
1. 템플릿을 복사하여 노트에 작성
2. 코드를 한 줄씩 실행한다고 가정
3. 각 Step에서 변수 값 기록
4. 조건문은 True/False 여부 확인
5. 반복문은 각 iteration마다 새로운 행 추가

---

## 💡 절차적 사고력 향상 학습 방법

### 1. 변수 테이블 작성 습관화
```
코드 실행 전 종이에 테이블 그리기:
| step | i | j | arr | result |
```

### 2. 반복문 첫 3번 iteration 손으로 따라하기
```python
for i in range(5):
    result += i * 2

# 손으로 쓰기:
# i=0: result = 0 + 0*2 = 0
# i=1: result = 0 + 1*2 = 2
# i=2: result = 2 + 2*2 = 6
# → 패턴 파악!
```

### 3. 조건문 경계값 테스트
```python
if x > 5:
    ...

# 테스트: x=4 (False), x=5 (False), x=6 (True)
# 경계값인 5를 반드시 확인!
```

### 4. print() 디버깅
```python
for i in range(n):
    print(f"i={i}, arr={arr}, result={result}")  # 중간 값 출력
    # ...
```

---

## 🚀 실전 활용 예시

### 문제를 풀 때 워크플로우

1. **문제 이해** → `python3 agents/main.py analyze "문제설명"`
2. **코드 작성**
3. **실행 흐름 확인** → `python3 agents/main.py trace my_code.py`
4. **템플릿으로 연습** → `python3 agents/main.py template my_code.py`
5. **복잡도 체크** → `python3 agents/main.py complexity my_code.py`
6. **최적화** → `python3 agents/main.py review my_code.py`
7. **힌트 필요시** → `python3 agents/main.py hint my_code.py`

### 학습 단계별 추천

#### 초보자 (절차적 흐름 이해 부족)
1. 간단한 코드로 시작
2. `template` 명령으로 손으로 직접 추적
3. 첫 3번 iteration을 종이에 쓰기
4. `trace` 명령으로 답안 확인

#### 중급자 (조건문/반복문 헷갈림)
1. `trace` 명령으로 조건문 분기 확인
2. 각 조건의 True/False 케이스 표로 정리
3. 경계값(boundary value) 테스트
4. `hint` 명령으로 반례 확인

#### 고급자 (최적화 필요)
1. `complexity` 명령으로 시간/공간 복잡도 분석
2. `review` 명령으로 성능 개선 포인트 확인
3. `trace` 명령으로 병목 지점 파악

---

## 📊 모든 분석 한 번에 (`all`)

```bash
python3 agents/main.py all Sovled/Class2/stack.py
```

다음 순서로 분석 실행:
1. 복잡도 분석
2. 코드 리뷰
3. **실행 흐름 추적** (NEW!)
4. 문제 분석

---

## 🎓 연습 팁

### 매일 10분 루틴
1. 어제 푼 문제 다시 보기
2. `template` 명령으로 템플릿 생성
3. 손으로 변수 테이블 작성 (3분)
4. `trace` 명령으로 정답 확인 (2분)
5. 틀린 부분 복습 (5분)

### 어려운 문제 만났을 때
1. 먼저 스스로 생각 (15분)
2. `analyze` 명령으로 방향성만 확인
3. 다시 시도 (15분)
4. `trace` 명령으로 흐름 확인
5. 여전히 막히면 `hint` 명령 사용

---

## ⚠️ 주의사항

- `trace` 명령은 **정적 분석**을 수행합니다 (실제 실행 X)
- 복잡한 코드는 일부 분석이 제한될 수 있습니다
- 가장 좋은 학습은 **손으로 직접 추적**하는 것입니다!

---

## 🤝 도움이 필요하면

```bash
python3 agents/main.py help
```

---

**🚀 매일 조금씩 연습하면 절차적 사고력이 자동으로 향상됩니다!**
