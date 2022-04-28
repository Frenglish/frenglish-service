from typing import TypedDict, Union


class UserData(TypedDict, total=False):
    id: str
    first_name: str
    last_name: str
    email: str
    username: Union[str, None]
