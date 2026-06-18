# agent-harness (плагин)

База знаний + обвязка для full-cycle dev-агента. Подробности и установка — в [README репозитория](../../README.md).

- **skills/bootstrap-new-project/** — генератор обвязки (`SKILL.md` + `BOOTSTRAP.md` + `templates/`).
- **commands/** — `/bootstrap` (развернуть), `/dashboard` (пересчитать сводку).

Шаблоны находятся через `${CLAUDE_PLUGIN_ROOT}/skills/bootstrap-new-project/templates` (с fallback на локальный `~/.claude/skills/...`).
