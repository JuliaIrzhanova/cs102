import requests
from bs4 import BeautifulSoup
import db


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    items = parser.find_all('tr', class_='athing')
    subtexts = parser.find_all('td', class_='subtext')

    for item, subtext in zip(items, subtexts):
        title_tag = item.find('span', class_='titleline').find('a')
        title = title_tag.text
        url = title_tag['href']
        author = subtext.find('a', class_='hnuser').text
        points = int(subtext.find('span', class_='score').text.split()[0])
        comments_text = subtext.find_all('a')[-1].text
        comments = 0 if comments_text == 'discuss' else int(comments_text.split()[0])

        news_list.append({
            'author': author,
            'comments': comments,
            'points': points,
            'title': title,
            'url': url
        })

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    morelink = parser.find('a', class_='morelink')
    return morelink['href'] if morelink else None

def save_news(news_list, session):
    for news in news_list:
        news_item = News(
            title=news['title'],
            author=news['author'],
            url=news['url'],
            comments=news['comments'],
            points=news['points']
        )
        session.add(news_item)
    session.commit()


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news

news_list = get_news("https://news.ycombinator.com/newest", n_pages=2)
print(news_list[:3])