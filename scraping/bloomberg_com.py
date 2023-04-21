from bs4 import BeautifulSoup
import pandas as pd
import requests

def get_article(data):
    if data is None:
        return None
    else:
        return dict(
            headline=data.get_text(),
            link='https://www.bloomberg.com' + data['href']
        )

def bloomberg_com():
    
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"
    }
    #TODO: Fix the data that is coming back from the request
    # -- try this -- #
    # resp = requests.get("https://www.bloomberg.com/fx-center", headers=headers)
    # soup = BeautifulSoup(resp.content, 'html.parser')
    # ---

    # -- when it doesn't work, use the mockup -- #
    with open("./scraping/mock_files/bloomberg.html", "r", encoding="utf-8") as f:
        resp = f.read()
        soup = BeautifulSoup(resp, 'html.parser')
    # ---

    all_links = []

    headline = soup.select_one(".single-story-module__headline-link")
    all_links.append(get_article(headline))

    grid_articles = soup.select(".grid-module-story__headline-link")
    [all_links.append(get_article(x)) for x in grid_articles]

    side_articles = soup.select(".story-list-story__info__headline-link")
    [all_links.append(get_article(x)) for x in side_articles]

    return [link for link in all_links if link is not None]
