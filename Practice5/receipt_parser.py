with open("Practice5/raw.txt", "r", encoding="utf-8-sig") as f:
    text = f.read()

import re
#all prices
patt1 = r"x\s(\d[\d\s]*,\d{2})"
prices = re.findall(patt1, text)
print("all prices",prices)

#all product names
patt2=r"\d+\.\n([^\d\n]+)"
names=re.findall(patt2,text)
print("all names",names)

#total amount
patt_total = r"ИТОГО:\n([\d\s]+,\d{2})"
itogo = re.search(patt_total, text)

if itogo:
    print("Итог", itogo.group(1))

#Extract date and time information
patt4=r"Время:\s*(.+)\n"
date=re.search(patt4,text)
print("дата и время:", date.group(1))

#Find payment method
pay = r"(Банковская карта|Наличные)"
pay1 = re.search(pay, text)
if pay1:
    print("метод оплаты:", pay1.group(1))
else:
    print("метод оплаты: Неизвестно")

#Create a structured output (JSON or formatted text)

print("\n" + "="*40)
print("обзор чека")
print("="*40)
for name, price in zip(names, prices):
    print(f"{name.strip()} — Цена за штуку: {price}")
print("-"*40)
print(f"Общая сумма: {itogo.group(1)}")
print(f"Дата и время: {date.group(1)}")
if pay1:
    print(f"Метод оплаты: {pay1.group(1)}")
else:
    print("Метод оплаты: Неизвестно")
print("="*45)