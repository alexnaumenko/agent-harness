#!/usr/bin/env python3
"""Считает сводку (dashboard.md) из летописи (runs.md).

Детерминированно: просто складывает числа из markdown-таблицы. Без LLM, без сети.
Запуск:  python3 scripts/analytics/build_dashboard.py
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "docs" / "analytics" / "runs.md"
DASHBOARD = ROOT / "docs" / "analytics" / "dashboard.md"

COLUMNS = [
    "дата", "фича", "этап", "статус", "крит", "важн", "мелк",
    "покрытие", "время_мин", "выпущено", "заметка",
]


def parse_rows(text: str) -> list[dict[str, str]]:
    """Извлекает строки данных из первой markdown-таблицы с нужными колонками."""
    rows: list[dict[str, str]] = []
    in_table = False
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            in_table = False
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        # шапка таблицы
        if cells and cells[0] == COLUMNS[0]:
            in_table = True
            continue
        # разделитель |---|---|
        if in_table and set("".join(cells)) <= set("-: "):
            continue
        if in_table and len(cells) >= len(COLUMNS):
            rows.append(dict(zip(COLUMNS, cells)))
    return rows


def to_int(val: str):
    val = (val or "").strip().rstrip("%")
    try:
        return int(val)
    except ValueError:
        try:
            return int(float(val))
        except ValueError:
            return None


def build(rows: list[dict[str, str]], examples: int = 0) -> str:
    total = len(rows)
    reviewed = [r for r in rows if r["статус"] in ("одобрено", "правки")]
    approved = [r for r in reviewed if r["статус"] == "одобрено"]
    approve_rate = round(100 * len(approved) / len(reviewed)) if reviewed else None

    crit = sum(to_int(r["крит"]) or 0 for r in rows)
    imp = sum(to_int(r["важн"]) or 0 for r in rows)
    minor = sum(to_int(r["мелк"]) or 0 for r in rows)
    crit_density = round(crit / len(reviewed), 2) if reviewed else None

    released = sum(1 for r in rows if r["выпущено"].lower() == "да")

    coverages = [to_int(r["покрытие"]) for r in rows if to_int(r["покрытие"]) is not None]
    coverage_last = coverages[-1] if coverages else None

    # разбивка по этапам: число строк + среднее время
    phases: dict[str, list[int]] = {}
    phase_counts: dict[str, int] = {}
    for r in rows:
        ph = r["этап"] or "—"
        phase_counts[ph] = phase_counts.get(ph, 0) + 1
        t = to_int(r["время_мин"])
        if t is not None:
            phases.setdefault(ph, []).append(t)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    def fmt(v, suffix=""):
        return f"{v}{suffix}" if v is not None else "—"

    lines = [
        "<!-- GENERATED скриптом scripts/analytics/build_dashboard.py — руками не править -->",
        "# Сводка работы агента",
        "",
        f"_Посчитано: {now}. Источник: `runs.md` ({total} записей; пропущено примеров: {examples})._",
        "",
        "## Главное",
        "",
        "| Показатель | Значение |",
        "|---|---|",
        f"| Всего записей | {total} |",
        f"| Прошло без правок с первого раза | {fmt(approve_rate, '%')} ({len(approved)}/{len(reviewed)}) |",
        f"| Критичных замечаний на задачу | {fmt(crit_density)} |",
        f"| Замечаний всего (крит/важн/мелк) | {crit} / {imp} / {minor} |",
        f"| Текущее покрытие тестами | {fmt(coverage_last, '%')} |",
        f"| Выпущено в бой | {released} |",
        "",
        "## По этапам",
        "",
        "| Этап | Записей | Среднее время, мин |",
        "|---|---|---|",
    ]
    for ph in ["требования", "дизайн", "код", "тесты", "релиз", "бой"]:
        cnt = phase_counts.get(ph, 0)
        times = phases.get(ph, [])
        avg = round(sum(times) / len(times)) if times else None
        lines.append(f"| {ph} | {cnt} | {fmt(avg)} |")
    # этапы, не попавшие в стандартный список
    for ph, cnt in phase_counts.items():
        if ph not in ["требования", "дизайн", "код", "тесты", "релиз", "бой"]:
            times = phases.get(ph, [])
            avg = round(sum(times) / len(times)) if times else None
            lines.append(f"| {ph} | {cnt} | {fmt(avg)} |")

    lines += [
        "",
        "---",
        "_Как обновить: `python3 scripts/analytics/build_dashboard.py`._",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    if not RUNS.exists():
        print(f"Не найден файл летописи: {RUNS}", file=sys.stderr)
        return 1
    all_rows = parse_rows(RUNS.read_text(encoding="utf-8"))
    # Строки-примеры (фича начинается с "demo-") в статистику не идут.
    rows = [r for r in all_rows if not r["фича"].lower().startswith("demo-")]
    examples = len(all_rows) - len(rows)
    DASHBOARD.write_text(build(rows, examples), encoding="utf-8")
    print(f"Сводка пересобрана: {DASHBOARD} ({len(rows)} записей, примеров пропущено: {examples})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
