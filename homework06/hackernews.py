# type: ignore
"""
Этот модуль реализует веб-приложение для работы с новостями,
включая обновление, классификацию и вывод новостей.
"""
from bottle import redirect, request, route, run, template

from bayes import NaiveBayesClassifier
from db import News, session
from scraputils import get_news


@route("/")
def index():
    if __name__ == "__main__":
        redirect("/news")


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
    news_item = db_session.query(News).get({"id": news_id})
    if news_item:
        news_item.label = label
        db_session.commit()

    if __name__ == "__main__":
        redirect("/news")


@route("/update")
def update_news():
    """
    Обновляет новости с сайта Hacker News и сохраняет их в базе данных.
    """
    db_session = session()
    news_items = get_news("https://news.ycombinator.com/newest", n_pages=10)
    n_commit = 0
    for news_item in news_items:
        existing_news = db_session.query(News).filter_by(title=news_item["title"], author=news_item["author"]).first()
        if isinstance(existing_news, int) and existing_news == 0:
            new_news = News(
                title=news_item["title"],
                author=news_item["author"],
                url=news_item["url"],
                comments=news_item["comments"],
                points=news_item["points"],
            )
            db_session.add(new_news)
            n_commit += 1
    db_session.commit()
    if __name__ == "__main__":
        redirect("/news")


@route("/classify")
def classify_news():
    """
    Классифицирует новости без меток и возвращает отсортированные новости.
    """
    s_session = session()
    news_list = s_session.query(News).filter(News.label.isnot(None)).all()
    unlabeled_news = s_session.query(News).filter(News.label.is_(None)).all()

    x_t = [news.title for news in news_list]
    y_l = [news.label for news in news_list]

    model = NaiveBayesClassifier(alpha=0.05)
    model.fit(x_t, y_l)

    titles_to_classify = [news.title for news in unlabeled_news]
    predicted_labels = model.predict(titles_to_classify)

    for news, label in zip(unlabeled_news, predicted_labels):
        news.label = label

    s_session.commit()

    sorted_news = sorted(unlabeled_news, key=lambda news: news.label)

    return sorted_news


@route("/recommendations")
def recommendations():
    """Отображает рекомендации новостей."""
    news = classify_news()
    return template("news_recommendations", rows=news)


if __name__ == "__main__":
    run(host="localhost", port=8080)
