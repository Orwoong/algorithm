"""
Execution Tracer Agent
코드 실행 흐름 추적 및 값 변화 시각화 에이전트

목적:
- 절차적 코드 실행 흐름 추적
- 변수 값 변화 시각화
- 조건문 분기 추적
- 반복문 iteration별 값 추적
- 디버깅 사고력 향상
"""

import re
import ast
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict


class ExecutionTracer:
    """코드 실행 흐름 추적 및 시각화 에이전트"""

    def __init__(self):
        self.trace_limit = 20  # 반복문 최대 추적 횟수

    def trace(self, code: str, test_input: str = None, max_iterations: int = 20) -> Dict:
        """
        코드 실행 흐름 추적

        Args:
            code: 분석할 Python 코드
            test_input: 테스트용 입력값 (줄바꿈으로 구분)
            max_iterations: 반복문 최대 추적 횟수

        Returns:
            추적 결과 딕셔너리
        """
        self.trace_limit = max_iterations

        result = {
            'static_analysis': self._static_analysis(code),
            'execution_flow': None,  # 실제 실행 추적 (입력값 있을 때)
            'variable_tracking': self._track_variable_flow(code),
            'conditional_branches': self._analyze_conditionals(code),
            'loop_analysis': self._analyze_loops(code),
            'recommendations': []
        }

        # 실제 실행 추적 (안전한 경우만)
        if test_input and self._is_safe_to_execute(code):
            result['execution_flow'] = self._trace_execution(code, test_input)
        else:
            result['recommendations'].append(
                "실제 실행 추적을 원하면 test_input을 제공하세요 (간단한 코드만 지원)"
            )

        # 학습 추천
        result['recommendations'].extend(self._generate_recommendations(result))

        return result

    def _static_analysis(self, code: str) -> Dict:
        """정적 코드 분석 - 구조 파악"""
        analysis = {
            'total_lines': len(code.split('\n')),
            'functions': [],
            'loops': [],
            'conditionals': [],
            'variables': set(),
            'complexity_indicators': {}
        }

        lines = code.split('\n')

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # 함수 정의
            if stripped.startswith('def '):
                func_name = re.search(r'def\s+(\w+)', stripped)
                if func_name:
                    analysis['functions'].append({
                        'name': func_name.group(1),
                        'line': i
                    })

            # 반복문
            if stripped.startswith('for ') or stripped.startswith('while '):
                loop_type = 'for' if stripped.startswith('for') else 'while'
                analysis['loops'].append({
                    'type': loop_type,
                    'line': i,
                    'code': stripped
                })

            # 조건문
            if stripped.startswith('if ') or stripped.startswith('elif ') or stripped.startswith('else'):
                cond_type = stripped.split()[0]
                analysis['conditionals'].append({
                    'type': cond_type,
                    'line': i,
                    'code': stripped
                })

            # 변수 할당
            if '=' in stripped and not any(op in stripped for op in ['==', '!=', '<=', '>=']):
                var_match = re.search(r'^(\w+)\s*=', stripped)
                if var_match:
                    analysis['variables'].add(var_match.group(1))

        # 복잡도 지표
        analysis['complexity_indicators'] = {
            'loop_count': len(analysis['loops']),
            'conditional_count': len(analysis['conditionals']),
            'nested_loops': self._count_nested_loops(code),
            'max_nesting_depth': self._calculate_nesting_depth(code)
        }

        return analysis

    def _track_variable_flow(self, code: str) -> List[Dict]:
        """변수 흐름 추적 - 변수가 어디서 생성/수정되는지"""
        tracking = []
        lines = code.split('\n')

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # 변수 선언 및 할당
            if '=' in stripped:
                # 할당 연산자 찾기 (비교 연산자 제외)
                if not any(op in stripped for op in ['==', '!=', '<=', '>=', '//=']):
                    var_match = re.search(r'^(\w+(?:\[.*?\])?)\s*([+\-*/%]?=)\s*(.+)', stripped)
                    if var_match:
                        var_name = var_match.group(1)
                        operator = var_match.group(2)
                        value_expr = var_match.group(3)

                        action = 'created' if operator == '=' else 'modified'

                        tracking.append({
                            'line': i,
                            'variable': var_name,
                            'action': action,
                            'operator': operator,
                            'expression': value_expr,
                            'code': stripped
                        })

            # 리스트 메서드 (append, pop, etc.)
            list_methods = ['append', 'pop', 'remove', 'insert', 'extend']
            for method in list_methods:
                if f'.{method}(' in stripped:
                    var_match = re.search(r'(\w+)\.' + method, stripped)
                    if var_match:
                        tracking.append({
                            'line': i,
                            'variable': var_match.group(1),
                            'action': 'modified',
                            'operator': f'.{method}()',
                            'expression': stripped,
                            'code': stripped
                        })

        return tracking

    def _analyze_conditionals(self, code: str) -> List[Dict]:
        """조건문 분석 - 분기 흐름 파악"""
        conditionals = []
        lines = code.split('\n')

        current_if_block = None
        indent_stack = []

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            indent_level = len(line) - len(line.lstrip())

            if stripped.startswith('if '):
                condition = re.search(r'if\s+(.+):', stripped)
                if condition:
                    current_if_block = {
                        'line': i,
                        'type': 'if',
                        'condition': condition.group(1),
                        'indent': indent_level,
                        'branches': [{
                            'type': 'if',
                            'condition': condition.group(1),
                            'line': i,
                            'truth_value_matters': self._explain_condition(condition.group(1))
                        }]
                    }
                    conditionals.append(current_if_block)

            elif stripped.startswith('elif ') and current_if_block:
                condition = re.search(r'elif\s+(.+):', stripped)
                if condition:
                    current_if_block['branches'].append({
                        'type': 'elif',
                        'condition': condition.group(1),
                        'line': i,
                        'truth_value_matters': self._explain_condition(condition.group(1))
                    })

            elif stripped.startswith('else:') and current_if_block:
                current_if_block['branches'].append({
                    'type': 'else',
                    'condition': 'default (모든 조건 False일 때)',
                    'line': i,
                    'truth_value_matters': '위의 모든 조건이 False일 때 실행'
                })
                current_if_block = None  # if 블록 종료

        return conditionals

    def _explain_condition(self, condition: str) -> str:
        """조건식 설명"""
        explanations = []

        # 비교 연산자
        if '>' in condition:
            explanations.append("'>'보다 큰 경우 True")
        if '<' in condition:
            explanations.append("'<'보다 작은 경우 True")
        if '==' in condition:
            explanations.append("'=='같은 경우 True")
        if '!=' in condition:
            explanations.append("'!='다른 경우 True")
        if '>=' in condition:
            explanations.append("'>='크거나 같은 경우 True")
        if '<=' in condition:
            explanations.append("'<='작거나 같은 경우 True")

        # 논리 연산자
        if ' and ' in condition:
            explanations.append("'and' 양쪽 모두 True여야 True")
        if ' or ' in condition:
            explanations.append("'or' 하나만 True여도 True")
        if 'not ' in condition:
            explanations.append("'not' 조건 반대")

        # in 연산자
        if ' in ' in condition:
            explanations.append("'in' 포함되어 있으면 True")
        if ' not in ' in condition:
            explanations.append("'not in' 포함되어 있지 않으면 True")

        return ' | '.join(explanations) if explanations else '조건 확인 필요'

    def _analyze_loops(self, code: str) -> List[Dict]:
        """반복문 분석 - iteration 흐름 파악"""
        loops = []
        lines = code.split('\n')

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # for 루프
            if stripped.startswith('for '):
                loop_match = re.search(r'for\s+(\w+)\s+in\s+(.+):', stripped)
                if loop_match:
                    var = loop_match.group(1)
                    iterable = loop_match.group(2)

                    loops.append({
                        'line': i,
                        'type': 'for',
                        'variable': var,
                        'iterable': iterable,
                        'code': stripped,
                        'iteration_explanation': self._explain_for_loop(var, iterable)
                    })

            # while 루프
            elif stripped.startswith('while '):
                condition = re.search(r'while\s+(.+):', stripped)
                if condition:
                    loops.append({
                        'line': i,
                        'type': 'while',
                        'condition': condition.group(1),
                        'code': stripped,
                        'iteration_explanation': f"조건 '{condition.group(1)}'가 True인 동안 반복"
                    })

        return loops

    def _explain_for_loop(self, var: str, iterable: str) -> str:
        """for 루프 설명"""
        if 'range(' in iterable:
            # range 분석
            range_match = re.search(r'range\(([^)]+)\)', iterable)
            if range_match:
                args = range_match.group(1).split(',')
                args = [arg.strip() for arg in args]

                if len(args) == 1:
                    return f"{var}이 0부터 {args[0]}-1까지 순회 (총 {args[0]}번)"
                elif len(args) == 2:
                    return f"{var}이 {args[0]}부터 {args[1]}-1까지 순회"
                elif len(args) == 3:
                    return f"{var}이 {args[0]}부터 {args[1]}-1까지 {args[2]} 간격으로 순회"

        elif '[' in iterable or iterable in ['list', 'arr', 'nums']:
            return f"{var}이 리스트의 각 원소를 순회"

        elif 'enumerate(' in iterable:
            return f"{var}이 (인덱스, 값) 튜플을 순회"

        elif 'zip(' in iterable:
            return f"{var}이 여러 iterable을 동시에 순회"

        return f"{var}이 {iterable}의 각 원소를 순회"

    def _trace_execution(self, code: str, test_input: str) -> Dict:
        """
        실제 코드 실행 추적 (간단한 코드만)
        주의: 복잡한 코드는 정적 분석만 사용
        """
        # 실행 환경 설정
        input_lines = test_input.strip().split('\n')
        input_idx = [0]  # mutable counter

        def mock_input(prompt=''):
            if input_idx[0] < len(input_lines):
                value = input_lines[input_idx[0]]
                input_idx[0] += 1
                return value
            return ''

        # 변수 추적을 위한 래퍼
        execution_trace = {
            'steps': [],
            'final_state': {},
            'output': [],
            'max_iterations_reached': False
        }

        # 간단한 추적 (실제로는 AST 기반 인터프리터 필요)
        # 여기서는 개념적 설명만 제공
        execution_trace['steps'].append({
            'note': '실제 실행 추적은 복잡한 코드에서는 제한적입니다.',
            'recommendation': '아래의 정적 분석 결과를 참고하세요.'
        })

        return execution_trace

    def _is_safe_to_execute(self, code: str) -> bool:
        """실행해도 안전한 코드인지 확인"""
        # 위험한 키워드 체크
        dangerous_keywords = [
            'import os', 'import sys', '__import__',
            'eval(', 'exec(', 'compile(',
            'open(', 'file(',
            'subprocess', 'socket'
        ]

        for keyword in dangerous_keywords:
            if keyword in code:
                return False

        return True

    def _count_nested_loops(self, code: str) -> int:
        """중첩 루프 개수 세기"""
        lines = code.split('\n')
        max_nested = 0
        current_nested = 0

        for line in lines:
            stripped = line.strip()
            indent = len(line) - len(line.lstrip())

            if stripped.startswith('for ') or stripped.startswith('while '):
                current_nested += 1
                max_nested = max(max_nested, current_nested)
            elif indent == 0 and stripped:
                current_nested = 0

        return max_nested

    def _calculate_nesting_depth(self, code: str) -> int:
        """최대 중첩 깊이 계산"""
        lines = code.split('\n')
        max_depth = 0

        for line in lines:
            if line.strip():
                indent = len(line) - len(line.lstrip())
                depth = indent // 4  # 4칸 = 1 depth
                max_depth = max(max_depth, depth)

        return max_depth

    def _generate_recommendations(self, result: Dict) -> List[str]:
        """학습 추천사항 생성"""
        recommendations = []

        static = result['static_analysis']

        # 복잡도 기반 추천
        if static['complexity_indicators']['nested_loops'] >= 2:
            recommendations.append(
                "💡 중첩 루프가 있습니다. 각 루프의 iteration을 종이에 그려보며 추적해보세요."
            )

        if len(result['conditional_branches']) > 3:
            recommendations.append(
                "💡 조건문이 많습니다. 각 조건의 True/False 케이스를 표로 정리해보세요."
            )

        if len(result['loop_analysis']) > 0:
            recommendations.append(
                "💡 반복문 연습: 첫 3번의 iteration을 손으로 따라해보세요. 패턴이 보일 겁니다."
            )

        if len(result['variable_tracking']) > 10:
            recommendations.append(
                "💡 변수가 많습니다. 각 변수의 역할을 주석으로 정리하면 흐름 파악이 쉬워집니다."
            )

        return recommendations

    def format_trace(self, result: Dict) -> str:
        """추적 결과 포맷팅"""
        output = []
        output.append("=" * 80)
        output.append("🔍 CODE EXECUTION TRACER")
        output.append("=" * 80)
        output.append("")

        # 1. 정적 분석
        static = result['static_analysis']
        output.append("📊 코드 구조 분석 (Static Analysis)")
        output.append("-" * 80)
        output.append(f"총 줄 수: {static['total_lines']}")
        output.append(f"함수 개수: {len(static['functions'])}")
        output.append(f"반복문 개수: {len(static['loops'])}")
        output.append(f"조건문 개수: {len(static['conditionals'])}")
        output.append(f"변수 개수: {len(static['variables'])}")
        output.append("")

        complexity = static['complexity_indicators']
        output.append("복잡도 지표:")
        output.append(f"  - 중첩 루프 수: {complexity['nested_loops']}")
        output.append(f"  - 최대 중첩 깊이: {complexity['max_nesting_depth']}")
        output.append("")

        # 2. 변수 흐름 추적
        if result['variable_tracking']:
            output.append("📝 변수 흐름 추적 (Variable Flow)")
            output.append("-" * 80)
            output.append("라인 | 변수명 | 동작 | 연산 | 설명")
            output.append("-" * 80)

            for track in result['variable_tracking'][:15]:  # 최대 15개
                output.append(
                    f"{track['line']:4d} | {track['variable']:15s} | "
                    f"{track['action']:8s} | {track['operator']:10s} | "
                    f"{track['expression'][:30]}"
                )

            if len(result['variable_tracking']) > 15:
                output.append(f"... (총 {len(result['variable_tracking'])}개 중 15개만 표시)")
            output.append("")

        # 3. 조건문 분석
        if result['conditional_branches']:
            output.append("🔀 조건문 분기 분석 (Conditional Branches)")
            output.append("-" * 80)

            for idx, cond in enumerate(result['conditional_branches'], 1):
                output.append(f"\n[조건문 블록 #{idx}] (라인 {cond['line']})")

                for branch in cond['branches']:
                    output.append(f"  {branch['type']:5s} | 조건: {branch['condition']}")
                    output.append(f"        → {branch['truth_value_matters']}")

                output.append("")
                output.append("  💡 연습 방법:")
                output.append("     1. 각 조건이 True/False일 때 어느 블록이 실행되는지 표로 작성")
                output.append("     2. 경계값(boundary values)을 대입해보기")
                output.append("")

        # 4. 반복문 분석
        if result['loop_analysis']:
            output.append("🔄 반복문 분석 (Loop Analysis)")
            output.append("-" * 80)

            for idx, loop in enumerate(result['loop_analysis'], 1):
                output.append(f"\n[반복문 #{idx}] (라인 {loop['line']})")
                output.append(f"  타입: {loop['type']}")
                output.append(f"  코드: {loop['code']}")
                output.append(f"  설명: {loop['iteration_explanation']}")

                if loop['type'] == 'for':
                    output.append(f"\n  💡 추적 연습:")
                    output.append(f"     변수 '{loop['variable']}'의 값 변화를 직접 써보세요:")
                    output.append(f"     iteration 1: {loop['variable']} = ?")
                    output.append(f"     iteration 2: {loop['variable']} = ?")
                    output.append(f"     iteration 3: {loop['variable']} = ?")
                    output.append(f"     ... (패턴을 찾아보세요)")

                output.append("")

        # 5. 추천사항
        if result['recommendations']:
            output.append("💡 학습 추천사항 (Recommendations)")
            output.append("-" * 80)
            for rec in result['recommendations']:
                output.append(f"  {rec}")
            output.append("")

        # 6. 디버깅 팁
        output.append("🎯 절차적 사고력 향상 팁")
        output.append("-" * 80)
        output.append("1. 코드를 실행하기 전에 종이에 변수 테이블을 만드세요")
        output.append("   예: | step | i | j | arr | result |")
        output.append("")
        output.append("2. 반복문은 첫 3번의 iteration을 손으로 따라하세요")
        output.append("   - 변수 값이 어떻게 변하는지")
        output.append("   - 조건문이 True/False 중 무엇인지")
        output.append("")
        output.append("3. 조건문은 경계값을 대입해보세요")
        output.append("   - if x > 5: → x=4, x=5, x=6 각각 어떻게 되는가?")
        output.append("")
        output.append("4. print()로 중간 값을 출력하며 디버깅하세요")
        output.append("   - 예상과 실제 값이 다른 지점을 찾으세요")
        output.append("")

        output.append("=" * 80)
        output.append("🚀 반복 연습하면 절차적 흐름이 자동으로 보이게 됩니다!")
        output.append("=" * 80)

        return "\n".join(output)

    def create_trace_template(self, code: str) -> str:
        """
        코드 추적용 템플릿 생성
        사용자가 손으로 직접 채워넣을 수 있는 표 형식
        """
        template = []
        template.append("=" * 80)
        template.append("📝 코드 추적 연습 템플릿")
        template.append("=" * 80)
        template.append("")
        template.append("아래 표를 채워가며 코드를 추적해보세요:")
        template.append("")

        # 변수 추출
        result = self.trace(code)
        variables = set()
        for track in result['variable_tracking']:
            # 배열 인덱스 제거
            var_name = re.sub(r'\[.*?\]', '', track['variable'])
            variables.add(var_name)

        # 테이블 헤더
        var_list = sorted(list(variables))
        header = "| Step | Line |"
        for var in var_list:
            header += f" {var:12s} |"

        template.append(header)
        template.append("|" + "------|------|" + "--------------|" * len(var_list))

        # 샘플 행
        for i in range(5):
            row = f"|  {i+1:2d}  |      |"
            for _ in var_list:
                row += "              |"
            template.append(row)

        template.append("|  ... |  ... |" + "      ...     |" * len(var_list))
        template.append("")
        template.append("💡 사용 방법:")
        template.append("1. 코드를 한 줄씩 실행한다고 생각하세요")
        template.append("2. 각 Step에서 변수 값이 어떻게 변하는지 기록하세요")
        template.append("3. 조건문은 True/False 여부를 확인하세요")
        template.append("4. 반복문은 각 iteration마다 새로운 행을 추가하세요")
        template.append("")

        return "\n".join(template)


if __name__ == "__main__":
    # 테스트
    tracer = ExecutionTracer()

    test_code = """
n = int(input())
arr = list(map(int, input().split()))

result = 0
for i in range(n):
    if arr[i] > 0:
        result += arr[i]
    elif arr[i] < 0:
        result -= arr[i]
    else:
        result = 0

print(result)
"""

    print("=" * 80)
    print("테스트 1: 기본 추적")
    print("=" * 80)

    result = tracer.trace(test_code, test_input="5\n1 -2 3 -4 5")
    print(tracer.format_trace(result))

    print("\n\n")
    print("=" * 80)
    print("테스트 2: 추적 템플릿 생성")
    print("=" * 80)
    print(tracer.create_trace_template(test_code))
