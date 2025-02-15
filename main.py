import requests
import pymysql
from bs4 import BeautifulSoup
import time
import os
from dotenv import load_dotenv

load_dotenv()

db = pymysql.connect(
    host="localhost", port=3306, user="root", passwd="", charset="utf8"
)
cursor = db.cursor()

url = os.getenv("URL")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
}

products = []
page = 1
while True:
    print(page)
    time.sleep(1)
    response = requests.get(f"{url}{page}", headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    is_last_page = soup.select(".ec-base-paginate > *")[-2]["href"] == "#none"
    datas = soup.select(".xans-record- .description")
    thumbnails = soup.select(".xans-record- > .thumbnail > .prdImg > a > img")
    for data, thumbnail in zip(datas, thumbnails):
        print(data.select_one("strong.name > a > *:last-child").text)
        link = data.select_one("strong.name > a")["href"]
        price = float(data.select_one("li.xans-record- > span").text.lstrip("USD "))
        discounts = data.select_one("li.xans-record-:nth-child(2) > span")
        if not discounts:
            discount_price = price
            discount_rate = int(0)
        else:
            discounts = discounts.text.split()
            discount_price = float(discounts[1])
            discount_rate = int(discounts[2][1:].rstrip("%"))
        reviews = int(data.select_one(".review_count_view1")["data-review"])
        product = {
            "name": data.select_one("strong.name > a > *:last-child").text,
            "price": price,
            "discount_price": discount_price,
            "discount_rate": discount_rate,
            "reviews": reviews,
            "link": f"https://jolse.com{link}",
            "thumbnail": thumbnail["src"],
        }
        products.append(product)
    if is_last_page:
        break
    page += 1


sql = "create database if not exists beauty_shop;"
cursor.execute(sql)
db.commit()
sql = "use beauty_shop;"
cursor.execute(sql)
db.commit()
sql = """
create table if not exists products (
    id int auto_increment primary key,
    name varchar(100) not null,
    price decimal(6,2) not null,
    discount_price decimal(6,2) not null,
    discount_rate tinyint not null,
    reviews int not null,
    link varchar(255) not null,
    thumbnail varchar(255) not null
)
"""
cursor.execute(sql)
db.commit()
for product in products:
    sql = f"insert into products (name, price, discount_price, discount_rate, reviews, link, thumbnail) values(%s, %s, %s, %s, %s, %s, %s);"
    values = (
        product["name"],
        product["price"],
        product["discount_price"],
        product["discount_rate"],
        product["reviews"],
        product["link"],
        product["thumbnail"],
    )
    cursor.execute(sql, values)
db.commit()
