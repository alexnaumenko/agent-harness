---
description: Пересобрать сводку статистики работы агента из летописи (docs/analytics/runs.md → dashboard.md)
---

Пересобери сводку статистики проекта:

```bash
python3 scripts/analytics/build_dashboard.py
```

Скрипт читает летопись `docs/analytics/runs.md`, считает итоги и перезаписывает `docs/analytics/dashboard.md`. Сам `dashboard.md` руками не правь. Если скрипта нет — проект ещё не развёрнут, предложи `/bootstrap`.
