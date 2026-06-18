---
title: Structural Gaps — {{PROJECT_NAME}}
type: gaps
source file path: wiki/gaps.md
created date: {{DATE}}
updated date: {{DATE}}
tags: [gaps, todo]
confidence level: high
---

**TL;DR:** Что в коде ещё **не задокументировано структурно** (модели/endpoints/сервисы без страницы). Процессные открытые вопросы — в логе текущей сессии, не здесь.

## Неудокументированные области кода
- _(кода нет — документировать пока нечего)_

## Когда появится код — кандидаты на страницу
- [ ] Каждая новая модель → `models/<name>.md` + строка в `data-model.md`
- [ ] Каждый нетривиальный endpoint → запись в `api.md` (тривиальный CRUD пропускаем)
- [ ] Каждый сервис/фоновый job → `services/<name>.md`
