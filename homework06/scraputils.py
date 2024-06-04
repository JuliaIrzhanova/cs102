"""
Этот модуль содержит функции для извлечения новостей и перехода на следующую страницу с новостями.
"""

import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """
    Извлекает новости с указанной веб-страницы.

    """
    news_list = []
    items = parser.find_all("tr", class_="athing")
    subtexts = parser.find_all("td", class_="subtext")

    for item, subtext in zip(items, subtexts):
        title_tag = item.find("span", class_="titleline").find("a")
        title = title_tag.text
        url = title_tag["href"]
        author = subtext.find("a", class_="hnuser").text if subtext.find("a", class_="hnuser") else "Unknown"
        points_tag = subtext.find("span", class_="score")
        points = int(points_tag.text.split()[0]) if points_tag else 0
        comments_text = subtext.find_all("a")[-1].text
        comments = 0 if comments_text == "discuss" else int(comments_text.split()[0])

        news_list.append(
            {
                "author": author,
                "comments": comments,
                "points": points,
                "title": title,
                "url": url,
            }
        )

    return news_list


def extract_next_page(parser):
    """
    Извлекает URL следующей страницы новостей.

    """
    morelink = parser.find("a", class_="morelink")
    return morelink["href"] if morelink else None


def get_news(url, n_pages=1):
    """
    Собирает новости с указанного URL.

    """
    news = []
    while n_pages:
        print(f"Collecting data from page: {url}")
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        if not next_page:
            break
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news
