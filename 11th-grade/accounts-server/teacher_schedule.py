"""Class schedules for the playground: packs of questions, each with a deadline in Tehran time,
and Jalali (Persian) dates for display.

A question counts for a student's score only if the student's first pass of it came on or before
the deadline of the pack that holds the question for the student's class. After that the question
stays open for practice, but without a score.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

TEHRAN = ZoneInfo("Asia/Tehran")
JALALI_MONTHS = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
                 "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
WEEKDAYS = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه", "شنبه", "یکشنبه"]  # Monday = 0
EN_WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
EN_MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
             "October", "November", "December"]
GREGORIAN_MONTH_DAYS = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]


def gregorian_to_jalali(day: date) -> tuple[int, int, int]:
    """Converts a Gregorian date to (year, month, day) of the Jalali calendar."""
    gy, gm, gd = day.year, day.month, day.day
    gy2 = gy + 1 if gm > 2 else gy
    days = (355666 + 365 * gy + (gy2 + 3) // 4 - (gy2 + 99) // 100 + (gy2 + 399) // 400
            + gd + GREGORIAN_MONTH_DAYS[gm - 1])
    jy = -1595 + 33 * (days // 12053)
    days %= 12053
    jy += 4 * (days // 1461)
    days %= 1461
    if days > 365:
        jy += (days - 1) // 365
        days = (days - 1) % 365
    if days < 186:
        jm, jd = 1 + days // 31, 1 + days % 31
    else:
        jm, jd = 7 + (days - 186) // 30, 1 + (days - 186) % 30
    return jy, jm, jd


def to_tehran(moment: datetime) -> datetime:
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    return moment.astimezone(TEHRAN)


def jalali_text(moment: datetime | None) -> str:
    """Persian text such as 'شنبه ۳۰ آبان ۱۴۰۵ ساعت ۲۲:۰۰' (Tehran time)."""
    if moment is None:
        return "—"
    local = to_tehran(moment)
    jy, jm, jd = gregorian_to_jalali(local.date())
    text = f"{WEEKDAYS[local.weekday()]} {jd} {JALALI_MONTHS[jm - 1]} {jy} ساعت {local:%H:%M}"
    return text.translate(str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹"))


def english_text(moment: datetime | None) -> str:
    """English text such as 'Saturday 21 November 2026, 22:00 (Tehran time)'."""
    if moment is None:
        return "—"
    local = to_tehran(moment)
    return (f"{EN_WEEKDAYS[local.weekday()]} {local.day} {EN_MONTHS[local.month - 1]} {local.year}, "
            f"{local:%H:%M} (Tehran time)")


def jalali_plain(moment: datetime | None) -> str:
    """ASCII form for spreadsheets: 1405/08/30 22:00 (Tehran time)."""
    if moment is None:
        return ""
    local = to_tehran(moment)
    jy, jm, jd = gregorian_to_jalali(local.date())
    return f"{jy:04d}/{jm:02d}/{jd:02d} {local:%H:%M}"


def parse_tehran(text: str) -> datetime:
    """'2026-11-16T22:00' (Tehran local time) -> UTC datetime."""
    local = datetime.strptime(text, "%Y-%m-%dT%H:%M").replace(tzinfo=TEHRAN)
    return local.astimezone(timezone.utc)


def stamp_utc(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class Pack:
    cls: str
    id: str
    title: str
    until: datetime  # UTC
    markdown: str
    problems: list[str] = field(default_factory=list)
    en: dict = field(default_factory=dict)  # optional English title and markdown


class Schedule:
    def __init__(self, data: dict, known_problems: set[str]):
        self.packs: dict[str, list[Pack]] = {}
        self._by_question: dict[tuple[str, str], Pack] = {}
        for cls, body in data.get("classes", {}).items():
            packs = []
            for item in body.get("packs", []):
                pack = Pack(cls=cls, id=item["id"], title=item["title"],
                            until=parse_tehran(item["until"]), markdown=item.get("markdown", ""),
                            problems=list(item["problems"]), en=dict(item.get("en") or {}))
                for pid in pack.problems:
                    if pid not in known_problems:
                        raise ValueError(f"schedule: unknown question {pid}")
                    if (cls, pid) in self._by_question:
                        raise ValueError(f"schedule: {pid} is in two packs for class {cls}")
                    self._by_question[(cls, pid)] = pack
                packs.append(pack)
            self.packs[cls] = sorted(packs, key=lambda p: p.until)

    @classmethod
    def load(cls, path: Path, known_problems: set[str]) -> "Schedule":
        if not path.exists():
            return cls({"classes": {}}, known_problems)
        return cls(json.loads(path.read_text(encoding="utf-8")), known_problems)

    def pack_for(self, class_code: str | None, problem_id: str) -> Pack | None:
        return self._by_question.get((class_code or "", problem_id))

    def deadline(self, class_code: str | None, problem_id: str) -> datetime | None:
        pack = self.pack_for(class_code, problem_id)
        return pack.until if pack else None

    def is_scored(self, class_code: str | None, problem_id: str, moment: datetime) -> bool:
        pack = self.pack_for(class_code, problem_id)
        return pack is not None and moment <= pack.until

    def public_packs(self, class_code: str | None, number_of: dict[str, dict]) -> list[dict]:
        out = []
        for pack in self.packs.get(class_code or "", []):
            out.append({
                "id": pack.id,
                "title": pack.title,
                "until": stamp_utc(pack.until),
                "untilText": jalali_text(pack.until),
                "markdown": pack.markdown,
                "en": {"title": pack.en.get("title", pack.title), "markdown": pack.en.get("markdown", pack.markdown),
                       "untilText": english_text(pack.until)},
                "questions": [
                    {"id": pid, "number": number_of.get(pid, {}).get("number", 0),
                     "title": number_of.get(pid, {}).get("title", "")}
                    for pid in pack.problems
                ],
            })
        return out

    def classes(self) -> list[str]:
        return sorted(self.packs)
