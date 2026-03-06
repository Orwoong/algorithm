"""
Senior Code Reviewer Agent
시니어 개발자를 위한 코드 리뷰 에이전트

목적:
- 성능 최적화 (메모리, 처리 속도)에 집중
- 더 효율적인 자료구조 제안
- 시니어 레벨에 맞지 않는 패턴 지적
- 성장을 위한 직접적이고 정확한 피드백
"""

import ast
import re
from typing import Dict, List, Tuple


class SeniorCodeReviewer:
    """시니어 개발자를 위한 엄격한 코드 리뷰어"""

    def __init__(self):
        self.performance_patterns = {
            'list_append_in_loop': '루프 내 append 대신 리스트 컴프리헨션 고려',
            'unnecessary_list_conversion': '불필요한 리스트 변환',
            'inefficient_string_concat': '문자열 연결시 join() 사용 권장',
            'redundant_iteration': '중복 순회 제거 가능',
            'unoptimized_search': '검색 최적화 필요 (set/dict 사용)',
        }

    def review(self, code: str, problem_info: Dict = None) -> Dict:
        """
        코드 리뷰 수행

        Args:
            code: 리뷰할 Python 코드
            problem_info: 문제 정보 (시간제한, 메모리제한 등)

        Returns:
            리뷰 결과 딕셔너리
        """
        review_result = {
            'performance_issues': [],
            'data_structure_suggestions': [],
            'senior_level_concerns': [],
            'optimization_opportunities': [],
            'overall_assessment': ''
        }

        # 성능 이슈 분석
        review_result['performance_issues'] = self._analyze_performance(code)

        # 자료구조 최적화 제안
        review_result['data_structure_suggestions'] = self._suggest_data_structures(code)

        # 시니어 레벨 체크
        review_result['senior_level_concerns'] = self._check_senior_level(code)

        # 최적화 기회
        review_result['optimization_opportunities'] = self._find_optimizations(code)

        # 종합 평가
        review_result['overall_assessment'] = self._generate_assessment(review_result)

        return review_result

    def _analyze_performance(self, code: str) -> List[Dict]:
        """성능 이슈 분석"""
        issues = []

        # sys.stdin.readline() 미사용 체크
        if 'input()' in code and 'sys.stdin' not in code:
            issues.append({
                'severity': 'HIGH',
                'issue': '입력 처리 비효율',
                'detail': 'input() 대신 sys.stdin.readline() 사용 필요',
                'reason': '다중 입력시 약 2-3배 성능 차이',
                'fix': 'import sys; input = sys.stdin.readline'
            })

        # 불필요한 정렬 체크
        sort_count = code.count('.sort()') + code.count('sorted(')
        if sort_count > 1:
            issues.append({
                'severity': 'MEDIUM',
                'issue': '중복 정렬 감지',
                'detail': f'{sort_count}번의 정렬 발견',
                'reason': '정렬은 O(n log n) - 최소화 필요',
                'fix': '한 번의 정렬로 해결 가능한지 검토'
            })

        # 리스트 컴프리헨션 미사용
        if re.search(r'for .+ in .+:\s+\w+\.append\(', code):
            issues.append({
                'severity': 'LOW',
                'issue': '리스트 컴프리헨션 미사용',
                'detail': 'append()를 사용한 루프 발견',
                'reason': '리스트 컴프리헨션이 약 30% 빠름',
                'fix': '[expression for item in iterable] 패턴 사용'
            })

        return issues

    def _suggest_data_structures(self, code: str) -> List[Dict]:
        """자료구조 최적화 제안"""
        suggestions = []

        # in 연산자를 리스트에 사용
        if re.search(r'if .+ in \[', code) or re.search(r'if .+ in \w+\s*\n.*\w+\s*=\s*\[', code):
            suggestions.append({
                'current': 'list',
                'suggested': 'set or dict',
                'reason': 'in 연산: list O(n) vs set O(1)',
                'impact': '대용량 데이터시 수백배 차이',
                'example': 'allowed = set([1, 2, 3])  # list 대신 set'
            })

        # Counter 미사용
        if 'count(' in code and 'Counter' not in code:
            suggestions.append({
                'current': 'list.count() 반복',
                'suggested': 'collections.Counter',
                'reason': '여러 요소 카운팅시 O(n²) → O(n)',
                'impact': '중간~대용량 데이터에서 현저한 차이',
                'example': 'from collections import Counter; cnt = Counter(arr)'
            })

        # defaultdict 미사용
        if re.search(r'if .+ not in \w+:\s+\w+\[.+\]\s*=', code):
            suggestions.append({
                'current': 'if key not in dict 패턴',
                'suggested': 'collections.defaultdict',
                'reason': '코드 간결성 + 약간의 성능 향상',
                'impact': '가독성 개선, 버그 감소',
                'example': 'from collections import defaultdict; d = defaultdict(list)'
            })

        # deque 미사용 (큐 구현시)
        if re.search(r'\.pop\(0\)', code) or re.search(r'del \w+\[0\]', code):
            suggestions.append({
                'current': 'list.pop(0)',
                'suggested': 'collections.deque',
                'reason': 'list.pop(0)는 O(n), deque.popleft()는 O(1)',
                'impact': '**심각한 성능 저하 - 즉시 수정 필요**',
                'example': 'from collections import deque; q = deque()'
            })

        return suggestions

    def _check_senior_level(self, code: str) -> List[Dict]:
        """시니어 레벨에 맞지 않는 패턴 체크"""
        concerns = []

        # 불필요한 변수 할당
        if re.search(r'(\w+)\s*=\s*(\w+)\s*\n\s*return\s+\1', code):
            concerns.append({
                'level': 'JUNIOR',
                'pattern': '불필요한 중간 변수',
                'feedback': '직접 반환 가능한 값을 변수에 할당하는 패턴',
                'improvement': '간결성과 성능을 위해 직접 반환'
            })

        # 매직 넘버 사용
        if re.search(r'\b(100000|1000000|10\*\*9)\b', code) and 'INF' not in code and 'MAX' not in code:
            concerns.append({
                'level': 'JUNIOR',
                'pattern': '매직 넘버 사용',
                'feedback': '의미있는 상수명으로 정의 필요',
                'improvement': 'INF = 10**9  # 명확한 의도 표현'
            })

        # 단일 문자 변수명 (i, j 제외)
        single_vars = re.findall(r'\b([a-hk-z])\s*=', code)
        if len(single_vars) > 2:
            concerns.append({
                'level': 'JUNIOR',
                'pattern': '불명확한 변수명',
                'feedback': f'단일 문자 변수 과다 사용: {set(single_vars)}',
                'improvement': '의미있는 변수명 사용 (count, result, visited 등)'
            })

        # try-except 없는 형변환
        if ('int(' in code or 'float(' in code) and 'try:' not in code:
            # 단, input 처리는 예외
            if 'input' not in code:
                concerns.append({
                    'level': 'JUNIOR',
                    'pattern': '예외처리 없는 형변환',
                    'feedback': '잘못된 입력에 대한 방어 코드 부재',
                    'improvement': '프로덕션 레벨 코드는 예외 상황 고려'
                })

        return concerns

    def _find_optimizations(self, code: str) -> List[Dict]:
        """최적화 기회 발견"""
        optimizations = []

        # 반복 계산 발견
        if re.search(r'len\(\w+\)', code):
            len_count = len(re.findall(r'len\(\w+\)', code))
            if len_count > 3:
                optimizations.append({
                    'type': 'COMPUTATION',
                    'opportunity': 'len() 반복 호출',
                    'current_cost': f'O(1) × {len_count}회',
                    'optimization': '변수에 캐싱',
                    'benefit': '미미하지만 코드 품질 향상',
                    'example': 'n = len(arr)  # 한 번만 계산'
                })

        # 문자열 연결 최적화
        if '+' in code and 'str' in code.lower():
            optimizations.append({
                'type': 'STRING',
                'opportunity': '문자열 연결 최적화',
                'current_cost': 'O(n²) 가능성',
                'optimization': 'join() 또는 f-string 사용',
                'benefit': '대량 문자열 처리시 극적인 개선',
                'example': '"".join(str_list) 또는 f"{a}{b}{c}"'
            })

        # 조기 종료 가능성
        if 'break' not in code and 'for' in code:
            optimizations.append({
                'type': 'LOGIC',
                'opportunity': '조기 종료 미사용',
                'current_cost': '불필요한 전체 순회',
                'optimization': '조건 만족시 즉시 break',
                'benefit': '최악의 경우만 전체 순회',
                'example': 'if found: break  # 더 이상 찾지 않음'
            })

        return optimizations

    def _generate_assessment(self, review_result: Dict) -> str:
        """종합 평가 생성"""
        total_issues = (
            len(review_result['performance_issues']) +
            len(review_result['data_structure_suggestions']) +
            len(review_result['senior_level_concerns'])
        )

        if total_issues == 0:
            return "✅ 시니어 레벨에 적합한 코드입니다. 최적화도 잘 되어 있습니다."
        elif total_issues <= 3:
            return "⚠️ 전반적으로 양호하나 몇 가지 개선 포인트가 있습니다."
        elif total_issues <= 6:
            return "🔴 여러 최적화 기회가 있습니다. 시니어 레벨이라면 반드시 개선이 필요합니다."
        else:
            return "🚨 심각한 성능/품질 이슈 다수. 즉시 리팩토링이 필요합니다."

    def format_review(self, review_result: Dict) -> str:
        """리뷰 결과를 읽기 쉬운 형태로 포맷팅"""
        output = []
        output.append("=" * 80)
        output.append("📋 SENIOR CODE REVIEW REPORT")
        output.append("=" * 80)
        output.append("")

        # 종합 평가
        output.append(f"종합 평가: {review_result['overall_assessment']}")
        output.append("")

        # 성능 이슈
        if review_result['performance_issues']:
            output.append("🔥 성능 이슈 (Performance Issues)")
            output.append("-" * 80)
            for idx, issue in enumerate(review_result['performance_issues'], 1):
                output.append(f"\n[{idx}] {issue['issue']} [{issue['severity']}]")
                output.append(f"    상세: {issue['detail']}")
                output.append(f"    이유: {issue['reason']}")
                output.append(f"    해결: {issue['fix']}")
            output.append("")

        # 자료구조 제안
        if review_result['data_structure_suggestions']:
            output.append("📊 자료구조 최적화 제안 (Data Structure Optimization)")
            output.append("-" * 80)
            for idx, sug in enumerate(review_result['data_structure_suggestions'], 1):
                output.append(f"\n[{idx}] {sug['current']} → {sug['suggested']}")
                output.append(f"    이유: {sug['reason']}")
                output.append(f"    영향: {sug['impact']}")
                output.append(f"    예시: {sug['example']}")
            output.append("")

        # 시니어 레벨 이슈
        if review_result['senior_level_concerns']:
            output.append("⚠️ 시니어 레벨 체크 (Senior Level Concerns)")
            output.append("-" * 80)
            for idx, concern in enumerate(review_result['senior_level_concerns'], 1):
                output.append(f"\n[{idx}] {concern['pattern']} [{concern['level']} 패턴]")
                output.append(f"    피드백: {concern['feedback']}")
                output.append(f"    개선: {concern['improvement']}")
            output.append("")

        # 최적화 기회
        if review_result['optimization_opportunities']:
            output.append("💡 추가 최적화 기회 (Optimization Opportunities)")
            output.append("-" * 80)
            for idx, opt in enumerate(review_result['optimization_opportunities'], 1):
                output.append(f"\n[{idx}] {opt['opportunity']} [{opt['type']}]")
                output.append(f"    현재: {opt['current_cost']}")
                output.append(f"    최적화: {opt['optimization']}")
                output.append(f"    효과: {opt['benefit']}")
                output.append(f"    예시: {opt['example']}")
            output.append("")

        output.append("=" * 80)
        output.append("💪 성장을 위한 피드백입니다. 끊임없이 개선하세요!")
        output.append("=" * 80)

        return "\n".join(output)


if __name__ == "__main__":
    # 테스트 코드
    reviewer = SeniorCodeReviewer()

    sample_code = """
n = int(input())
arr = []
for i in range(n):
    arr.append(int(input()))

result = 0
for i in range(len(arr)):
    if arr[i] in [1, 2, 3]:
        result += arr[i]
print(result)
    """

    review = reviewer.review(sample_code)
    print(reviewer.format_review(review))
