#!/bin/bash
"""
نسخ احتياطي يومي — مجلد الأرقام
يرسل نسخة إلى Desktop_Cleanup/Backups ويمكن إيميل
"""

DIR="$(cd "$(dirname "$0")" && pwd)"
BACKUP_DIR="$DIR/../Desktop_Cleanup/Backups"
mkdir -p "$BACKUP_DIR"

DATE=$(date +%Y-%m-%d)
BACKUP_FILE="$BACKUP_DIR/ارقام_من_الانترنت_يومي_$DATE.zip"

# Compress important files
zip -j "$BACKUP_FILE" \
    "$DIR/contacts.xlsx" \
    "$DIR/results.csv" \
    "$DIR/calculator_history.json" \
    "$DIR/seen_urls.json" 2>/dev/null

echo "✓ باك أب: $BACKUP_FILE ($(du -h "$BACKUP_FILE" | cut -f1))"

# Keep only last 7 backups
find "$BACKUP_DIR" -name "ارقام_من_الانترنت_يومي_*.zip" -mtime +7 -delete 2>/dev/null
