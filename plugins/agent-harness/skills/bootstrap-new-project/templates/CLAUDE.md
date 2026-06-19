# CLAUDE.md — {{PROJECT_NAME}}

This file provides guidance to Claude Code when working in this repository.

## MANDATORY: Session logging
Каждая сессия ведёт лог в `docs/sessions/YYYY-MM/YYYY-MM-DD.md` (папка на месяц).
- **Старт:** создать файл (или открыть за тот же день), записать цель из первого сообщения owner'а.
- **По ходу:** логировать значимые действия, решения с обоснованием и проблемы — сразу, не в конце.
- **Конец:** дописать «Итог», финализировать «Открытые вопросы», закоммитить лог.
Формат — `docs/sessions/TEMPLATE.md`.

## CRITICAL: No hardcoded secrets
**НИКОГДА** не класть пароли, токены, ключи в файлы под git — высший приоритет.
- Все секреты — в `.env` (в `.gitignore`, не коммитится).
- Конфиги/код используют `${ENV_VARS}` или чтение из окружения.
- `.env.example` — только плейсхолдеры.
- Перед каждым коммитом — grep на утёкшие паттерны (ключи, токены, пароли).
- Утёкший в историю секрет = **скомпрометирован**, ротировать немедленно.

## What is this
{{DOMAIN}}

## Tech stack
{{STACK}}

## Commands
{{COMMANDS}}

## Architecture
_Owner заполнит общую картину. Машинная карта структуры кода — в Understand-Anything (см. ниже)._

## Structural knowledge — три слоя
**Структурные вопросы (схема БД, маршруты, зависимости, что-на-что-влияет)** — сначала
смотри **Understand-Anything**: `/understand-chat "..."` или дашборд `/understand-dashboard`
(граф из кода, регенерируется командой `/understand`). Это машинная карта структуры.

- **Understand-Anything** — авто-карта структуры кода (граф файлов/функций/зависимостей). Регенерируем по требованию, **без `--auto-update` хука** (запускаем `/understand` осознанно на гейтах, как `/dashboard`). Граф = производное представление, не source of truth.
- **`wiki/`** — только структурные заметки, которые UA **не выводит** из кода: бизнес-инварианты, договорённости, «почему именно так». Обновляй в том же PR, что меняет код.
- **`docs/`** — процесс (сессии, решения/ADR, инциденты, статистика). См. `docs/README.md`.

Source of truth = код + миграции + ADR. Установка UA — см. `docs/decisions/0002-understand-anything.md`.

## Жизненный цикл и статистика (обвязка)
Агент ведёт задачу через 6 этапов; на выходе с каждого — проверка-условие (тривиальное пропускается). Подробности и обоснование — `docs/decisions/0001-adopt-harness.md`.

1. **Требования** — записан список «что должно получиться» (acceptance criteria, риски, не-цели).
2. **Дизайн** — решение записано (ADR в `docs/decisions/`) и прошло multi-agent review.
3. **Код** — код готов; `wiki/`-заметки и (по необходимости) граф UA (`/understand`) обновлены.
4. **Тесты (VERIFY)** — тесты зелёные, покрытие ≥ порог; прогнан `/understand-diff` (ripple-эффект изменений); проверяющий выдал вердикт по `docs/reviews/review-format.md`, сверившись с `CODE-REVIEW.md`.
5. **Релиз** — pre-push checklist пройден, CI зелёный, есть runbook.
6. **Бой** — после выката: health + tail логов 2 мин + smoke; инцидент → `docs/audits/` + `docs/analytics/incidents.md`.

**На выходе с каждого этапа** допиши строку в `docs/analytics/runs.md` (только дописывать; колонки — в `docs/analytics/README.md`). **Перед отправкой кода** пересобери сводку: `python3 scripts/analytics/build_dashboard.py` (сам `dashboard.md` руками не правь).

**Петля самоулучшения:** каждый разбор поломки добавляет правило в `CODE-REVIEW.md`, чтобы ошибка не повторилась.

## Multi-agent review policy
PR с любым из триггеров требует параллельного ревью 3 агентами
(`architect` + `code-reviewer` + `security-reviewer`) **до merge** в main.
**Триггеры (любой):** ≥500 строк изменений в коде (без docs/tests); любое изменение в
`.github/workflows/`; новая миграция БД; изменение LLM-кода (prompt / API surface).
**Опционально:** `database-reviewer` (схема/SQL), `performance-optimizer` (hot path).
**Exit:** CRITICAL → BLOCK (fix или revert); HIGH → fix либо явный accept в PR;
MEDIUM → backlog/опц.; LOW → informational.
**Не нужно:** docs-only, минорные фиксы (<50 строк, без миграций/LLM), формат, dep-bump.

## Known footguns (НЕ повторять)
Грабли, на которые уже наступали → ведутся в `CODE-REVIEW.md` (раздел «Граблиный список»)
и в `docs/audits/`. Если решение «проще в обход» — сначала перечитай.

## Pre-push + Post-deploy
**Pre-push (перед каждым push в main):** линтер 0 ошибок · type-check 0 ошибок ·
тесты passed + coverage ≥ gate · `python3 scripts/analytics/build_dashboard.py`.
Coverage gate в CI **должен совпадать** с локальным.
**Post-deploy:** health-check (200) → tail логов **минимум 2 минуты** → smoke, если менялся
LLM/config. Зелёный CI ≠ работающий прод. Деталь — `docs/operations/runbook-prod-deploy.md`.
