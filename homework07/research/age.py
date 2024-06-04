import datetime as dt
import statistics
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    data = get_friends(user_id, fields=["bdate"])
    current_date = dt.datetime.now()
    ages = []
    for friend in data.items:
        try:
            if not isinstance(friend, dict):
                raise ValueError()
            age_datetime = dt.datetime.strptime(friend["bdate"], "%d.%m.%Y")
            ages.append((current_date - age_datetime).days // 365.25)
        except:
            pass
    return statistics.median(ages) if ages else None

print(age_predict(189183825))
