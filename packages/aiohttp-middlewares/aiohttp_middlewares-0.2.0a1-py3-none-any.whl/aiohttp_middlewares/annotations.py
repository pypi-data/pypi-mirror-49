"""
===============================
aiohttp_middlewares.annotations
===============================

Type annotation shortcuts for the project.

"""

from typing import Dict, FrozenSet, List, Set, Tuple, Union
from typing.re import Pattern


StrCollection = Union[List[str], FrozenSet[str], Set[str], Tuple[str, ...]]
StrDict = Dict[str, str]

Url = Union[str, Pattern]
UrlCollection = Union[List[Url], Set[Url], Tuple[Url, ...]]
UrlDict = Dict[Url, Union[StrCollection, str]]
Urls = Union[UrlCollection, UrlDict]
