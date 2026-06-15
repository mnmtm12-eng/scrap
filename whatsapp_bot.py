#!/usr/bin/env /tmp/akva_env2/bin/python3
"""
بوت واتساب — يولّد روابط wa.me جاهزة للأرقام اللي جمعناها
وتفتح المتصفح بنقرة
"""

import os, csv, re, webbrowser, random
from datetime import date

DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_CSV = os.path.join(DIR, "results.csv")

MESSAGES = [
    "السلام عليكم، معي عرض أبواب مصفحة تركية من مصنع TLT في قيصري. سعر مصنع + فحص جودة شخصي. مهتم؟",
    "السلام عليكم، أنا محمد من تركيا. عندي أبواب مصفحة بجودة أوروبية وأسعار منافسة. بسأل إذا كنت مهت بالتوريد؟",
    "السلام عليكم، عندي تشكيلة أبواب مصفحة تركية بأسعار الجملة. فحص شخصي على كل شحنة. للاستفسار واتساب.",
    "Hello, I represent TLT Steel Doors in Turkey. High quality, factory price. Interested in cooperation?",
    "Hi, this is Mohammad from Turkey. We manufacture steel security doors. Looking for partners in your region.",
]


def load_contacts():
    contacts = []
    if not os.path.exists(RESULTS_CSV):
        print("⚠ مافي results.csv — شغّل البحث أولاً")
        return contacts

    with open(RESULTS_CSV, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            phones = r.get("phones", "")
            name = r.get("name", "")
            country = r.get("country", "")
            for p in re.split(r",\s*", phones):
                p = p.strip()
                if p and len(p) > 7:
                    contacts.append({"phone": p, "name": name, "country": country})
    return contacts


def show_menu(contacts):
    while True:
        os.system("clear")
        print("\033[1;34m" + "="*50 + "\033[0m")
        print("\033[1;33m  📱 واتساب — روابط جاهزة\033[0m")
        print("\033[1;34m" + "="*50 + "\033[0m")
        print(f"\n  إجمالي الأرقام: {len(contacts)}")
        print("\n1. 🔗 عرض رابط واتساب عشوائي")
        print("2. 🌍 عرض حسب الدولة")
        print("3. 📋 عرض كل الأرقام بروابط")
        print("4. 📝 اختيار رسالة مخصصة")
        print("5. 💾 حفظ روابط في ملف HTML")
        print("0. ⬅ رجوع")

        choice = input("\nاختر: ").strip()
        if choice == "1":
            random_link(contacts)
        elif choice == "2":
            by_country(contacts)
        elif choice == "3":
            list_all(contacts)
        elif choice == "4":
            custom_message(contacts)
        elif choice == "5":
            save_html(contacts)
        elif choice == "0":
            break


def pick_msg():
    print("\n── الرسائل المتوفرة ──")
    for i, m in enumerate(MESSAGES, 1):
        print(f"{i}. {m[:60]}...")
    print(f"{len(MESSAGES)+1}. ✏️  رسالة مخصصة")
    choice = input("\nاختر: ").strip()
    if choice == str(len(MESSAGES)+1):
        return input("اكتب رسالتك: ").strip()
    try:
        return MESSAGES[int(choice)-1]
    except:
        return MESSAGES[0]


def wa_url(phone, msg):
    clean = re.sub(r'[^\d]', '', phone)
    if not clean.startswith("+"):
        clean = "+" + clean
    return f"https://wa.me/{clean}?text={msg[:500]}"


def random_link(contacts):
    c = random.choice(contacts)
    msg = pick_msg()
    url = wa_url(c["phone"], msg)
    print(f"\n  📍 {c['name'][:40]} | {c['country']}")
    print(f"  📞 {c['phone']}")
    print(f"  🔗 {url}")
    if input("\nفتح الرابط؟ (y/n): ").strip().lower() == "y":
        webbrowser.open(url)
    input("Enter للعودة...")


def by_country(contacts):
    countries = sorted(set(c["country"] for c in contacts))
    print("\n── الدول ──")
    for i, co in enumerate(countries, 1):
        cnt = sum(1 for c in contacts if c["country"] == co)
        print(f"  {i}. {co} ({cnt})")
    choice = input("\nاختر: ").strip()
    try:
        selected = countries[int(choice)-1]
    except:
        return
    subset = [c for c in contacts if c["country"] == selected]
    msg = pick_msg()
    print(f"\n── {selected} ({len(subset)}) ──")
    for c in subset:
        url = wa_url(c["phone"], msg)
        print(f"  {c['name'][:30]:30s} | {c['phone']:15s} | {url}")
    input("\nEnter للعودة...")


def list_all(contacts):
    msg = pick_msg()
    print(f"\n── كل الأرقام ──")
    for i, c in enumerate(contacts, 1):
        url = wa_url(c["phone"], msg)
        print(f"{i:3d}. {c['name'][:25]:25s} | {c['country']:10s} | {c['phone']:15s}")
    input("\nEnter للعودة...")


def custom_message(contacts):
    msg = input("اكتب رسالتك: ").strip()
    print(f"\n── أوّل 10 روابط ──")
    for i, c in enumerate(contacts[:10], 1):
        url = wa_url(c["phone"], msg)
        print(f"{i}. {url}")
    input("\nEnter للعودة...")


def save_html(contacts):
    msg = pick_msg()
    lines = ["<html dir='rtl'><head><meta charset='utf-8'><title>روابط واتساب</title>"]
    lines.append("<style>body{font-family:sans-serif;padding:20px;background:#f5f5f5}")
    lines.append("a{display:block;padding:10px;margin:5px 0;background:#25D366;color:white;")
    lines.append("text-decoration:none;border-radius:5px;font-size:14px}")
    lines.append("a:hover{background:#128C7E}</style></head><body>")
    lines.append(f"<h1>روابط واتساب — {date.today()}</h1>")
    lines.append(f"<p>{len(contacts)} جهة اتصال</p>")

    for c in contacts:
        url = wa_url(c["phone"], msg)
        lines.append(f"<a href='{url}' target='_blank'>{c['name'][:40]} | {c['country']} | {c['phone']}</a>")

    lines.append("</body></html>")

    fp = os.path.join(DIR, "whatsapp_links.html")
    with open(fp, "w") as f:
        f.write("\n".join(lines))
    print(f"\n  ✓ حفظ {len(contacts)} رابط في: {fp}")
    if input("فتح؟ (y/n): ").strip().lower() == "y":
        webbrowser.open(f"file://{fp}")
    input("Enter للعودة...")


def main():
    contacts = load_contacts()
    show_menu(contacts)


if __name__ == "__main__":
    main()
