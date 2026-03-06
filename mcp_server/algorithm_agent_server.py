#!/usr/bin/env python3
"""
Algorithm Agent MCP Server
Claude Code에서 /review-algo, /hint-algo, /complexity 명령어로 사용 가능한 MCP 서버
"""

import asyncio
import json
import sys
from pathlib import Path

# 에이전트 모듈 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent / "agents"))

from code_reviewer import SeniorCodeReviewer
from problem_analyzer import ProblemAnalyzer
from complexity_analyzer import ComplexityAnalyzer
from execution_tracer import ExecutionTracer


class AlgorithmAgentServer:
    """알고리즘 에이전트 MCP 서버"""

    def __init__(self):
        self.reviewer = SeniorCodeReviewer()
        self.analyzer = ProblemAnalyzer()
        self.complexity = ComplexityAnalyzer()
        self.tracer = ExecutionTracer()

    async def handle_request(self, request: dict) -> dict:
        """MCP 요청 처리"""
        method = request.get("method")
        params = request.get("params", {})

        if method == "tools/list":
            return self._list_tools()
        elif method == "tools/call":
            return await self._call_tool(params)
        elif method == "initialize":
            return self._initialize()
        else:
            return {"error": f"Unknown method: {method}"}

    def _initialize(self) -> dict:
        """MCP 초기화"""
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "algorithm-agent",
                "version": "1.0.0"
            }
        }

    def _list_tools(self) -> dict:
        """사용 가능한 도구 목록"""
        return {
            "tools": [
                {
                    "name": "review_code",
                    "description": "시니어 레벨 코드 리뷰 (성능 최적화, 자료구조 개선, 시니어 레벨 체크)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "리뷰할 Python 코드"
                            },
                            "file_path": {
                                "type": "string",
                                "description": "코드 파일 경로 (선택사항)"
                            }
                        },
                        "required": ["code"]
                    }
                },
                {
                    "name": "analyze_problem",
                    "description": "문제 분석 및 방향성 제시 (알고리즘/자료구조 제안, 힌트 최소화)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "problem_text": {
                                "type": "string",
                                "description": "문제 설명"
                            },
                            "code": {
                                "type": "string",
                                "description": "현재 작성한 코드 (선택사항)"
                            },
                            "explicit_hint": {
                                "type": "boolean",
                                "description": "명시적으로 힌트 요청 여부 (기본: false)",
                                "default": False
                            }
                        },
                        "required": ["problem_text"]
                    }
                },
                {
                    "name": "provide_hints",
                    "description": "힌트 및 반례 제공 (명시적 요청시)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "분석할 코드"
                            },
                            "problem_text": {
                                "type": "string",
                                "description": "문제 설명 (선택사항)"
                            }
                        },
                        "required": ["code"]
                    }
                },
                {
                    "name": "analyze_complexity",
                    "description": "시간/공간 복잡도 상세 분석 (수학적 설명 포함)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "분석할 코드"
                            },
                            "n_value": {
                                "type": "integer",
                                "description": "입력 크기 (연산 횟수 추정용, 선택사항)"
                            }
                        },
                        "required": ["code"]
                    }
                },
                {
                    "name": "trace_execution",
                    "description": "코드 실행 흐름 추적 및 절차적 사고력 향상 (변수 흐름, 조건문 분기, 반복문 iteration 추적)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "추적할 코드"
                            },
                            "test_input": {
                                "type": "string",
                                "description": "테스트 입력값 (줄바꿈으로 구분, 선택사항)"
                            },
                            "max_iterations": {
                                "type": "integer",
                                "description": "반복문 최대 추적 횟수 (기본: 20)",
                                "default": 20
                            }
                        },
                        "required": ["code"]
                    }
                },
                {
                    "name": "create_trace_template",
                    "description": "코드 추적 연습용 빈 템플릿 생성 (손으로 직접 채우며 절차적 사고력 훈련)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "템플릿을 생성할 코드"
                            }
                        },
                        "required": ["code"]
                    }
                }
            ]
        }

    async def _call_tool(self, params: dict) -> dict:
        """도구 실행"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        try:
            if tool_name == "review_code":
                return self._review_code(arguments)
            elif tool_name == "analyze_problem":
                return self._analyze_problem(arguments)
            elif tool_name == "provide_hints":
                return self._provide_hints(arguments)
            elif tool_name == "analyze_complexity":
                return self._analyze_complexity(arguments)
            elif tool_name == "trace_execution":
                return self._trace_execution(arguments)
            elif tool_name == "create_trace_template":
                return self._create_trace_template(arguments)
            else:
                return {"error": f"Unknown tool: {tool_name}"}
        except Exception as e:
            return {"error": str(e)}

    def _review_code(self, args: dict) -> dict:
        """코드 리뷰 실행"""
        code = args.get("code")
        if not code:
            return {"error": "코드가 제공되지 않았습니다"}

        review_result = self.reviewer.review(code)
        formatted = self.reviewer.format_review(review_result)

        return {
            "content": [
                {
                    "type": "text",
                    "text": formatted
                }
            ]
        }

    def _analyze_problem(self, args: dict) -> dict:
        """문제 분석 실행"""
        problem_text = args.get("problem_text", "")
        code = args.get("code")
        explicit_hint = args.get("explicit_hint", False)

        result = self.analyzer.analyze(
            problem_text=problem_text,
            code=code,
            explicit_hint_request=explicit_hint
        )
        formatted = self.analyzer.format_analysis(result, explicit_hint=explicit_hint)

        return {
            "content": [
                {
                    "type": "text",
                    "text": formatted
                }
            ]
        }

    def _provide_hints(self, args: dict) -> dict:
        """힌트 제공 실행"""
        code = args.get("code")
        problem_text = args.get("problem_text", "")

        if not code:
            return {"error": "코드가 제공되지 않았습니다"}

        result = self.analyzer.analyze(
            problem_text=problem_text,
            code=code,
            explicit_hint_request=True
        )
        formatted = self.analyzer.format_analysis(result, explicit_hint=True)

        return {
            "content": [
                {
                    "type": "text",
                    "text": formatted
                }
            ]
        }

    def _analyze_complexity(self, args: dict) -> dict:
        """복잡도 분석 실행"""
        code = args.get("code")
        n_value = args.get("n_value")

        if not code:
            return {"error": "코드가 제공되지 않았습니다"}

        result = self.complexity.analyze(code, n_value=n_value)
        formatted = self.complexity.format_analysis(result)

        return {
            "content": [
                {
                    "type": "text",
                    "text": formatted
                }
            ]
        }

    def _trace_execution(self, args: dict) -> dict:
        """실행 흐름 추적 실행"""
        code = args.get("code")
        test_input = args.get("test_input")
        max_iterations = args.get("max_iterations", 20)

        if not code:
            return {"error": "코드가 제공되지 않았습니다"}

        result = self.tracer.trace(code, test_input=test_input, max_iterations=max_iterations)
        formatted = self.tracer.format_trace(result)

        return {
            "content": [
                {
                    "type": "text",
                    "text": formatted
                }
            ]
        }

    def _create_trace_template(self, args: dict) -> dict:
        """추적 템플릿 생성 실행"""
        code = args.get("code")

        if not code:
            return {"error": "코드가 제공되지 않았습니다"}

        template = self.tracer.create_trace_template(code)

        return {
            "content": [
                {
                    "type": "text",
                    "text": template
                }
            ]
        }


async def main():
    """메인 함수 - stdio를 통한 MCP 통신"""
    server = AlgorithmAgentServer()

    # stdin에서 요청 읽기, stdout으로 응답 쓰기
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(
                None, sys.stdin.readline
            )
            if not line:
                break

            request = json.loads(line)
            response = await server.handle_request(request)

            # 응답 출력
            print(json.dumps(response), flush=True)

        except json.JSONDecodeError:
            error_response = {"error": "Invalid JSON"}
            print(json.dumps(error_response), flush=True)
        except Exception as e:
            error_response = {"error": str(e)}
            print(json.dumps(error_response), flush=True)


if __name__ == "__main__":
    asyncio.run(main())
