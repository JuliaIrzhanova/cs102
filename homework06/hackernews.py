from bottle import route, run, template, request, redirect
from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    label = request.query.label
    news_id = request.query.id

    s = session()
    news_item = s.query(News).filter_by(id=news_id).first()
    news_item.label = label
    s.commit()

    redirect("/news")


@route("/update")
def update_news():
    s = session()
    news_list = get_news("https://news.ycombinator.com/newest", n_pages=10)
    for news in news_list:
        existing_news = s.query(News).filter_by(title=news['title'], author=news['author']).first()
        if not existing_news:
            news_item = News(
                title=news['title'],
                author=news['author'],
                url=news['url'],
                comments=news['comments'],
                points=news['points']
            )
            s.add(news_item)
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    news = s.query(News).filter(News.label == None).all()

    X = [n.title for n in news]
    y = [n.label for n in news if n.label]

    model = NaiveBayesClassifier()
    model.fit(X, y)

    for n in news:
        n.label = model.predict([n.title])[0]

    s.commit()
    redirect("/news")


@route("/recommendations")
def recommendations():
    s = session()
    news = s.query(News).filter(News.label == None).all()

    X = [n.title for n in news]
    y = [n.label for n in news if n.label]

    model = NaiveBayesClassifier()
    model.fit(X, y)

    classified_news = []
    for n in news:
        label = model.predict([n.title])[0]
        classified_news.append({
            'title': n.title,
            'author': n.author,
            'url': n.url,
            'comments': n.comments,
            'points': n.points,
            'label': label
        })

    classified_news = sorted(classified_news, key=lambda x: x['points'], reverse=True)
    return template('news_recommendations', rows=classified_news)


if __name__ == "__main__":
    run(host="localhost", port=8080)
