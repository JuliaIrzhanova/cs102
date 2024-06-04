import math


class NaiveBayesClassifier:
    def __init__(self, alpha=1.0):
        self.alpha = alpha  # параметр сглаживания
        self.classes = set()
        self.counts = {}  # словарь для хранения количества статей для каждого класса
        self.word_counts = {}  # словарь для хранения количества каждого слова для каждого класса
        self.set_words = set()  # набор уникальных слов во всех документах
        self.word_counts_class = {}  # словарь для хранения общего количества слов для каждого класса

    def fit(self, X, y):
        """Fit Naive Bayes classifier according to X, y."""
        for text, label in zip(X, y):
            self.classes.add(label)
            if label not in self.counts:
                self.counts[label] = 0
                self.word_counts[label] = {}
                self.word_counts_class[label] = 0
            self.counts[label] += 1
            words = text.split()
            for word in words:
                if word not in self.word_counts[label]:
                    self.word_counts[label][word] = 0
                self.word_counts[label][word] += 1
                self.set_words.add(word)
                self.word_counts_class[label] += 1

    def predict(self, X):
        """Perform classification on an array of test vectors X."""
        predictions = []
        for text in X:
            words = text.split()
            logs = {}
            for i in self.classes:
                prob_log = math.log(self.counts[i] / sum(self.counts.values()))
                for word in words:
                    prob_word = (self.word_counts[i].get(word, 0) + self.alpha) / (
                        self.word_counts_class[i] + self.alpha * len(self.set_words)
                    )
                    prob_log += math.log(prob_word)
                logs[i] = prob_log
            predictions.append(max(logs, key=logs.get))
        return predictions

    def score(self, X_test, y_test):
        """Returns the mean accuracy on the given test data and labels."""
        predictions = self.predict(X_test)
        correct = sum(1 for pred, true in zip(predictions, y_test) if pred == true)
        return correct / len(y_test)
