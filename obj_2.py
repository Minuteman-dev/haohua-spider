import requests
import pandas as pd
from bs4 import BeautifulSoup
import sqlite3

main_url = "https://www.haohua.com/"

resp = requests.get(main_url, headers={"User-Agent": "Mozilla/5.0"})
resp.encoding = "utf-8"
soup = BeautifulSoup(resp.text,"html.parser")

data_1 = []
data_2 = []

dd_a = soup.find_all("dd")
dd_b = dd_a[8:]

for a in dd_b:
    price_all = a.find("p",class_ = "price").get_text(strip=True)
    price_front = price_all.split("直降")[0].strip()
    price_back = price_all.split("直降")[1].strip()
    data_1.append({
        "类别" : "限时抢购",
        "名称" : a.find("h5").get_text(strip=True),
        "价格" : price_front,
        "直降" : price_back
    })



li_a = soup.find_all("li")
tem_ = []
for li in li_a:
    if li.find("label") == None:
        continue
    else:
        tem_.append(li)


type_ = []

block_tem = soup.find_all("h5")
for x in block_tem:
    t = x.find_next_sibling("p",string=lambda s: s and "进入专区" in s)
    if t:
        type_.append(x.get_text(strip=True))


flag = 0

for b in tem_:
    mix_tem = b.find("p",class_ = "price").get_text(strip=True)
    price_tem = mix_tem.split("原价")[0].strip()
    ori_tem = mix_tem.split("原价")[1].split("人气")[0].strip()
    pop_tem = mix_tem.split("人气")[1].strip()
    data_2.append({
        "类别" : type_[flag//6],
        "名称" : b.find("h5").get_text(strip=True),
        "价格" : price_tem,
        "原价" : ori_tem,
        "人气" : pop_tem
    })
    flag += 1

with pd.ExcelWriter("好花网首页商品内容.xlsx") as writer:
    pd.DataFrame(data_1).to_excel(writer, sheet_name="限时直降部分", index=False)
    pd.DataFrame(data_2).to_excel(writer, sheet_name="专区部分", index=False)

con = sqlite3.connect('data.db')

con.execute('''CREATE TABLE IF NOT EXISTS SALES (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    "类别" TEXT NOT NULL,
    "名称" TEXT NOT NULL,
    "价格" TEXT NOT NULL,
    "直降" TEXT NOT NULL)''')

con.execute('''CREATE TABLE IF NOT EXISTS AREA (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    "类别" TEXT NOT NULL,
    "名称" TEXT NOT NULL,
    "价格" TEXT NOT NULL,
    "原价" TEXT NOT NULL,
    "人气" TEXT NOT NULL)''')

for y in data_1:
    con.execute("""
    INSERT INTO SALES (类别,名称,价格,直降) VALUES(?,?,?,?)""",(y["类别"],y["名称"],y["价格"],y["直降"]))

for z in data_2:
    con.execute("""
    INSERT INTO AREA (类别,名称,价格,原价,人气) VALUES(?,?,?,?,?)""",(z["类别"],z["名称"],z["价格"],z["原价"],z["人气"]))

con.commit()
con.close()

print("总共抓取{}件商品".format(len(data_1+data_2)))