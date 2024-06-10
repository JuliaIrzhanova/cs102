import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tqdm.notebook import tqdm


class GDRegressor:
    def __init__(self, alpha=0.001, n_iter=100, progress=True):
        self.alpha = alpha # скорость обучения
        self.n_iter = n_iter
        self.progress = progress

    def fit(self, X, y):
        m, n = X.shape # количество примеров и признаков
        self.param = np.zeros(n) # инициализируем вектор параметров нулями
        self.loss_history = [] # список для хранения истории значений функции стоимости
        self.param_history = [] # список для хранения истории значений параметров

        for _ in tqdm(range(self.n_iter), disable=not self.progress):
            gradients = 1 / m * X.T.dot(X.dot(self.param) - y)
            self.param -= self.alpha * gradients
            loss = self.compute_cost(X, y)
            self.loss_history.append(loss)
            self.param_history.append(self.param.copy())

    def predict(self, X):
        return X.dot(self.param)

    def compute_cost(self, X, y):
        m = len(y)
        return (1 / (2 * m)) * np.sum((X.dot(self.param) - y) ** 2)
