#!/usr/bin/env /tmp/akva_env2/bin/python3
"""
فاتورة احترافية PDF — محمد نعمة
للأبواب المصفحة التركية (عربي/إنجليزي/تركي)
"""

import os
from datetime import datetime

DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(DIR, "invoices")
os.makedirs(OUT_DIR, exist_ok=True)


def generate_invoice():
    from fpdf import FPDF

    inv_num = datetime.now().strftime("INV-%Y%m%d-%H%M%S")

    print("\n" + "="*50)
    print("  📄 منشئ الفواتير")
    print("="*50)

    client = input("اسم الزبون: ").strip()
    country = input("الدولة: ").strip()
    phone = input("رقم الهاتف: ").strip()

    items = []
    while True:
        desc = input("صنف (أو Enter للانتهاء): ").strip()
        if not desc:
            break
        qty = int(input("  الكمية: ").strip() or "1")
        uprice = float(input("  سعر الوحدة ($): ").strip() or "0")
        items.append((desc, qty, uprice))

    if not items:
        print("ما في أصناف")
        return

    currency = "USD"
    payment = input("طريقة الدفع (تحويل/نقد/LC): ").strip() or "تحويل بنكي"
    notes = input("ملاحظات: ").strip()

    total = sum(q * p for _, q, p in items)

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_rtl(True)

    # Colors
    blue = (31, 78, 121)
    gold = (212, 175, 55)
    gray = (240, 240, 240)

    # Header background
    pdf.set_fill_color(*blue)
    pdf.rect(0, 0, 210, 50, "F")

    # Logo area
    pdf.set_xy(10, 8)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 24)
    pdf.cell(190, 10, "INVOICE", align="C")
    pdf.ln(14)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(190, 8, "Steel Security Doors - Turkey", align="C")
    pdf.ln(8)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(190, 6, "Mohammad Nema | Kayseri, Turkey", align="C")

    # Invoice details
    pdf.set_text_color(0, 0, 0)
    pdf.set_y(58)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(190, 8, f"Invoice #{inv_num}", align="R")
    pdf.ln(6)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(190, 6, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", align="R")

    # Client info box
    pdf.set_y(75)
    pdf.set_fill_color(*gray)
    pdf.rect(10, 75, 190, 30, "F")
    pdf.set_xy(15, 78)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(180, 6, f"Bill To:")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(15, 85)
    pdf.cell(180, 6, f"{client}")
    pdf.set_xy(15, 92)
    pdf.cell(180, 6, f"{country} | {phone}")

    # Table header
    y = 115
    pdf.set_fill_color(*blue)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_xy(10, y)
    pdf.cell(90, 8, "  Description", border=1, fill=True)
    pdf.cell(30, 8, "Qty", border=1, fill=True, align="C")
    pdf.cell(35, 8, "Unit Price", border=1, fill=True, align="C")
    pdf.cell(35, 8, "Total", border=1, fill=True, align="C")

    # Items
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "", 10)
    y += 8
    for i, (desc, qty, uprice) in enumerate(items):
        if i % 2 == 0:
            pdf.set_fill_color(245, 245, 245)
        else:
            pdf.set_fill_color(255, 255, 255)
        line_total = qty * uprice
        pdf.set_xy(10, y)
        pdf.cell(90, 8, f"  {desc}", border=1, fill=True)
        pdf.cell(30, 8, str(qty), border=1, fill=True, align="C")
        pdf.cell(35, 8, f"${uprice:,.2f}", border=1, fill=True, align="C")
        pdf.cell(35, 8, f"${line_total:,.2f}", border=1, fill=True, align="C")
        y += 8

    # Total
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_fill_color(*gold)
    pdf.set_text_color(0, 0, 0)
    pdf.set_xy(10, y)
    pdf.cell(155, 10, "  TOTAL", border=1, fill=True)
    pdf.cell(35, 10, f"${total:,.2f}", border=1, fill=True, align="C")

    # Payment & notes
    y += 15
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_xy(10, y)
    pdf.cell(190, 6, f"Payment Method: {payment}")
    y += 8
    if notes:
        pdf.set_font("Helvetica", "", 9)
        pdf.set_xy(10, y)
        pdf.multi_cell(190, 5, f"Notes: {notes}")
        y += 15

    # Footer
    pdf.set_y(260)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(190, 5, "Mohammad Nema | Kayseri, Turkey | Phone: ________ | Email: ________", align="C")
    pdf.ln(4)
    pdf.cell(190, 5, "Thank you for your business!", align="C")

    filepath = os.path.join(OUT_DIR, f"{inv_num}.pdf")
    pdf.output(filepath)
    print(f"\n  ✓ الفاتورة: {filepath}")


def main():
    while True:
        generate_invoice()
        again = input("\nفاتورة جديدة؟ (y/n): ").strip().lower()
        if again != "y":
            break


if __name__ == "__main__":
    main()
