#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$DIR/runner.pid"
LOG_FILE="$DIR/runner.log"

if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if kill -0 "$OLD_PID" 2>/dev/null; then
        echo "آلة الحفر شغّالة بالفعل! PID: $OLD_PID"
        echo "لإيقافها:"
        echo "  kill $OLD_PID"
        exit 1
    fi
fi

nohup /tmp/akva_env2/bin/python3 -u "$DIR/search_importers.py" > "$LOG_FILE" 2>&1 &
PID=$!
echo $PID > "$PID_FILE"
echo "✓ آلة الحفر شغّالة! PID: $PID"
echo "لمشاهدة السجل: tail -f '$LOG_FILE'"
echo "لإيقاف:        kill $PID"
