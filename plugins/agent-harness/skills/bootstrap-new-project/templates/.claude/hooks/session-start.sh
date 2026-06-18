#!/usr/bin/env bash
# SessionStart hook — подгружает шапку wiki/index.md и хвост wiki/log.md в контекст сессии.
# Бесплатно (просто head/tail). Stdout попадает в additionalContext сессии Claude Code.
set -euo pipefail

WIKI="${CLAUDE_PROJECT_DIR:-$(pwd)}/wiki"
[ -d "$WIKI" ] || exit 0

echo "## 📚 Project knowledge (auto-loaded)"
echo "_Structure → wiki/ (check before structural answers). Process → docs/ (sessions, ADR, audits)._"
echo "_Reminder: open a session log at docs/sessions/$(date +%Y-%m)/$(date +%Y-%m-%d).md._"

if [ -f "$WIKI/index.md" ]; then
  echo ""
  echo "### wiki/index.md (top 60 lines)"
  head -n 60 "$WIKI/index.md"
fi

if [ -f "$WIKI/log.md" ]; then
  echo ""
  echo "### wiki/log.md (last 15 lines)"
  tail -n 15 "$WIKI/log.md"
fi
