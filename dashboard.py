#!/usr/bin/env /tmp/akva_env2/bin/python3
"""
لوحة التحكم اليومية — محمد نعمة
تشوف كلشي بصفحة: الأرقام الجديدة، حالة آلة الحفر، آخر الفواتير، العمولات
"""

import os, csv, re, json, subprocess
from datetime import date, datetime

DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(DIR, "results.csv")
HISTORY = os.path.join(DIR, "calculator_history.json")
PID_FILE = os.path.join(DIR, "runner.pid")
LOG_FILE = os.path.join(DIR, "runner.log")
EXCEL = os.path.join(DIR, "contacts.xlsx")


def check_runner():
    if not os.path.exists(PID_FILE):
        return "❌ موقفة"
    try:
        with open(PID_FILE) as f:
            pid = int(f.read().strip())
        subprocess.run(["kill", "-0", str(pid)], capture_output=True, check=True)
        return f"✅ شغّالة (PID: {pid})"
    except:
        return "❌ موقفة"


def get_stats():
    stats = {"pages": 0, "phones": set(), "emails": set(), "by_country": {}}
    if not os.path.exists(RESULTS):
        return stats
    with open(RESULTS, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            stats["pages"] += 1
            country = r.get("country", "")
            for p in re.split(r",\s*", r.get("phones", "")):
                p = p.strip()
                if p and len(p) > 7:
                    stats["phones"].add(p)
                    stats["by_country"].setdefault(country, {"phones": set()})
                    stats["by_country"][country]["phones"].add(p)
            for e in re.split(r",\s*", r.get("emails", "")):
                e = e.strip().lower()
                if e and not any(s in e for s in ["example", "domain.com"]):
                    stats["emails"].add(e)
    return stats


def get_commission_total():
    if not os.path.exists(HISTORY):
        return 0, 0
    with open(HISTORY) as f:
        h = json.load(f)
    total = sum(hh["commission"] for hh in h)
    return len(h), total


def get_last_log():
    if not os.path.exists(LOG_FILE):
        return ""
    try:
        with open(LOG_FILE) as f:
            lines = f.readlines()
        return "".join(lines[-8:])
    except:
        return ""


def main():
    os.system("clear")
    runner = check_runner()
    stats = get_stats()
    inv_count, comm_total = get_commission_total()
    last_log = get_last_log()

    print("\033[1;34m" + "="*55 + "\033[0m")
    print(f"\033[1;33m  📊 لوحة التحكم — محمد نعمة | {date.today()}\033[0m")
    print("\033[1;34m" + "="*55 + "\033[0m")

    print(f"\n┌── آلة الحفر ──")
    print(f"│ {runner}")
    print(f"└────────────────")

    print(f"\n┌── الأرقام المجموعة ──")
    print(f"│ 📄 صفحات: {stats['pages']}")
    print(f"│ 📞 أرقام: {len(stats['phones'])}")
    print(f"│ ✉️ إيميلات: {len(stats['emails'])}")
    print(f"└────────────────")

    if stats["by_country"]:
        print(f"\n┌── حسب الدولة ──")
        for c, data in sorted(stats["by_country"].items()):
            n = len(data["phones"])
            bar = "█" * min(n // 2 + 1, 30)
            print(f"│ {c:10s} │ {n:3d} │ {bar}")
        print(f"└────────────────")

    print(f"\n┌── حسابات العمولات ──")
    print(f"│ 📝 {inv_count} عملية مسجلة")
    if comm_total > 0:
        print(f"│ 💰 \033[1;32m\${comm_total:,.2f}\033[0m إجمالي")
    print(f"└────────────────")

    print(f"\n┌── آخر تحديث ──")
    print(f"│ 📁 contacts.xlsx: {'موجود' if os.path.exists(EXCEL) else '⚠ مفقود'}")
    print(f"│ 📊 results.csv: {'موجود' if os.path.exists(RESULTS) else '⚠ مفقود'}")
    print(f"└────────────────")

    if last_log:
        print(f"\n┌── آخر السجل ──")
        for line in last_log.strip().split("\n"):
            print(f"│ {line.strip()}")
        print(f"└────────────────")

    print(f"\n{'─'*55}")
    print("  s: تشغيل/إيقاف آلة الحفر")
    print("  l: عرض السجل كامل")
    print("  q: خروج")
    print(f"{'─'*55}")

    choice = input("\n➜ ").strip().lower()
    if choice == "s":
        if "شغّالة" in runner:
            with open(PID_FILE) as f:
                os.system(f"kill {f.read().strip()}")
            print("🛑 أوقفت")
        else:
            os.system(f"bash '{DIR}/start.sh'")
    elif choice == "l":
        print("\n" + ("="*55))
        if last_log:
            print(last_log)
        else:
            print("لا يوجد سجل")
        input("Enter للعودة...")
    elif choice == "q":
        return
    else:
        main()


if __name__ == "__main__":
    main()
