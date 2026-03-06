"""
Problem Analyzer Agent
문제 분석 및 최소 힌트 제공 에이전트

목적:
- 적절한 자료구조/알고리즘 방향성 제시
- 최소한의 힌트 제공 (방향성만)
- 명시적 요청시 반례 및 문제점 지적
"""

import re
from typing import Dict, List, Optional, Tuple


class ProblemAnalyzer:
    """문제 분석 및 힌트 제공 에이전트 (최소 개입 원칙)"""

    def __init__(self):
        # 알고리즘 패턴 키워드
        self.algorithm_keywords = {
            'DP': ['최적', '최소', '최대', '경우의 수', '피보나치', 'LCS', 'LIS'],
            'Greedy': ['최적해', '매 순간', '선택', '정렬 후'],
            'Graph': ['경로', '최단거리', '연결', '사이클', 'BFS', 'DFS'],
            'Tree': ['부모', '자식', '레벨', '트리', '이진'],
            'Sort': ['정렬', '순서', '오름차순', '내림차순'],
            'Search': ['찾기', '탐색', '이분탐색', '존재'],
            'Math': ['소수', '약수', '최대공약수', 'GCD', '조합', '순열'],
            'String': ['문자열', '패턴', '매칭', '회문'],
            'Stack': ['괄호', '후위표기', '가장 가까운', '짝'],
            'Queue': ['순서대로', 'FIFO', '대기'],
            'Priority Queue': ['우선순위', 'K번째', '최솟값 유지'],
            'Hash': ['중복', '개수', '빈도', '존재 여부'],
        }

        # 자료구조 감지 패턴
        self.data_structure_patterns = {
            'list': r'\[\]|list\(\)',
            'set': r'set\(|\{.*\}',
            'dict': r'dict\(|\{.*:.*\}',
            'deque': r'deque\(',
            'heap': r'heapq|heappush|heappop',
            'Counter': r'Counter\(',
            'defaultdict': r'defaultdict\(',
        }

    def analyze(self, problem_text: str = None, code: str = None,
                explicit_hint_request: bool = False) -> Dict:
        """
        문제 분석 및 힌트 제공

        Args:
            problem_text: 문제 설명 텍스트
            code: 현재 작성한 코드 (없을 수도 있음)
            explicit_hint_request: 명시적으로 힌트를 요청했는지

        Returns:
            분석 결과 딕셔너리
        """
        result = {
            'direction': None,  # 방향성
            'suggested_algorithms': [],  # 제안 알고리즘
            'suggested_data_structures': [],  # 제안 자료구조
            'current_approach_issues': [],  # 현재 접근의 문제점 (코드 있을 때)
            'counter_examples': [],  # 반례 (명시적 요청시)
            'hints': []  # 힌트 (명시적 요청시만)
        }

        # 문제 텍스트 분석 (방향성 제시)
        if problem_text:
            result['direction'] = self._suggest_direction(problem_text)
            result['suggested_algorithms'] = self._suggest_algorithms(problem_text)
            result['suggested_data_structures'] = self._suggest_data_structures_from_problem(problem_text)

        # 코드 분석 (있는 경우)
        if code:
            result['current_approach_issues'] = self._analyze_code_approach(code, problem_text)

        # 명시적 힌트 요청시에만 상세 정보 제공
        if explicit_hint_request:
            if code:
                result['hints'] = self._provide_hints(code, problem_text)
                result['counter_examples'] = self._generate_counter_examples(code, problem_text)
            else:
                result['hints'] = ['코드가 없습니다. 위의 방향성을 참고하여 먼저 구현해보세요.']

        return result

    def _suggest_direction(self, problem_text: str) -> str:
        """문제의 방향성만 제시"""
        direction_hints = []

        # 시간복잡도 힌트
        if '100000' in problem_text or '10^5' in problem_text:
            direction_hints.append("N이 10^5 수준 → O(n log n) 이하 알고리즘 필요")
        elif '1000' in problem_text or '10^3' in problem_text:
            direction_hints.append("N이 10^3 수준 → O(n^2) 허용 가능")

        # 문제 유형 힌트
        if any(word in problem_text for word in ['최소', '최대', '최적']):
            direction_hints.append("최적화 문제 → DP 또는 Greedy 고려")

        if any(word in problem_text for word in ['경로', '연결', '그래프']):
            direction_hints.append("그래프 탐색 문제 → BFS/DFS 방향")

        if any(word in problem_text for word in ['순서', '정렬']):
            direction_hints.append("정렬 기반 접근 고려")

        if any(word in problem_text for word in ['개수', '빈도', '중복']):
            direction_hints.append("카운팅/해시 자료구조 활용")

        return " | ".join(direction_hints) if direction_hints else "문제 조건을 다시 분석해보세요"

    def _suggest_algorithms(self, problem_text: str) -> List[str]:
        """적합한 알고리즘 제안 (방향성만)"""
        suggestions = []

        for algo, keywords in self.algorithm_keywords.items():
            if any(keyword in problem_text for keyword in keywords):
                suggestions.append(algo)

        # 중복 제거 및 우선순위
        return list(dict.fromkeys(suggestions))[:3]  # 최대 3개만

    def _suggest_data_structures_from_problem(self, problem_text: str) -> List[Dict]:
        """문제에서 필요한 자료구조 제안"""
        suggestions = []

        # 우선순위 큐
        if any(word in problem_text for word in ['우선순위', 'K번째', '최솟값', '최댓값']):
            suggestions.append({
                'structure': 'Priority Queue (heapq)',
                'reason': '우선순위 관리 필요',
                'hint': 'heappush, heappop 활용'
            })

        # 큐
        if any(word in problem_text for word in ['순서대로', '먼저', 'BFS']):
            suggestions.append({
                'structure': 'Queue (deque)',
                'reason': 'FIFO 순서 처리',
                'hint': 'collections.deque 사용'
            })

        # 스택
        if any(word in problem_text for word in ['괄호', '짝', '가장 가까운', '후입선출']):
            suggestions.append({
                'structure': 'Stack (list)',
                'reason': 'LIFO 또는 짝 매칭',
                'hint': 'append, pop 활용'
            })

        # 해시
        if any(word in problem_text for word in ['중복', '개수', '존재', '빈도']):
            suggestions.append({
                'structure': 'Hash (set/dict/Counter)',
                'reason': 'O(1) 검색/카운팅',
                'hint': 'collections.Counter 고려'
            })

        return suggestions[:2]  # 최대 2개만 제안

    def _analyze_code_approach(self, code: str, problem_text: str = None) -> List[Dict]:
        """현재 코드의 접근 방식 문제점 분석"""
        issues = []

        # 자료구조 잘못 사용
        if 'pop(0)' in code or 'del ' in code and '[0]' in code:
            issues.append({
                'issue': '잘못된 자료구조 사용',
                'detail': 'list를 queue처럼 사용 중 (O(n) pop)',
                'direction': 'collections.deque로 변경 필요'
            })

        # 비효율적인 탐색
        if re.search(r'for.*for.*if', code, re.DOTALL):
            # 중첩 루프에서 검색
            if 'in' in code:
                issues.append({
                    'issue': '비효율적 탐색',
                    'detail': '중첩 루프 + in 연산',
                    'direction': 'set/dict으로 O(1) 검색 구현'
                })

        # DFS/BFS 없이 그래프 문제 접근
        if problem_text and any(word in problem_text for word in ['경로', '연결', '방문']):
            if 'def dfs' not in code and 'def bfs' not in code and 'deque' not in code:
                issues.append({
                    'issue': '그래프 탐색 알고리즘 미사용',
                    'detail': '그래프 문제인데 DFS/BFS가 보이지 않음',
                    'direction': 'BFS 또는 DFS 구현 필요'
                })

        # DP 문제인데 DP 미사용
        if problem_text and any(word in problem_text for word in ['최적', '최소', '최대', '경우의 수']):
            if 'dp' not in code.lower() and 'memo' not in code.lower():
                issues.append({
                    'issue': 'DP 접근 필요',
                    'detail': '최적화 문제인데 DP 패턴이 보이지 않음',
                    'direction': 'dp 배열 또는 메모이제이션 고려'
                })

        return issues

    def _provide_hints(self, code: str, problem_text: str = None) -> List[str]:
        """명시적 요청시 힌트 제공 (문제점 지적)"""
        hints = []

        # 코드 분석
        lines = code.split('\n')

        # 무한루프 가능성
        if 'while True' in code and 'break' not in code:
            hints.append("⚠️ while True에 break 조건이 없어 무한루프 가능성")

        # 인덱스 에러 가능성
        if '[' in code and 'len(' in code:
            if 'range(len(' in code and '[i+1]' in code:
                hints.append("⚠️ i+1 인덱스 접근 - 범위 초과 가능성 체크")

        # 빈 리스트/딕셔너리 접근
        if any(op in code for op in ['.pop()', '[0]', '[-1]']):
            if 'if len(' not in code and 'if ' in code:
                hints.append("⚠️ 빈 컬렉션 접근 가능성 - 예외처리 필요")

        # 정렬 후 변경
        if '.sort()' in code or 'sorted(' in code:
            # 정렬 후 삽입/삭제
            sort_line = -1
            for i, line in enumerate(lines):
                if 'sort' in line:
                    sort_line = i
                    break

            if sort_line >= 0 and sort_line < len(lines) - 1:
                remaining = '\n'.join(lines[sort_line+1:])
                if 'append' in remaining or 'insert' in remaining:
                    hints.append("⚠️ 정렬 후 삽입/수정 - 정렬 순서 깨짐 주의")

        # 로직 힌트
        if not hints:
            hints.append("🔍 코드 구조는 괜찮아 보입니다. 예외 케이스를 점검해보세요.")

        return hints

    def _generate_counter_examples(self, code: str, problem_text: str = None) -> List[Dict]:
        """반례 생성 (명시적 요청시만)"""
        counter_examples = []

        # 엣지 케이스들
        edge_cases = [
            {
                'category': '경계값',
                'cases': [
                    {'input': 'N=1 (최소값)', 'expected': '?', 'your_output': '?'},
                    {'input': 'N=최대값', 'expected': '?', 'your_output': '?'},
                ]
            },
            {
                'category': '특수 케이스',
                'cases': [
                    {'input': '빈 입력', 'expected': '?', 'your_output': '?'},
                    {'input': '모든 값이 같은 경우', 'expected': '?', 'your_output': '?'},
                ]
            }
        ]

        # 코드 분석 기반 반례
        if 'if' in code:
            counter_examples.append({
                'type': '조건문 반례',
                'hint': '조건의 경계값과 반대 케이스를 테스트해보세요',
                'example': 'if x > 0 이면 → x=0, x=-1 케이스 확인'
            })

        if '.sort()' in code or 'sorted(' in code:
            counter_examples.append({
                'type': '정렬 반례',
                'hint': '이미 정렬된 경우, 역순 정렬, 중복값',
                'example': '[1,2,3], [3,2,1], [2,2,2]'
            })

        if 'deque' in code or 'queue' in code.lower():
            counter_examples.append({
                'type': '큐 반례',
                'hint': '큐가 비었을 때, 한 개만 있을 때',
                'example': 'popleft() 전 empty 체크'
            })

        # 일반적인 반례 템플릿
        counter_examples.append({
            'type': '일반 체크리스트',
            'cases': [
                '1. 최소 입력 (N=1, 빈 배열 등)',
                '2. 최대 입력 (시간초과 체크)',
                '3. 모든 값이 동일',
                '4. 정렬된 입력 vs 역순',
                '5. 음수, 0, 양수 혼합'
            ]
        })

        return counter_examples

    def format_analysis(self, result: Dict, explicit_hint: bool = False) -> str:
        """분석 결과 포맷팅"""
        output = []
        output.append("=" * 80)
        output.append("🎯 PROBLEM ANALYSIS")
        output.append("=" * 80)
        output.append("")

        # 방향성 (항상 표시)
        if result['direction']:
            output.append("📍 방향성 (Direction)")
            output.append("-" * 80)
            output.append(result['direction'])
            output.append("")

        # 제안 알고리즘
        if result['suggested_algorithms']:
            output.append("🧮 제안 알고리즘 (Suggested Algorithms)")
            output.append("-" * 80)
            output.append(", ".join(result['suggested_algorithms']))
            output.append("")

        # 제안 자료구조
        if result['suggested_data_structures']:
            output.append("📦 제안 자료구조 (Suggested Data Structures)")
            output.append("-" * 80)
            for ds in result['suggested_data_structures']:
                output.append(f"  • {ds['structure']}")
                output.append(f"    이유: {ds['reason']}")
                output.append(f"    힌트: {ds['hint']}")
            output.append("")

        # 현재 접근의 문제점 (코드가 있을 때)
        if result['current_approach_issues']:
            output.append("⚠️ 현재 접근의 문제점 (Current Approach Issues)")
            output.append("-" * 80)
            for issue in result['current_approach_issues']:
                output.append(f"  ❌ {issue['issue']}")
                output.append(f"     상세: {issue['detail']}")
                output.append(f"     방향: {issue['direction']}")
                output.append("")

        # 명시적 힌트 요청시에만 표시
        if explicit_hint:
            if result['hints']:
                output.append("💡 힌트 (Hints) - 명시적 요청")
                output.append("-" * 80)
                for hint in result['hints']:
                    output.append(f"  {hint}")
                output.append("")

            if result['counter_examples']:
                output.append("🧪 반례 체크 (Counter Examples) - 명시적 요청")
                output.append("-" * 80)
                for ce in result['counter_examples']:
                    if 'type' in ce:
                        output.append(f"  [{ce['type']}]")
                        if 'hint' in ce:
                            output.append(f"    힌트: {ce['hint']}")
                        if 'example' in ce:
                            output.append(f"    예시: {ce['example']}")
                        if 'cases' in ce:
                            for case in ce['cases']:
                                output.append(f"    {case}")
                        output.append("")

        output.append("=" * 80)
        output.append("💪 스스로 생각하고 해결하는 것이 최고의 학습입니다!")
        output.append("=" * 80)

        return "\n".join(output)


if __name__ == "__main__":
    # 테스트
    analyzer = ProblemAnalyzer()

    problem = """
    N개의 수가 주어졌을 때, 이를 오름차순으로 정렬하는 프로그램을 작성하시오.
    시간 제한: 1초, N ≤ 100,000
    """

    code = """
n = int(input())
arr = []
for i in range(n):
    arr.append(int(input()))

# 버블 정렬
for i in range(n):
    for j in range(n-1):
        if arr[j] > arr[j+1]:
            arr[j], arr[j+1] = arr[j+1], arr[j]

for num in arr:
    print(num)
    """

    # 일반 분석
    result = analyzer.analyze(problem_text=problem, code=code, explicit_hint_request=False)
    print(analyzer.format_analysis(result, explicit_hint=False))

    print("\n\n" + "="*80)
    print("명시적 힌트 요청시:")
    print("="*80 + "\n")

    # 명시적 힌트 요청
    result = analyzer.analyze(problem_text=problem, code=code, explicit_hint_request=True)
    print(analyzer.format_analysis(result, explicit_hint=True))
