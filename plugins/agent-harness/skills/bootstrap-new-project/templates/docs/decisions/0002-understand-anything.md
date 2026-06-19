# ADR-0002: Understand-Anything как слой структуры кода

**Дата:** {{DATE}}
**Статус:** Accepted
**Контекст:** дополняет [[0001-adopt-harness]].

## Контекст
Базе знаний нужен **структурный snapshot кода** (схема, маршруты, зависимости, ripple-эффект). Вести его вручную в `wiki/` — обуза, файлы устаревают. Есть зрелый инструмент [Understand-Anything](https://github.com/Egonex-AI/Understand-Anything) (Claude Code плагин): строит граф кода (Tree-sitter + LLM), даёт дашборд, поиск, diff-impact, онбординг.

## Решение
**Структурный слой отдаём Understand-Anything (UA), процесс и «почему» остаются у нас.**

Три слоя знания:
1. **UA** — машинная карта структуры (граф файлов/функций/зависимостей). Авто, регенерируемо.
2. **`wiki/`** — только структурные заметки, что UA не выводит из кода (бизнес-инварианты, договорённости).
3. **`docs/`** — процесс (сессии, ADR, audits, статистика).

## Сознательные решения (мирят с [[0001-adopt-harness]])
- **Без `--auto-update` хука.** `/understand` запускаем **вручную на гейтах** (как `/dashboard`). Это сохраняет правило «без авто-генерации через хуки»: пересборка осознанная, нет тихого дрейфа и платы за каждый коммит. У UA структура детерминированная (Tree-sitter) + инкрементальная.
- **Граф = производное представление, не source of truth** (как `wiki/`). Истина = код + миграции + ADR.

## Установка (компаньон)
```
/plugin marketplace add Egonex-AI/Understand-Anything
/plugin install understand-anything
/understand            # построить граф
/understand-dashboard  # открыть дашборд
```
В `.gitignore`: `.understand-anything/intermediate/` и `.understand-anything/diff-overlay.json`. Сам `knowledge-graph.json` можно коммитить, чтобы команда не пересобирала.

## Использование по этапам
- Требования/Дизайн: `/understand-chat`, `/understand-onboard`, `/understand-domain`.
- Код: `/understand-explain <файл>`.
- VERIFY: `/understand-diff` (ripple-эффект) → в вердикт ревью.

## Последствия
- `wiki/`-файлы `data-model/api/architecture` теперь **опциональны** — основную структуру покрывает UA; в `wiki/` держим только то, что код не выражает.
- UA — внешний плагин, не входит в `agent-harness`; рекомендуется к установке при bootstrap.
