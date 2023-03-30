from bs4 import BeautifulStoneSoup

with open("./scraping/index.html", "r") as f:
    data = f.read()

soup = BeautifulStoneSoup(data, 'html.parser')

print(soup)