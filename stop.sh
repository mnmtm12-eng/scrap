#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$DIR/runner.pid"
LOG_FILE="$DIR/runner.log"

if [ ! -f "$PID_FILE" ]; then
    echo "ما في آلة حفر شغّالة (لا يوجد PID file)"
    exit 1
fi

PID=$(cat "$PID_FILE")
echo "🛑 إيقاف آلة الحفر (PID: $PID)..."
kill "$PID" 2>/dev/null
sleep 1
if kill -0 "$PID" 2>/dev/null; then
    kill -9 "$PID" 2>/dev/null
fi
rm -f "$PID_FILE"
echo "✓ أوقفت!"
echo "آخر سجل:"
tail -5 "$LOG_FILE" 2>/dev/null
