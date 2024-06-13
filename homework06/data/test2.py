import csv
import string

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

with open("SMSSpamCollection") as f:
    data = list(csv.reader(f, delimiter="\t"))


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


X, y = [], []
for target, msg in data:
    X.append(msg)
    y.append(target)
X = [clean(x).lower() for x in X]

X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]

model = Pipeline(
    [
        ("vectorizer", CountVectorizer()),
        ("classifier", MultinomialNB(alpha=0.05)),
    ]
)

model.fit(X_train, y_train)
print(accuracy_score(model.predict(X_test), y_test))
# 0.982057416268
