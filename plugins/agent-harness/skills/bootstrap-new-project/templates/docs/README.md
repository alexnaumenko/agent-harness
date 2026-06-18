# docs/ — процессное знание проекта {{PROJECT_NAME}}

Здесь живут **первичные нарративы**: как мы пришли к решениям, что делали, что ломалось. В отличие от `wiki/` (snapshot структуры кода), `docs/` — это **история и обоснования**, source of truth для «почему».

| Слой | Что | Когда писать |
|------|-----|--------------|
| `wiki/` | структура (схема, маршруты, архитектура) | в том же PR, что меняет код |
| `docs/` | процесс (сессии, решения, инциденты, runbook) | по ходу работы |

## Структура

- **`sessions/YYYY-MM/YYYY-MM-DD.md`** — дневной лог работы. Формат: [`sessions/TEMPLATE.md`](sessions/TEMPLATE.md). Один файл на день, папка на месяц.
- **`decisions/`** — ADR (Architecture Decision Records): что решили, почему, альтернативы. Нумеруются `NNNN-kebab-title.md`.
- **`audits/`** — incident-аудиты и review. Формат: [`audits/TEMPLATE.md`](audits/TEMPLATE.md).
- **`operations/runbook-prod-deploy.md`** — пошаговый runbook деплоя + откат.
- **`analytics/`** — статистика работы агента (летопись `runs.md` + сводка `dashboard.md` + `incidents.md`). См. `analytics/README.md`.
- **`reviews/review-format.md`** — формат вердикта проверяющего на этапе тестов.
- **`gems.md`** — переносимые уроки и переиспользуемые приёмы (растёт со временем).

## Правила
1. **Session log обязателен** — см. `CLAUDE.md` § «MANDATORY: Session logging».
2. Значимое решение → ADR в `decisions/` + ссылка из session log.
3. Инцидент → аудит в `audits/` сразу после mitigation, пока контекст свежий.
4. Уроки из сессий и инцидентов периодически конденсируются в `gems.md`.
