# Agent Harness

Устанавливаемая **обвязка для full-cycle dev-агента** в Claude Code: база знаний + статистика работы + дисциплина процесса от требований до production. Всё — в обычных markdown-файлах, рядом с кодом, без баз и сторонних сервисов.

Это Claude Code marketplace с одним плагином (`agent-harness`); со временем сюда можно добавлять другие.

## Что разворачивает

Команда `/bootstrap` спрашивает стек/домен/деплой/базу и создаёт в проекте:

- **`wiki/`** — структурное знание о коде (схема БД, маршруты, архитектура).
- **`docs/`** — процесс: сессии, ADR (решения), audits (разборы поломок), runbook.
- **`docs/analytics/`** — статистика «летопись + сводка»: факты дописываются в `runs.md`, итоги считает скрипт в `dashboard.md`.
- **`CODE-REVIEW.md`** — чек-лист проверки качества (растёт из разборов поломок).
- **6-этапный жизненный цикл** в `CLAUDE.md`: требования → дизайн → код → тесты → релиз → бой, с проверкой на выходе каждого этапа.
- **`.claude/`** — SessionStart hook (подгружает шапку wiki при старте сессии).
- **`.github/`** — PR-шаблон + CI-шаблон (dev auto / prod manual).

Методология: insight-bot-mvp + статья [vc.ru/ai/2869178](https://vc.ru/ai/2869178-sozdanie-samoobnovlyayushcheysya-bazy-znaniy), с сознательными отклонениями (без авто-генерации через хуки, без QMD, аналитика в markdown, сводку считает скрипт а не LLM).

## Установка

```text
/plugin marketplace add alexnaumenko/agent-harness
/plugin install agent-harness
```

## Использование

```text
/bootstrap     — развернуть обвязку в текущем проекте
/dashboard     — пересобрать сводку статистики
```

Или skill `bootstrap-new-project` вызывается автоматически, когда говоришь «новый проект» / «разверни обвязку».

## Команды

| Команда | Что делает |
|---|---|
| `/agent-harness:bootstrap` | Развернуть базу знаний + обвязку |
| `/agent-harness:dashboard` | Пересчитать `docs/analytics/dashboard.md` из летописи |

## Структура репозитория

```
agent-harness/
├── .claude-plugin/marketplace.json     — витрина (перечисляет плагины)
└── plugins/agent-harness/
    ├── .claude-plugin/plugin.json
    ├── skills/bootstrap-new-project/   — SKILL.md + BOOTSTRAP.md + templates/
    └── commands/                       — /bootstrap, /dashboard
```

## Лицензия
MIT — см. [LICENSE](LICENSE).
