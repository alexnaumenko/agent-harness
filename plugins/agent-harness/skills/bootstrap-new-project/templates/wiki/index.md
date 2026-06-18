---
title: Wiki Index — {{PROJECT_NAME}} (структурное знание)
type: index
source file path: wiki/index.md
created date: {{DATE}}
updated date: {{DATE}}
tags: [index, catalog, structure]
confidence level: high
---

**TL;DR:** Каталог **структурного** знания о коде {{PROJECT_NAME}} (схема БД, маршруты, архитектура). Процессное знание (сессии, audits, решения) — в `docs/`. Claude читает шапку этого файла при старте сессии (SessionStart hook). Сначала ищи здесь, потом парси код.

## wiki/ — структура (производное от кода)
- [data-model.md](data-model.md) — схема БД, ER, ассоциации
- [api.md](api.md) — endpoints, контракты, формат ответов
- [architecture.md](architecture.md) — компоненты, потоки данных, внешние зависимости
- [gaps.md](gaps.md) — структурные пробелы (что не задокументировано)
- [log.md](log.md) — журнал изменений wiki
- `models/`, `controllers/`, `services/` — по странице на сущность _(пусто)_

## docs/ — процесс (первичные нарративы)
- `docs/sessions/` — дневные логи работы (формат: `docs/sessions/TEMPLATE.md`)
- `docs/decisions/` — ADR (журнал решений)
- `docs/audits/` — incident/review аудиты (формат: `docs/audits/TEMPLATE.md`)
- `docs/operations/runbook-prod-deploy.md` — runbook деплоя
- `docs/gems.md` — переносимые уроки и приёмы

## Правила (кратко)
- Wiki **не** source of truth — source = код + миграции + ADR.
- Обновляй wiki в том же PR, что меняет код.
- Без авто-генерации через хуки и без QMD (до ~50 файлов). Подробности — [README.md](README.md).

## Статус проекта
{{PROJECT_NAME}} — {{DOMAIN}}. Стек: {{STACK}}. Структурные страницы заполняются по мере появления кода. Открытые вопросы — в логе текущей сессии (`docs/sessions/`).
