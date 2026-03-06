"""
Algorithm Problem Solving Agents - Main Interface
백준 문제 풀이를 위한 통합 에이전트 인터페이스

사용법:
    python agents/main.py <command> <file_path> [options]

Commands:
    review <file>           - 코드 리뷰 (성능 최적화 중심)
    analyze <문제설명|file> - 문제 분석 (방향성 제시)
    hint <file>             - 힌트 제공 (반례 포함)
    complexity <file>       - 시간/공간 복잡도 분석
    trace <file> [input]    - 실행 흐름 추적 (절차적 사고력 향상)
    template <file>         - 추적 템플릿 생성 (손으로 채우기)
    all <file>              - 모든 분석 실행

Examples:
    python agents/main.py review Sovled/Class2/stack.py
    python agents/main.py analyze "N개의 수를 정렬하시오"
    python agents/main.py hint Sovled/Class2/fizz_buzz.py
    python agents/main.py complexity Sovled/Class2/prime_number.py
    python agents/main.py trace Sovled/Class2/fizz_buzz.py "5\n1 2 3 4 5"
    python agents/main.py template Sovled/Class2/fizz_buzz.py
    python agents/main.py all Sovled/Class2/stack_progression.py
"""

import sys
import os
from pathlib import Path

# 에이전트 임포트
from code_reviewer import SeniorCodeReviewer
from problem_analyzer import ProblemAnalyzer
from complexity_analyzer import ComplexityAnalyzer
from execution_tracer import ExecutionTracer


class AgentInterface:
    """에이전트 통합 인터페이스"""

    def __init__(self):
        self.reviewer = SeniorCodeReviewer()
        self.analyzer = ProblemAnalyzer()
        self.complexity = ComplexityAnalyzer()
        self.tracer = ExecutionTracer()

    def review_code(self, file_path: str):
        """코드 리뷰 실행"""
        print("\n🔍 시니어 코드 리뷰를 시작합니다...\n")

        code = self._read_file(file_path)
        if not code:
            return

        review_result = self.reviewer.review(code)
        print(self.reviewer.format_review(review_result))

    def analyze_problem(self, problem_input: str, explicit_hint: bool = False):
        """문제 분석 실행"""
        print("\n🎯 문제 분석을 시작합니다...\n")

        # 파일인지 텍스트인지 확인
        if os.path.exists(problem_input):
            code = self._read_file(problem_input)
            problem_text = self._extract_problem_from_comments(code)
            result = self.analyzer.analyze(
                problem_text=problem_text,
                code=code,
                explicit_hint_request=explicit_hint
            )
        else:
            # 문제 설명 텍스트로 간주
            result = self.analyzer.analyze(
                problem_text=problem_input,
                code=None,
                explicit_hint_request=explicit_hint
            )

        print(self.analyzer.format_analysis(result, explicit_hint=explicit_hint))

    def provide_hints(self, file_path: str):
        """힌트 제공 (명시적 요청)"""
        print("\n💡 힌트를 제공합니다 (반례 포함)...\n")

        code = self._read_file(file_path)
        if not code:
            return

        problem_text = self._extract_problem_from_comments(code)
        result = self.analyzer.analyze(
            problem_text=problem_text,
            code=code,
            explicit_hint_request=True  # 명시적 힌트 요청
        )

        print(self.analyzer.format_analysis(result, explicit_hint=True))

    def analyze_complexity(self, file_path: str, n_value: int = None):
        """시간/공간 복잡도 분석"""
        print("\n⏱️ 시간/공간 복잡도 분석을 시작합니다...\n")

        code = self._read_file(file_path)
        if not code:
            return

        result = self.complexity.analyze(code, n_value=n_value)
        print(self.complexity.format_analysis(result))

    def trace_execution(self, file_path: str, test_input: str = None):
        """실행 흐름 추적"""
        print("\n🔍 코드 실행 흐름을 추적합니다...\n")

        code = self._read_file(file_path)
        if not code:
            return

        result = self.tracer.trace(code, test_input=test_input)
        print(self.tracer.format_trace(result))

    def create_trace_template(self, file_path: str):
        """추적 템플릿 생성"""
        print("\n📝 추적 템플릿을 생성합니다...\n")

        code = self._read_file(file_path)
        if not code:
            return

        template = self.tracer.create_trace_template(code)
        print(template)

    def analyze_all(self, file_path: str):
        """모든 분석 실행"""
        print("\n" + "=" * 80)
        print("🚀 전체 분석을 시작합니다")
        print("=" * 80)

        code = self._read_file(file_path)
        if not code:
            return

        # 1. 복잡도 분석
        print("\n\n[1/4] 복잡도 분석")
        print("-" * 80)
        complexity_result = self.complexity.analyze(code)
        print(self.complexity.format_analysis(complexity_result))

        # 2. 코드 리뷰
        print("\n\n[2/4] 코드 리뷰")
        print("-" * 80)
        review_result = self.reviewer.review(code)
        print(self.reviewer.format_review(review_result))

        # 3. 실행 흐름 추적
        print("\n\n[3/4] 실행 흐름 추적")
        print("-" * 80)
        trace_result = self.tracer.trace(code)
        print(self.tracer.format_trace(trace_result))

        # 4. 문제 분석 (방향성만)
        print("\n\n[4/4] 문제 분석")
        print("-" * 80)
        problem_text = self._extract_problem_from_comments(code)
        analyze_result = self.analyzer.analyze(
            problem_text=problem_text,
            code=code,
            explicit_hint_request=False
        )
        print(self.analyzer.format_analysis(analyze_result, explicit_hint=False))

        print("\n" + "=" * 80)
        print("✅ 전체 분석 완료!")
        print("=" * 80)

    def _read_file(self, file_path: str) -> str:
        """파일 읽기"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
            return None
        except Exception as e:
            print(f"❌ 파일 읽기 오류: {e}")
            return None

    def _extract_problem_from_comments(self, code: str) -> str:
        """코드에서 주석으로 작성된 문제 설명 추출"""
        lines = code.split('\n')
        comments = []

        for line in lines:
            stripped = line.strip()
            if stripped.startswith('#'):
                comments.append(stripped[1:].strip())
            elif stripped.startswith('"""') or stripped.startswith("'''"):
                # 독스트링 추출
                in_docstring = True
                docstring = []
                for l in lines:
                    if '"""' in l or "'''" in l:
                        if docstring:  # 닫는 부분
                            break
                        continue
                    if in_docstring:
                        docstring.append(l)
                comments.extend(docstring)
                break

        return '\n'.join(comments) if comments else ""


def print_usage():
    """사용법 출력"""
    print(__doc__)


def main():
    """메인 함수"""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    command = sys.argv[1].lower()
    interface = AgentInterface()

    if command == 'review':
        if len(sys.argv) < 3:
            print("❌ 파일 경로를 지정해주세요.")
            print("사용법: python agents/main.py review <file_path>")
            sys.exit(1)
        interface.review_code(sys.argv[2])

    elif command == 'analyze':
        if len(sys.argv) < 3:
            print("❌ 문제 설명 또는 파일 경로를 지정해주세요.")
            print("사용법: python agents/main.py analyze <문제설명|file_path>")
            sys.exit(1)
        interface.analyze_problem(sys.argv[2], explicit_hint=False)

    elif command == 'hint':
        if len(sys.argv) < 3:
            print("❌ 파일 경로를 지정해주세요.")
            print("사용법: python agents/main.py hint <file_path>")
            sys.exit(1)
        interface.provide_hints(sys.argv[2])

    elif command == 'complexity':
        if len(sys.argv) < 3:
            print("❌ 파일 경로를 지정해주세요.")
            print("사용법: python agents/main.py complexity <file_path> [n_value]")
            sys.exit(1)

        n_value = None
        if len(sys.argv) >= 4:
            try:
                n_value = int(sys.argv[3])
            except ValueError:
                print("⚠️ n_value는 정수여야 합니다. 기본값으로 진행합니다.")

        interface.analyze_complexity(sys.argv[2], n_value=n_value)

    elif command == 'trace':
        if len(sys.argv) < 3:
            print("❌ 파일 경로를 지정해주세요.")
            print("사용법: python agents/main.py trace <file_path> [test_input]")
            sys.exit(1)

        test_input = None
        if len(sys.argv) >= 4:
            test_input = sys.argv[3]

        interface.trace_execution(sys.argv[2], test_input=test_input)

    elif command == 'template':
        if len(sys.argv) < 3:
            print("❌ 파일 경로를 지정해주세요.")
            print("사용법: python agents/main.py template <file_path>")
            sys.exit(1)
        interface.create_trace_template(sys.argv[2])

    elif command == 'all':
        if len(sys.argv) < 3:
            print("❌ 파일 경로를 지정해주세요.")
            print("사용법: python agents/main.py all <file_path>")
            sys.exit(1)
        interface.analyze_all(sys.argv[2])

    elif command in ['help', '-h', '--help']:
        print_usage()

    else:
        print(f"❌ 알 수 없는 명령어: {command}")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
