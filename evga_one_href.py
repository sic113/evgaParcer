import requests
from bs4 import BeautifulSoup
import lxml
import os
import csv
from time import sleep


domen = "https://evgakids.com/kategorii-sayta/p-0/"
domen_last = "https://evgakids.com/kategorii-sayta/p-76/"

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 OPR/75.0.3969.93",
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}

htm = domen.split("/")
print(htm[4])
# Получаем главный html


with open("evga_1href.csv", "w", newline='', encoding="UTF-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    "Артикул",
                    "Описание",
                    "Название",
                    "Размер",
                    "Фото по ссылке",
                    "Цена",
                    "Категория",
                    "Наличие",
                    "Отображать на сайте"
                )
            )


for i in range(77):
    domen = f"https://evgakids.com/kategorii-sayta/p-{i}/"
    htm = domen.split("/")
    req = requests.get(url=domen, headers=headers)
    src = req.text
    with open(f"evga/source/{htm[4]}.html", "w", encoding="UTF-8") as file:
        file.write(src)
    print(f"htm {i} dwnloded")
    sleep(1)

products_list = []
for i in range(77):
    domen = f"https://evgakids.com/kategorii-sayta/p-{i}/"
    htm = domen.split("/")
    with open(f"evga/source/{htm[4]}.html", "r", encoding="UTF-8") as file:
        src = file.read()
    print(f"Ссылка номер {i} открыта")

    soup = BeautifulSoup(src, "lxml")
    divs = soup.findAll("div", class_="name")
    for i in divs:
        products_href = i.find("a").get("href")
        products_list.append(products_href)

n = 0
print(f"Всего товаров:")
for i in products_list:
    req = requests.get(url=i, headers=headers)
    src = req.text
    with open(f"evga/source/products/prod_{n}.html", "w", encoding="UTF-8") as file:
        file.write(src)
    print(f"товар номер {n} сохранен, осталось {len(products_list) - n}")
    n += 1


def sort_key_digit_getter(row):
    raw_digit, *_ = row.split("_")
    return int(raw_digit)

folder_name = "evga/source/products/"
nazvaniya = os.listdir(folder_name)

n = 0
# открываем каждый товар
for name in nazvaniya:
    with open(f"{folder_name}/{name}", "r", encoding="UTF-8") as file:
        src = file.read()
        soup = BeautifulSoup(src, "lxml")

        try:
            art = soup.find("span", itemprop="mpn").text.strip()
        except:
            art = "-"
        # print(art)


        try:
            discr = soup.find("div", class_="block-wrapp").text
            # discr = discr.replace("А чтобы вы наглядно оценили все преимущества и достоинства данного товара предлагаем вашему вниманию видеообзор:","")
            discr = discr.replace(" ","")
            discr = discr.strip()
        except:
            discr = "-"


        try:
            video_link = soup.find("iframe",allowfullscreen="allowfullscreen").get("src")
        except:
            video_link = ""

        discr = discr+"\n"+video_link
        discr = discr.strip()

        try:
            name = soup.find("div", class_="code").findNext("h1").text.strip()
        except:
            name = "-"
        # print(name)

        try:
            razmer = soup.find("div", class_="element-value").text.replace("Выберите Размер ","").strip()
        except:
            razmer = "-"
        # print(razmer)

        try:
            price = soup.find("div", class_="price").text.replace("\n","").strip()
        except:
            price = "-"
        # print(price)

        try:
            dom = "https://evgakids.com"
            img_hrefs = soup.find("div", class_="simpleLens-thumbnails-container ev-vertical-thumbnails js-vertical-thumbnails").find("div",class_="element")
            href = img_hrefs.find("a").get("data-big-image")
            href = dom+href
        except:
            href = "-"
        # print(hrefs)

        try:
            kats_list = soup.find("div", class_="os-crumbs").findAll("span", itemprop="title")
            kats = ""
            for i in kats_list:
                kat = i.text
                kats = kats+kat+"/"
            kats = kats.replace("Evgakids/Категории сайта/","")
            kats.strip()
        except:
            kats = "-"


        try:
            nalichie = "в наличии"
        except:
            nalichie = "?"



        try:
            show = "да"
        except:
            show = "-"



        with open("evga_1href.csv", "a", newline='', encoding="UTF-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    art,
                    discr,
                    name,
                    razmer,
                    href,
                    price,
                    kats,
                    nalichie,
                    show
                )
            )
    print(f"Товар с артикулом '{art}' номером '{n}' записан в csv, осталость: {len(nazvaniya) - n}")
    n += 1