#type: ignore
"""
Этот модуль реализует веб-приложение для работы с новостями,
включая обновление, классификацию и вывод новостей.
"""

from bottle import redirect, request, route, run, template

from bayes import NaiveBayesClassifier
from db import News, session
from scraputils import get_news


@route("/news")
def news_list():
    """
    Отображает список новостей без меток.
    """
    db_session = session()
    rows = db_session.query(News).filter(News.label.is_(None)).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    """
    Добавляет метку к указанной новости и перенаправляет на страницу новостей.
    """
    label = request.query.label
    news_id = request.query.id

    db_session = session()
    news_item = db_session.query(News).filter_by(id=news_id).first()
    news_item.label = label
    db_session.commit()

    redirect("/news")


@route("/update")
def update_news():
    """
    Обновляет новости с сайта Hacker News и сохраняет их в базе данных.
    """
    db_session = session()
    news_items = get_news("https://news.ycombinator.com/newest", n_pages=10)
    for news_item in news_items:
        existing_news = db_session.query(News).filter_by(title=news_item["title"], author=news_item["author"]).first()
        if not existing_news:
            new_news = News(
                title=news_item["title"],
                author=news_item["author"],
                url=news_item["url"],
                comments=news_item["comments"],
                points=news_item["points"],
            )
            db_session.add(new_news)
    db_session.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    """
    Классифицирует новости без меток и обновляет базу данных.
    """
    db_session = session()
    unlabelled_news = db_session.query(News).filter(News.label.is_(None)).all()

    if unlabelled_news:
        labelled_news = db_session.query(News).filter(News.label.isnot(None)).all()
        y_labelled = [news.label for news in labelled_news]
        x_labelled = [news.title for news in labelled_news]

        model = NaiveBayesClassifier()
        model.fit(x_labelled, y_labelled)

        for news in unlabelled_news:
            news.label = model.predict([news.title])[0]

        db_session.commit()
    redirect("/news")


@route("/recommendations")
def recommendations():
    """
    Отображает ранжированный список новостей.
    """
    db_session = session()
    unlabelled_news = db_session.query(News).filter(News.label.is_(None)).all()

    labelled_news = db_session.query(News).filter(News.label.isnot(None)).all()
    y_labelled = [news.label for news in labelled_news]
    x_labelled = [news.title for news in labelled_news]

    model = NaiveBayesClassifier()
    model.fit(x_labelled, y_labelled)

    classified_news = []
    for news in unlabelled_news:
        label = model.predict([news.title])[0]
        classified_news.append(
            {
                "title": news.title,
                "author": news.author,
                "url": news.url,
                "comments": news.comments,
                "points": news.points,
                "label": label,
            }
        )

    classified_news = sorted(classified_news, key=lambda x: x["points"], reverse=True)
    return template("news_recommendations", rows=classified_news)


if __name__ == "__main__":
    run(host="localhost", port=8080)
