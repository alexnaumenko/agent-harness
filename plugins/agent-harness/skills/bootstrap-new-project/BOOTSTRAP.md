# BOOTSTRAP — процедура развёртывания (исполняет агент по шагам)

Цель: развернуть базу знаний + обвязку в текущей папке проекта из шаблонов skill'а.

Путь к шаблонам (работает и как установленный плагин, и как локальный skill):
- как плагин: `${CLAUDE_PLUGIN_ROOT}/skills/bootstrap-new-project/templates`
- как локальный skill (fallback): `$HOME/.claude/skills/bootstrap-new-project/templates`
Целевая папка: текущая рабочая директория проекта.

---

## Шаг 1. Спросить owner'а (4 вопроса)
Задай (можно через AskUserQuestion, можно текстом):
1. **Стек** — Python / TypeScript / Go / Rust / другое.
2. **Домен** — одно предложение «что это за проект».
3. **Деплой** — Docker compose / Cloud Run / k8s / нет деплоя.
4. **База** — PostgreSQL / SQLite / нет.

Имя проекта (`PROJECT_NAME`) — по умолчанию имя текущей папки (`basename "$PWD"`), уточни при сомнении.

## Шаг 2. Проверить, что не затираем существующее
```bash
ls CLAUDE.md wiki docs CODE-REVIEW.md 2>/dev/null
```
Если что-то уже есть — НЕ перезаписывать молча. Спросить owner'а (слить/пропустить/перезаписать).

## Шаг 3. Скопировать шаблоны в проект
```bash
# Найти шаблоны: сперва путь плагина, иначе локальный skill
TEMPLATES="${CLAUDE_PLUGIN_ROOT}/skills/bootstrap-new-project/templates"
[ -d "$TEMPLATES" ] || TEMPLATES="$HOME/.claude/skills/bootstrap-new-project/templates"
cp -R "$TEMPLATES/." .
```
Это принесёт: `CLAUDE.md`, `CODE-REVIEW.md`, `wiki/`, `docs/`, `scripts/`, `.github/`, `.claude/`.

## Шаг 4. Подставить простые плейсхолдеры (`{{PROJECT_NAME}}`, `{{DATE}}`)
```bash
NAME="$(basename "$PWD")"           # или имя, согласованное с owner'ом
TODAY="$(date +%Y-%m-%d)"
find . -name "*.md" -not -path './.git/*' -type f \
  -exec perl -i -pe "s/\Q{{PROJECT_NAME}}\E/$NAME/g; s/\Q{{DATE}}\E/$TODAY/g" {} +
```

## Шаг 5. Заполнить смысловые плейсхолдеры из ответов owner'а
В этих файлах замени плейсхолдеры на ответы (через Edit, текстом owner'а):
- `CLAUDE.md`: `{{DOMAIN}}` (домен), `{{STACK}}` (стек + ключевые библиотеки), `{{COMMANDS}}` (install / lint / type-check / test / run под стек).
- `wiki/index.md`: `{{DOMAIN}}`, `{{STACK}}`.

Также обнови в `CLAUDE.md` секцию «Tech stack» и `CODE-REVIEW.md`/`runbook` под выбранные деплой и базу (например, добавь backup БД в runbook, если база есть).

## Шаг 6. Применить language-specific правила (если есть)
Если существует `~/.claude/rules/<стек>/` — упомяни owner'у, что они применяются (линтер/тайпчек/тесты под язык). Подставь конкретные команды в `{{COMMANDS}}` и в `.github/workflows/deploy.yml.template`.

## Шаг 7. Завести первый session-log за сегодня
Создай `docs/sessions/$(date +%Y-%m)/$(date +%Y-%m-%d).md` по шаблону `docs/sessions/TEMPLATE.md`, цель: «Проект развёрнут через /bootstrap-new-project». Удали `{{...}}` из шаблона.

## Шаг 8. Сгенерировать сводку статистики
```bash
python3 scripts/analytics/build_dashboard.py
```
(в `runs.md` лежат только demo-образцы → сводка будет пустой по реальным данным — это норма.)

## Шаг 9. Сделать хук исполняемым
```bash
chmod +x .claude/hooks/session-start.sh scripts/analytics/build_dashboard.py
```

## Шаг 10. Доложить owner'у + предложить первый коммит
Сообщи, что развёрнуто (список папок), и предложи:
```bash
git init 2>/dev/null; git add -A
git commit -m "chore: bootstrap knowledge base + agent harness"
```
Не коммить без явного согласия owner'а.

---

## Проверка (что должно получиться)
- `ls CLAUDE.md CODE-REVIEW.md` — оба есть, без `{{плейсхолдеров}}`.
- `wiki/` и `docs/` на месте; `docs/analytics/dashboard.md` сгенерирован.
- `grep -rn "{{" .` по `*.md` — ничего не находит (все плейсхолдеры заменены).
- SessionStart hook работает: `CLAUDE_PROJECT_DIR="$PWD" bash .claude/hooks/session-start.sh`.
