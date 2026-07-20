"""Fetch the public GitHub contribution calendar without using a token."""

import json
import re
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data/contributions.json"
USERNAME = "Aditya-tech-201"
URL = f"https://github.com/users/{USERNAME}/contributions"


def streaks(days):
    counts = {date.fromisoformat(day["date"]): day["count"] for day in days}
    longest = current = running = 0
    cursor, last = min(counts), max(counts)
    while cursor <= last:
        if counts.get(cursor, 0):
            running += 1
            longest = max(longest, running)
        else:
            running = 0
        cursor += timedelta(days=1)
    cursor = last
    while counts.get(cursor, 0):
        current += 1
        cursor -= timedelta(days=1)
    return current, longest


response = requests.get(URL, timeout=30, headers={"User-Agent": "profile-readme-generator"})
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")
days = []
for cell in soup.select("[data-date]"):
    day = cell.get("data-date")
    if not day or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day):
        continue
    text = cell.get("data-count") or cell.get("aria-label", "")
    match = re.search(r"(\d[\d,]*) contribution", text)
    count = int(match.group(1).replace(",", "")) if match else 0
    level = int(cell.get("data-level", "0") or 0)
    days.append({"date": day, "count": count, "level": min(max(level, 0), 4)})

if not days:
    sys.exit("GitHub returned no contribution cells; its public HTML may have changed.")
days.sort(key=lambda item: item["date"])
monthly = defaultdict(int)
for day in days:
    monthly[day["date"][:7]] += day["count"]
current, longest = streaks(days)
best = max(days, key=lambda item: item["count"])
payload = {"username": USERNAME, "updated_at": datetime.now().astimezone().isoformat(timespec="seconds"), "days": days, "stats": {"total": sum(day["count"] for day in days), "current_streak": current, "longest_streak": longest, "best_day": best, "monthly": dict(monthly)}}
OUTPUT.parent.mkdir(exist_ok=True)
OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
print(f"Fetched {len(days)} days for {USERNAME}: {OUTPUT}")
