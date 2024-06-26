# type: ignore
import dataclasses
import math
import typing as tp
from time import sleep

import requests

from vkapi import session
from vkapi.config import VK_CONFIG

# from vkapi.exceptions import APIError

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:

    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).

    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """

    domain = VK_CONFIG["domain"]
    access_token = VK_CONFIG["access_token"]
    v = VK_CONFIG["version"]

    params = {"access_token": access_token, "user_id": user_id, "v": v, "count": count, "offset": offset}

    if fields:
        params["fields"] = ",".join(fields)

    max_retries = 5
    retry_delay = 1

    for attempt in range(max_retries):
        response = requests.get(f"{domain}/friends.get", params=params)
        data = response.json()

        if "error" in data:
            error_code = data["error"]["error_code"]
            error_msg = data["error"]["error_msg"]
            if error_code == 30:
                raise Exception(f"Аккаунт пользователя {user_id} является закрытым.")
            elif error_code == 6:
                if attempt < max_retries - 1:
                    sleep(retry_delay)
                else:
                    raise Exception(f"Ошибка VK API: Превышен лимит запросов ({error_msg})")
            else:
                raise Exception(f"Ошибка VK API: {error_msg}")
        else:
            friends_data = data["response"]
            return FriendsResponse(count=friends_data["count"], items=friends_data["items"])

    raise Exception("Не удалось выполнить запрос к VK API после нескольких попыток.")

    friends_data = data["response"]
    return FriendsResponse(count=friends_data["count"], items=friends_data["items"])


print(get_friends(71313378))


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.

    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """
    domain = VK_CONFIG["domain"]
    access_token = VK_CONFIG["access_token"]
    v = VK_CONFIG["version"]

    mutual_friends = []

    if progress is None:
        progress = lambda x: x

    if target_uids is not None:
        target_uids = target_uids
    else:
        target_uids = [target_uid]

    source_friends_response = get_friends(source_uid)
    source_friends_set = set(source_friends_response.items)
    if not isinstance(source_friends_response.items, list):
        raise ValueError("Expected source_friends_response.items to be a list")

    chunk_size = 100
    for i in progress(range(0, len(target_uids), chunk_size)):
        chunk = target_uids[i : i + chunk_size]

        for target in chunk:
            target_friends = get_friends(target)
            target_friends_set = set(target_friends.items)

            common_friends = list(source_friends_set.intersection(target_friends_set))

            mutual_friends.append(
                {"id": target, "common_friends": list(common_friends), "common_count": len(common_friends)}
            )

        sleep(1 / 3)

    print(source_friends_response)
    return mutual_friends


print(get_mutual(71313378, 443814824))
