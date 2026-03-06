#!/bin/bash
# Claude Code MCP 자동 설정 스크립트

set -e

echo "🚀 Algorithm Agent MCP 서버 설정 시작..."
echo ""

# 현재 디렉토리
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SERVER_PATH="$SCRIPT_DIR/mcp_server/algorithm_agent_server.py"

# Python 경로 확인
PYTHON_PATH=$(which python3)
if [ -z "$PYTHON_PATH" ]; then
    echo "❌ python3를 찾을 수 없습니다. Python 3.9 이상을 설치해주세요."
    exit 1
fi

echo "✅ Python 경로: $PYTHON_PATH"
echo "✅ 서버 경로: $SERVER_PATH"
echo ""

# Claude 설정 디렉토리
CLAUDE_CONFIG_DIR="$HOME/.config/claude"
CLAUDE_SETTINGS="$CLAUDE_CONFIG_DIR/settings.json"

# 디렉토리 생성
mkdir -p "$CLAUDE_CONFIG_DIR"

echo "📝 Claude Code 설정 파일 업데이트 중..."

# 기존 설정 파일이 있는지 확인
if [ -f "$CLAUDE_SETTINGS" ]; then
    echo "⚠️  기존 설정 파일이 있습니다: $CLAUDE_SETTINGS"
    echo "   백업을 만들겠습니다: ${CLAUDE_SETTINGS}.backup"
    cp "$CLAUDE_SETTINGS" "${CLAUDE_SETTINGS}.backup"

    # jq가 있으면 JSON 병합, 없으면 수동 안내
    if command -v jq &> /dev/null; then
        # MCP 서버 설정 추가
        jq --arg cmd "$PYTHON_PATH" --arg path "$SERVER_PATH" \
            '.mcpServers."algorithm-agent" = {
                "command": $cmd,
                "args": [$path],
                "description": "시니어 개발자를 위한 알고리즘 문제 풀이 에이전트"
            }' "$CLAUDE_SETTINGS" > "${CLAUDE_SETTINGS}.tmp"
        mv "${CLAUDE_SETTINGS}.tmp" "$CLAUDE_SETTINGS"
        echo "✅ 설정 파일이 자동으로 업데이트되었습니다!"
    else
        echo ""
        echo "⚠️  jq가 설치되지 않아 수동 설정이 필요합니다."
        echo ""
        echo "다음 내용을 $CLAUDE_SETTINGS 파일의 mcpServers 섹션에 추가하세요:"
        echo ""
        cat <<EOF
{
  "mcpServers": {
    "algorithm-agent": {
      "command": "$PYTHON_PATH",
      "args": [
        "$SERVER_PATH"
      ],
      "description": "시니어 개발자를 위한 알고리즘 문제 풀이 에이전트"
    }
  }
}
EOF
        echo ""
    fi
else
    # 새로운 설정 파일 생성
    echo "📄 새로운 설정 파일 생성 중..."
    cat > "$CLAUDE_SETTINGS" <<EOF
{
  "mcpServers": {
    "algorithm-agent": {
      "command": "$PYTHON_PATH",
      "args": [
        "$SERVER_PATH"
      ],
      "description": "시니어 개발자를 위한 알고리즘 문제 풀이 에이전트"
    }
  }
}
EOF
    echo "✅ 설정 파일이 생성되었습니다: $CLAUDE_SETTINGS"
fi

# 실행 권한 부여
chmod +x "$SERVER_PATH"
echo "✅ 서버 실행 권한 설정 완료"

echo ""
echo "🎉 설정 완료!"
echo ""
echo "📋 다음 단계:"
echo "   1. Claude Code를 재시작하세요"
echo "   2. Claude와 대화하면서 다음과 같이 요청하세요:"
echo ""
echo "      \"이 코드를 review_code 도구로 리뷰해줘\""
echo "      \"이 문제를 analyze_problem 도구로 분석해줘\""
echo "      \"이 코드를 analyze_complexity 도구로 분석해줘\""
echo "      \"이 코드를 provide_hints 도구로 힌트 줘\""
echo ""
echo "🔍 문제 해결:"
echo "   - 도구가 안 보이면: Claude Code 재시작"
echo "   - 오류 발생시: $SERVER_PATH 직접 실행하여 확인"
echo "   - 자세한 가이드: $SCRIPT_DIR/CLAUDE_SETUP.md"
echo ""
echo "✨ 즐거운 알고리즘 풀이 되세요!"
