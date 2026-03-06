"""
Time Complexity Analyzer Agent
시간복잡도 상세 분석 에이전트

목적:
- 코드의 시간복잡도 상세 분석
- 각 구문별 복잡도 계산
- 수학적 개념 및 증명 포함
- 공간복잡도도 함께 분석
"""

import re
import ast
from typing import Dict, List, Tuple, Optional


class ComplexityAnalyzer:
    """시간/공간 복잡도 상세 분석 에이전트"""

    def __init__(self):
        self.complexity_order = {
            'O(1)': 1,
            'O(log n)': 2,
            'O(n)': 3,
            'O(n log n)': 4,
            'O(n^2)': 5,
            'O(n^3)': 6,
            'O(2^n)': 7,
            'O(n!)': 8,
        }

    def analyze(self, code: str, n_value: int = None) -> Dict:
        """
        시간복잡도 상세 분석

        Args:
            code: 분석할 Python 코드
            n_value: 입력 크기 (있으면 실제 연산 횟수 추정)

        Returns:
            분석 결과 딕셔너리
        """
        result = {
            'time_complexity': None,  # 전체 시간복잡도
            'space_complexity': None,  # 전체 공간복잡도
            'line_by_line': [],  # 라인별 분석
            'mathematical_explanation': [],  # 수학적 설명
            'breakdown': {},  # 각 부분별 복잡도
            'total_operations': None,  # 예상 연산 횟수
            'optimization_possible': False,  # 최적화 가능 여부
        }

        # 라인별 분석
        result['line_by_line'] = self._analyze_line_by_line(code)

        # 전체 시간복잡도 계산
        result['time_complexity'], result['breakdown'] = self._calculate_total_complexity(code)

        # 공간복잡도 분석
        result['space_complexity'] = self._analyze_space_complexity(code)

        # 수학적 설명
        result['mathematical_explanation'] = self._generate_mathematical_explanation(
            result['time_complexity'], result['breakdown']
        )

        # 연산 횟수 추정
        if n_value:
            result['total_operations'] = self._estimate_operations(
                result['time_complexity'], n_value
            )

        # 최적화 가능 여부
        result['optimization_possible'] = self._check_optimization_possible(
            result['time_complexity'], code
        )

        return result

    def _analyze_line_by_line(self, code: str) -> List[Dict]:
        """라인별 시간복잡도 분석"""
        lines = code.split('\n')
        analysis = []

        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            complexity = self._analyze_single_line(line)
            if complexity:
                analysis.append({
                    'line_number': i,
                    'code': line,
                    'complexity': complexity['complexity'],
                    'explanation': complexity['explanation'],
                    'operations': complexity.get('operations', '?')
                })

        return analysis

    def _analyze_single_line(self, line: str) -> Optional[Dict]:
        """단일 라인 분석"""
        # for 루프
        if line.startswith('for ') and ' in range(' in line:
            match = re.search(r'range\(([^)]+)\)', line)
            if match:
                range_expr = match.group(1)
                if 'len(' in range_expr:
                    return {
                        'complexity': 'O(n)',
                        'explanation': 'n번 반복',
                        'operations': 'n'
                    }
                elif ',' in range_expr:
                    parts = range_expr.split(',')
                    if len(parts) == 2:
                        return {
                            'complexity': 'O(n)',
                            'explanation': f'{parts[0]}부터 {parts[1]}까지 반복',
                            'operations': f'{parts[1]} - {parts[0]}'
                        }
                else:
                    return {
                        'complexity': 'O(n)',
                        'explanation': f'{range_expr}번 반복',
                        'operations': range_expr
                    }

        # while 루프
        elif line.startswith('while '):
            return {
                'complexity': 'O(?)',
                'explanation': 'while 루프 - 종료 조건에 따라 다름',
                'operations': '분석 필요'
            }

        # 정렬
        elif '.sort()' in line or 'sorted(' in line:
            return {
                'complexity': 'O(n log n)',
                'explanation': 'Tim Sort 알고리즘 (평균/최악)',
                'operations': 'n log n'
            }

        # 리스트 메소드
        elif '.append(' in line:
            return {
                'complexity': 'O(1)',
                'explanation': 'amortized O(1) - 평균 상수시간',
                'operations': '1'
            }
        elif '.pop(0)' in line or '.pop()' not in line and '.pop(' in line:
            return {
                'complexity': 'O(n)',
                'explanation': '첫 원소 제거 후 전체 이동',
                'operations': 'n'
            }
        elif '.pop()' in line:
            return {
                'complexity': 'O(1)',
                'explanation': '마지막 원소 제거',
                'operations': '1'
            }
        elif '.insert(' in line:
            return {
                'complexity': 'O(n)',
                'explanation': '삽입 위치 이후 원소들 이동',
                'operations': 'n'
            }
        elif '.remove(' in line:
            return {
                'complexity': 'O(n)',
                'explanation': '검색 O(n) + 제거 O(n)',
                'operations': 'n'
            }

        # 문자열 연산
        elif '+' in line and ('str' in line or '"' in line or "'" in line):
            return {
                'complexity': 'O(n)',
                'explanation': '문자열 길이만큼 복사',
                'operations': '문자열 길이'
            }

        # in 연산자
        elif ' in ' in line:
            if '[' in line or 'list' in line:
                return {
                    'complexity': 'O(n)',
                    'explanation': 'list에서 선형 탐색',
                    'operations': 'n'
                }
            elif '{' in line or 'set' in line or 'dict' in line:
                return {
                    'complexity': 'O(1)',
                    'explanation': 'hash table 검색 (평균)',
                    'operations': '1'
                }

        # heapq
        elif 'heappush' in line or 'heappop' in line:
            return {
                'complexity': 'O(log n)',
                'explanation': 'heap 재정렬 (트리 높이)',
                'operations': 'log n'
            }

        # 기본 할당/연산
        elif '=' in line and 'for' not in line and 'while' not in line:
            return {
                'complexity': 'O(1)',
                'explanation': '단순 할당 또는 연산',
                'operations': '1'
            }

        return None

    def _calculate_total_complexity(self, code: str) -> Tuple[str, Dict]:
        """전체 시간복잡도 계산"""
        # 중첩 루프 깊이 계산
        max_depth = 0
        current_depth = 0
        has_sort = False
        has_log = False

        lines = code.split('\n')
        for line in lines:
            stripped = line.strip()

            # 들여쓰기로 깊이 계산
            indent = len(line) - len(line.lstrip())

            if 'for ' in stripped or 'while ' in stripped:
                current_depth += 1
                max_depth = max(max_depth, current_depth)

            if '.sort()' in stripped or 'sorted(' in stripped:
                has_sort = True

            if 'heappush' in stripped or 'heappop' in stripped:
                has_log = True

            # 블록 끝 감지 (간단한 방식)
            if stripped and not stripped.startswith('#'):
                if indent == 0 and current_depth > 0:
                    current_depth = 0

        # 복잡도 결정
        breakdown = {}

        if max_depth == 0:
            if has_sort:
                time_complexity = 'O(n log n)'
                breakdown['main'] = 'O(n log n) - 정렬'
            elif has_log:
                time_complexity = 'O(n log n)'
                breakdown['main'] = 'O(n log n) - heap 연산들'
            else:
                time_complexity = 'O(n)'
                breakdown['main'] = 'O(n) - 단순 순회'
        elif max_depth == 1:
            if has_sort:
                time_complexity = 'O(n^2 log n)'
                breakdown['loop'] = 'O(n)'
                breakdown['sort'] = 'O(n log n)'
                breakdown['total'] = 'O(n) × O(n log n) = O(n^2 log n)'
            else:
                time_complexity = 'O(n)'
                breakdown['loop'] = 'O(n) - 단일 루프'
        elif max_depth == 2:
            time_complexity = 'O(n^2)'
            breakdown['outer_loop'] = 'O(n)'
            breakdown['inner_loop'] = 'O(n)'
            breakdown['total'] = 'O(n) × O(n) = O(n^2)'
        elif max_depth == 3:
            time_complexity = 'O(n^3)'
            breakdown['triple_nested'] = 'O(n) × O(n) × O(n) = O(n^3)'
        else:
            time_complexity = f'O(n^{max_depth})'
            breakdown['nested'] = f'{max_depth}중 중첩 루프'

        # 재귀 감지
        if 'def ' in code:
            func_names = re.findall(r'def (\w+)\(', code)
            for func in func_names:
                # 함수 내에서 자기 자신 호출
                if func in code.split(f'def {func}')[1] if len(code.split(f'def {func}')) > 1 else '':
                    breakdown['recursion'] = '재귀 호출 감지 - 추가 분석 필요'

        return time_complexity, breakdown

    def _analyze_space_complexity(self, code: str) -> Dict:
        """공간복잡도 분석"""
        space_analysis = {
            'complexity': 'O(1)',
            'components': [],
            'total': 'O(1)'
        }

        max_space = 1  # O(1)

        # 배열/리스트 생성
        if re.search(r'\[\]\s*$|\w+\s*=\s*\[', code, re.MULTILINE):
            space_analysis['components'].append({
                'type': 'list/array',
                'complexity': 'O(n)',
                'explanation': 'n개 원소 저장'
            })
            max_space = max(max_space, 3)  # O(n)

        # 딕셔너리/set
        if 'dict(' in code or '{' in code and ':' in code:
            space_analysis['components'].append({
                'type': 'dictionary',
                'complexity': 'O(n)',
                'explanation': '최대 n개 키-값 쌍'
            })
            max_space = max(max_space, 3)

        if 'set(' in code or '{' in code and ':' not in code:
            space_analysis['components'].append({
                'type': 'set',
                'complexity': 'O(n)',
                'explanation': '최대 n개 원소'
            })
            max_space = max(max_space, 3)

        # 2차원 배열
        if '[[' in code or re.search(r'\[\s*\[\s*\]', code):
            space_analysis['components'].append({
                'type': '2D array',
                'complexity': 'O(n^2)',
                'explanation': 'n×n 또는 n×m 배열'
            })
            max_space = max(max_space, 5)  # O(n^2)

        # 재귀 스택
        func_names = re.findall(r'def (\w+)\(', code)
        for func in func_names:
            func_body = code.split(f'def {func}')[1] if len(code.split(f'def {func}')) > 1 else ''
            if func in func_body:
                space_analysis['components'].append({
                    'type': 'recursion stack',
                    'complexity': 'O(n) or O(log n)',
                    'explanation': '재귀 깊이만큼 스택 사용'
                })
                max_space = max(max_space, 3)

        # 최종 공간복잡도
        if max_space == 1:
            space_analysis['total'] = 'O(1)'
        elif max_space == 2:
            space_analysis['total'] = 'O(log n)'
        elif max_space == 3:
            space_analysis['total'] = 'O(n)'
        elif max_space == 4:
            space_analysis['total'] = 'O(n log n)'
        elif max_space == 5:
            space_analysis['total'] = 'O(n^2)'

        space_analysis['complexity'] = space_analysis['total']

        return space_analysis

    def _generate_mathematical_explanation(self, complexity: str, breakdown: Dict) -> List[str]:
        """수학적 설명 생성"""
        explanations = []

        # 기본 정의
        explanations.append("📐 시간복잡도 수학적 분석")
        explanations.append("")
        explanations.append("Big-O 표기법: 입력 크기 n이 충분히 클 때, 알고리즘의 최악 수행시간")
        explanations.append("정의: T(n) = O(f(n)) ⟺ ∃c, n₀ > 0, ∀n ≥ n₀: T(n) ≤ c·f(n)")
        explanations.append("")

        # 복잡도별 설명
        if complexity == 'O(1)':
            explanations.append("O(1) - 상수 시간")
            explanations.append("  입력 크기와 무관하게 일정한 시간")
            explanations.append("  예: 배열 인덱스 접근, 변수 할당")
            explanations.append("  T(n) = c (상수)")

        elif complexity == 'O(log n)':
            explanations.append("O(log n) - 로그 시간")
            explanations.append("  이진 탐색, 균형 트리 탐색")
            explanations.append("  매 단계 절반으로 감소: n → n/2 → n/4 → ... → 1")
            explanations.append("  단계 수 k: n/2^k = 1 ⟹ k = log₂n")
            explanations.append("  매우 효율적: n=1,000,000일 때 약 20단계")

        elif complexity == 'O(n)':
            explanations.append("O(n) - 선형 시간")
            explanations.append("  전체 데이터를 한 번 순회")
            explanations.append("  예: 배열 전체 탐색, 리스트 순회")
            explanations.append("  T(n) = c₁·n + c₂ = O(n)")

        elif complexity == 'O(n log n)':
            explanations.append("O(n log n) - 선형로그 시간")
            explanations.append("  효율적인 정렬 알고리즘 (Quick, Merge, Heap Sort)")
            explanations.append("  분할정복: n개를 log n 깊이로 분할")
            explanations.append("  각 레벨에서 O(n) 작업, 총 log n 레벨")
            explanations.append("  T(n) = n·log n")
            explanations.append("  예: n=1,000일 때 약 10,000 연산")

        elif complexity == 'O(n^2)':
            explanations.append("O(n^2) - 이차 시간")
            explanations.append("  이중 중첩 루프")
            explanations.append("  ∑(i=1 to n) ∑(j=1 to n) 1 = n²")
            explanations.append("  버블/삽입/선택 정렬")
            explanations.append("  주의: n=10,000이면 100,000,000 연산 (1억)")

        elif complexity == 'O(n^3)':
            explanations.append("O(n^3) - 삼차 시간")
            explanations.append("  삼중 중첩 루프")
            explanations.append("  행렬 곱셈, 플로이드-워셜 알고리즘")
            explanations.append("  n=1,000이면 10억 연산 - 매우 느림")

        elif complexity == 'O(2^n)':
            explanations.append("O(2^n) - 지수 시간")
            explanations.append("  모든 부분집합 탐색, 피보나치 naive 재귀")
            explanations.append("  T(n) = 2·T(n-1) = 2^n")
            explanations.append("  극도로 느림: n=30이면 10억 연산")
            explanations.append("  n=40이면 1조 연산 (불가능)")

        # 상세 분석
        if breakdown:
            explanations.append("")
            explanations.append("🔍 상세 분석")
            for key, value in breakdown.items():
                explanations.append(f"  {key}: {value}")

        # 성장률 비교
        explanations.append("")
        explanations.append("📊 성장률 비교 (n = 1,000일 때)")
        explanations.append("  O(1)      : 1 연산")
        explanations.append("  O(log n)  : ~10 연산")
        explanations.append("  O(n)      : 1,000 연산")
        explanations.append("  O(n log n): ~10,000 연산")
        explanations.append("  O(n^2)    : 1,000,000 연산 (100만)")
        explanations.append("  O(n^3)    : 1,000,000,000 연산 (10억)")
        explanations.append("  O(2^n)    : 불가능 (2^1000)")

        return explanations

    def _estimate_operations(self, complexity: str, n: int) -> Dict:
        """실제 연산 횟수 추정"""
        import math

        operations = {
            'n_value': n,
            'estimated_operations': 0,
            'time_estimate_seconds': 0,
            'feasible': True
        }

        # 연산 횟수 계산
        if complexity == 'O(1)':
            ops = 1
        elif complexity == 'O(log n)':
            ops = math.log2(n) if n > 0 else 0
        elif complexity == 'O(n)':
            ops = n
        elif complexity == 'O(n log n)':
            ops = n * math.log2(n) if n > 0 else 0
        elif complexity == 'O(n^2)':
            ops = n * n
        elif complexity == 'O(n^3)':
            ops = n * n * n
        elif 'O(n^' in complexity:
            power = int(re.search(r'n\^(\d+)', complexity).group(1))
            ops = n ** power
        elif complexity == 'O(2^n)':
            ops = 2 ** n if n < 30 else float('inf')
        else:
            ops = n  # 기본값

        operations['estimated_operations'] = int(ops) if ops != float('inf') else '무한대'

        # 시간 추정 (1초에 10^8 연산 가정)
        operations_per_second = 10 ** 8
        if ops != float('inf'):
            operations['time_estimate_seconds'] = ops / operations_per_second
            operations['feasible'] = ops < operations_per_second * 2  # 2초 이내
        else:
            operations['time_estimate_seconds'] = float('inf')
            operations['feasible'] = False

        return operations

    def _check_optimization_possible(self, complexity: str, code: str) -> bool:
        """최적화 가능 여부 체크"""
        # O(n^2) 이상이면 최적화 검토
        if complexity in ['O(n^2)', 'O(n^3)', 'O(2^n)']:
            return True

        # 비효율적 패턴 감지
        if 'pop(0)' in code or ('in [' in code):
            return True

        # 중복 정렬
        if code.count('.sort()') + code.count('sorted(') > 1:
            return True

        return False

    def format_analysis(self, result: Dict) -> str:
        """분석 결과 포맷팅"""
        output = []
        output.append("=" * 80)
        output.append("⏱️ TIME & SPACE COMPLEXITY ANALYSIS")
        output.append("=" * 80)
        output.append("")

        # 전체 복잡도
        output.append("📊 종합 결과")
        output.append("-" * 80)
        output.append(f"시간 복잡도: {result['time_complexity']}")
        output.append(f"공간 복잡도: {result['space_complexity']['complexity']}")

        if result['optimization_possible']:
            output.append("⚠️ 최적화 가능 - 개선 여지 있음")
        else:
            output.append("✅ 복잡도 양호")
        output.append("")

        # 라인별 분석
        if result['line_by_line']:
            output.append("📝 라인별 분석")
            output.append("-" * 80)
            for line in result['line_by_line']:
                output.append(f"L{line['line_number']:3d} | {line['complexity']:12s} | {line['code'][:50]}")
                output.append(f"      → {line['explanation']} (연산: {line['operations']})")
            output.append("")

        # 수학적 설명
        if result['mathematical_explanation']:
            output.append("")
            for exp in result['mathematical_explanation']:
                output.append(exp)
            output.append("")

        # 공간복잡도 상세
        if result['space_complexity']['components']:
            output.append("💾 공간 복잡도 상세")
            output.append("-" * 80)
            for comp in result['space_complexity']['components']:
                output.append(f"  • {comp['type']}: {comp['complexity']}")
                output.append(f"    → {comp['explanation']}")
            output.append(f"\n총 공간: {result['space_complexity']['total']}")
            output.append("")

        # 연산 횟수 추정
        if result['total_operations']:
            ops = result['total_operations']
            output.append("🔢 실제 연산 횟수 추정")
            output.append("-" * 80)
            output.append(f"입력 크기 n = {ops['n_value']:,}")
            output.append(f"예상 연산 횟수: {ops['estimated_operations']:,}")
            if ops['time_estimate_seconds'] != float('inf'):
                output.append(f"예상 소요 시간: {ops['time_estimate_seconds']:.6f}초")
            else:
                output.append(f"예상 소요 시간: 불가능 (시간초과)")
            output.append(f"실행 가능 여부: {'✅ YES' if ops['feasible'] else '❌ NO (최적화 필요)'}")
            output.append("")

        output.append("=" * 80)

        return "\n".join(output)


if __name__ == "__main__":
    # 테스트
    analyzer = ComplexityAnalyzer()

    test_code = """
n = int(input())
arr = [int(input()) for _ in range(n)]

# 버블 정렬
for i in range(n):
    for j in range(n-1):
        if arr[j] > arr[j+1]:
            arr[j], arr[j+1] = arr[j+1], arr[j]

for num in arr:
    print(num)
    """

    result = analyzer.analyze(test_code, n_value=10000)
    print(analyzer.format_analysis(result))
