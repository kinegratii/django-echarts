from typing import List, Union, TypedDict

from typing_extensions import NotRequired


class TNavConfig(TypedDict):
    nav_left: NotRequired[List[Union[str, dict]]]
    nav_right: NotRequired[List[Union[str, dict]]]
    nav_footer: NotRequired[List[Union[str, dict]]]
