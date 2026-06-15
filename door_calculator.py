#!/usr/bin/env /tmp/akva_env2/bin/python3
"""
حاسبة الأبواب — محمد نعمة
تحسب سعر الباب، العمولة، سعر الزبون، وأرباح الكونتنير
"""

import os, json
from datetime import date

DIR = os.path.dirname(os.path.abspath(__file__))
HIST = os.path.join(DIR, "calculator_history.json")

# Commission rates
RATES = {
    "قياسي": {"min_cm": 0, "max_cm": 100, "rate": 5},
    "120 سم": {"min_cm": 101, "max_cm": 120, "rate": 6},
    "140 سم": {"min_cm": 121, "max_cm": 140, "rate": 8},
    "160 سم": {"min_cm": 141, "max_cm": 200, "rate": 10},
}

DOOR_TYPES = {
    "1": "قياسي",
    "2": "120 سم",
    "3": "140 سم",
    "4": "160 سم",
    "5": "خاص (عراق - بالمتر)",
}

COUNTRIES = {
    "1": ("مصر", 167, 850),
    "2": ("الأردن", 120, 850),
    "3": ("العراق", 100, 850),
    "4": ("ليبيا", 100, 950),
    "5": ("المغرب", 100, 950),
    "6": ("أخرى", 100, 1000),
}


def clear():
    os.system('clear')


def show_header():
    print("\033[1;34m" + "="*55 + "\033[0m")
    print("\033[1;33m  🔩 حاسبة الأبواب — محمد نعمة\033[0m")
    print("\033[1;34m" + "="*55 + "\033[0m")


def calc_door():
    clear()
    show_header()
    print("\n── أبعاد الباب ──")
    for k, v in DOOR_TYPES.items():
        print(f"  {k}. {v}")
    
    choice = input("\nاختر نوع الباب (1-5): ").strip()
    while choice not in DOOR_TYPES:
        choice = input("رقم غير صحيح، حاول مرة: ").strip()
    
    qty = int(input("الكمية (عدد الأبواب): ").strip() or "1")
    
    if choice == "5":
        w = float(input("العرض (متر): ").strip())
        h = float(input("الارتفاع (متر): ").strip())
        area = w * h
        unit = area * 3  # $3/m²
        rate = area * 3
        desc = f"{w}×{h}m = {area:.2f}m² × $3"
    else:
        door_type = DOOR_TYPES[choice]
        r = RATES[door_type]
        unit = r["rate"]
        rate = r["rate"]
        desc = f"{door_type} — ${rate}/باب"
    
    commission = unit * qty
    
    print(f"\n\033[1;36m{'─'*40}\033[0m")
    print(f"  {desc}")
    print(f"  الكمية: {qty}")
    print(f"  \033[1;32mعمولتك: ${commission:,.2f}\033[0m")
    print(f"\033[1;36m{'─'*40}\033[0m")
    
    factory_price = float(input("\nسعر الباب من المصنع (TL أو $): ").strip() or "0")
    currency = input("عملة المصنع (TL/$): ").strip().upper() or "TL"
    if currency == "TL":
        rate_try = float(input("سعر الصرف (TL/$): ").strip() or "40")
        factory_usd = factory_price / rate_try
    else:
        factory_usd = factory_price
    
    total_factory = factory_usd * qty
    sell_price = factory_usd + unit
    total_sell = sell_price * qty
    
    print(f"\n\033[1;33m── سعر البيع للزبون ──\033[0m")
    print(f"  سعر الباب: ${sell_price:,.2f}")
    print(f"  إجمالي للزبون: ${total_sell:,.2f}")
    print(f"  \${\033[1;32m{commission:,.2f}\033[0m} عمولتك")
    
    save = input("\nحفظ؟ (y/n): ").strip().lower()
    if save == 'y':
        history = []
        if os.path.exists(HIST):
            with open(HIST) as f:
                history = json.load(f)
        history.append({
            "date": str(date.today()),
            "desc": desc,
            "qty": qty,
            "commission": commission,
            "total_sell": total_sell,
            "factory_usd": factory_usd,
        })
        with open(HIST, "w") as f:
            json.dump(history, f, indent=2)
        print("  ✓ حفظت!")
    
    input("\nاضغط Enter للعودة...")


def calc_container():
    clear()
    show_header()
    print("\n── حاسبة الكونتنير ──")
    for k, v in COUNTRIES.items():
        print(f"  {k}. {v[0]} ({v[1]} باب/كونتنير)")
    
    choice = input("\nاختر الدولة: ").strip()
    while choice not in COUNTRIES:
        choice = input("رقم غير صحيح: ").strip()
    
    cname, doors, container_cost = COUNTRIES[choice]
    
    print(f"\n── كونتنير {cname} ──")
    print(f"  عدد الأبواب: {doors}")
    
    avg_price = float(input("متوسط سعر الباب (عمولتك بال$): ").strip() or "5")
    container_price = float(input("سعر الكونتنير (شحن + مصنع بال$): ").strip() or "0")
    
    commission_per_container = avg_price * doors
    sell_total = container_price + commission_per_container
    containers = int(input("عدد الكونتنيرات: ").strip() or "1")
    
    print(f"\n\033[1;36m{'─'*40}\033[0m")
    print(f"  الدولة: {cname}")
    print(f"  ألواح/كونتنير: {doors}")
    print(f"  عمولة/كونتنير: ${commission_per_container:,.2f}")
    print(f"  كل الكونتنيرات ({containers}): \033[1;32m${commission_per_container*containers:,.2f}\033[0m")
    print(f"\033[1;36m{'─'*40}\033[0m")
    
    input("\nاضغط Enter للعودة...")


def show_history():
    clear()
    show_header()
    print("\n── سجل الحسابات ──")
    if not os.path.exists(HIST):
        print("  لا يوجد سجل بعد")
        input("\nاضغط Enter...")
        return
    
    with open(HIST) as f:
        history = json.load(f)
    
    total = 0
    for i, h in enumerate(history[-20:], 1):
        total += h["commission"]
        print(f"  {i}. {h['date']} | {h['desc']:25s} | {h['qty']} باب | \033[1;32m\${h['commission']:>7,.2f}\033[0m")
    
    print(f"\n  \033[1;33mالمجموع: \${total:,.2f}\033[0m")
    input("\nاضغط Enter...")


def main():
    while True:
        clear()
        show_header()
        print("\n1. 🚪 حساب باب واحد")
        print("2. 📦 حساب كونتنير كامل")
        print("3. 📊 سجل العمولات")
        print("0. 🔙 خروج")
        
        choice = input("\nاختر: ").strip()
        if choice == "1":
            calc_door()
        elif choice == "2":
            calc_container()
        elif choice == "3":
            show_history()
        elif choice == "0":
            break


if __name__ == "__main__":
    main()
