import mechanicalsoup
import pandas as pd
import sqlite3

url = "https://minecraft.wiki/w/Enchanting"

browser = mechanicalsoup.StatefulBrowser()
browser.open(url)

all_tables = browser.page.find_all("table", attrs={"class": "wikitable"})

th = browser.page.find_all("th")
all_headers = [value.text.replace("\n", "") for value in th]
wanted_th = all_headers[
    all_headers.index("Enchantment") : (all_headers.index("Enchantment") + 5)
]
wanted_th = [th.replace(" ", "_") for th in wanted_th]

td = browser.page.find_all("td")
columns = [value.text.strip() for value in td][827:1022]

dictionary = {}

for idx, key in enumerate(wanted_th):
    dictionary[key] = columns[idx:][::5]

df = pd.DataFrame(data=dictionary)
print(",".join(wanted_th))

connection = sqlite3.connect("enchanting.db")
cursor = connection.cursor()
cursor.execute("create table ENCHANT_STATS (" + ",".join(wanted_th) + ")")
for i in range(len(df)):
    cursor.execute("insert into ENCHANT_STATS values (?,?,?,?,?)", df.iloc[i])

connection.commit()
connection.close()
