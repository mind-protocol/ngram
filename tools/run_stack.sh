#!/usr/bin/env bash
# DOCS: docs/tools/PATTERNS_Tools.md
set -euo pipefail

LOG_DIR="${LOG_DIR:-./logs/run_stack}"
ERROR_LOG="${ERROR_LOG:-./.ngram/error.log}"
mkdir -p "$LOG_DIR"
mkdir -p "$(dirname "$ERROR_LOG")"

FALKORDB_CMD="${FALKORDB_CMD:-falkordb-server}"
FALKORDB_PATTERN="${FALKORDB_PATTERN:-$FALKORDB_CMD}"

BE_CMD="${BE_CMD:-}"
BE_PATTERN="${BE_PATTERN:-$BE_CMD}"

FE_CMD="${FE_CMD:-}"
FE_PATTERN="${FE_PATTERN:-$FE_CMD}"
FE_SKIP_RESTART=0

MCP_CMD="${MCP_CMD:-cd ~/FalkorDB-MCPServer && HOST=127.0.0.1 PORT=3005 npm run dev}"
MCP_PATTERN="${MCP_PATTERN:-FalkorDB-MCPServer}"

NGROK_URL="${NGROK_URL:-https://trusted-magpie-social.ngrok-free.app}"
NGROK_PORT="${NGROK_PORT:-3005}"
NGROK_CMD="${NGROK_CMD:-ngrok http $NGROK_PORT --url $NGROK_URL}"
NGROK_PATTERN="${NGROK_PATTERN:-ngrok http $NGROK_PORT --url $NGROK_URL}"

stop_service() {
  local name="$1"
  local pattern="$2"

  if [[ -z "$pattern" ]]; then
    echo "○ Skipping stop for $name (no pattern configured)"
    return
  fi

  if pgrep -f "$pattern" >/dev/null 2>&1; then
    echo "Stopping $name (pattern: $pattern)"
    pkill -f "$pattern" || true
    sleep 2
    if pgrep -f "$pattern" >/dev/null 2>&1; then
      echo "Force stopping $name"
      pkill -9 -f "$pattern" || true
    fi
  else
    echo "○ $name not running"
  fi
}

start_service() {
  local name="$1"
  local cmd="$2"
  local log_file="$3"

  if [[ -z "$cmd" ]]; then
    echo "○ Skipping start for $name (no command configured)"
    return
  fi

  echo "Starting $name → $log_file"
  setsid -f bash -lc "$cmd" >"$log_file" 2>>"$ERROR_LOG"
}

stop_service "FalkorDB" "$FALKORDB_PATTERN"
stop_service "Backend" "$BE_PATTERN"
if [[ -n "$FE_PATTERN" ]] && pgrep -f "$FE_PATTERN" >/dev/null 2>&1; then
  echo "○ Frontend already running; skipping restart"
  FE_SKIP_RESTART=1
else
  stop_service "Frontend" "$FE_PATTERN"
fi
stop_service "FalkorDB-MCPServer" "$MCP_PATTERN"
stop_service "ngrok" "$NGROK_PATTERN"

start_service "FalkorDB" "$FALKORDB_CMD" "$LOG_DIR/falkordb.log"
start_service "Backend" "$BE_CMD" "$LOG_DIR/backend.log"
if [[ "$FE_SKIP_RESTART" -eq 0 ]]; then
  start_service "Frontend" "$FE_CMD" "$LOG_DIR/frontend.log"
fi
start_service "FalkorDB-MCPServer" "$MCP_CMD" "$LOG_DIR/mcp.log"
start_service "ngrok" "$NGROK_CMD" "$LOG_DIR/ngrok.log"

echo "✓ Restart complete. Logs at $LOG_DIR"
