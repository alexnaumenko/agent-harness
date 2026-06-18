<!--
Шаблон описания PR. Заполни применимые секции, остальные удали.
Тривиальный фикс (опечатка / dependency bump / format-only) — можно одной строкой
без секций. Для крупных изменений (новый feature, миграция БД, CI/CD) — заполнить всё.
-->

## Motivation

<!-- Зачем эта фича / какую боль решает / какое требование закрывает.
     1-3 предложения. Если есть session log или ADR — ссылка. -->


## Scope

<!-- Что в этом PR. Список файлов / модулей / тестов. -->


## Non-goals

<!-- Что НЕ в этом PR (защита от scope-drift при ревью).
     Например: «не трогаем CI», «не меняем схему БД», «не вводим новых зависимостей». -->


## Risks

<!-- Что может сломать. Особенно: prod, миграции, API breaking changes, совместимость. -->


## Test plan

<!-- Что прогнал локально + что должно пройти на CI. Адаптируй под стек. -->

- [ ] Линтер — clean
- [ ] Type-check — clean
- [ ] Тесты — passed, coverage ≥ gate
- [ ] Smoke (если задеты LLM / config / migration)
- [ ] Manual UI/flow check (если задет пользовательский флоу)
- [ ] **wiki/ обновлён в этом же PR** (если менялись схема / endpoints / архитектура)
- [ ] Multi-agent review запущен, если PR подпадает под политику (см. `CLAUDE.md` § «Multi-agent review policy»). CRITICAL адресованы, HIGH — fix либо явный accept.


## Связано

<!-- Linked issues / PRs / ADR / session logs / docs.
     Например: closes #N, refs docs/sessions/YYYY-MM/YYYY-MM-DD.md, ADR-0001. -->
