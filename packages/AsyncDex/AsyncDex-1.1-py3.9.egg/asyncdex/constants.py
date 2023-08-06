import re
from re import compile
from typing import Dict, List

from .ratelimit import Path, PathRatelimit

invalid_folder_name_regex = re.compile(
    r"""([<>:"/\\|?*\u0000\u0001\u0002\u0003\u0004\u0005\u0006\u0007\u0008\u0009
\u000a\u000b\u000c\u000d\u000e\u000f\u0010\u0011\u0012\u0013\u0014\u0015\u0016\u0017\u0018\u0019\u001a\u001b\u001c
\u001d\u001e\u001f]|CON|PRN|AUX|NUL|COM1|COM2|COM3|COM4|COM5|COM6|COM7|COM8|COM9|LPT1|LPT2|LPT3|LPT4|LPT5|LPT6|LPT7
|LPT8|LPT9)""",
    re.VERBOSE,
)
r"""The regex for invalid folder names.

Contains:

* Windows/MacOS/Linux restricted characters:
    * ``<``
    * ``>``
    * ``:``
    * ``"``
    * ``/``
    * ``\``
    * ``|``
    * ``?``
    * ``*``
    
* All control characters from ``0x0`` through ``0x31`` inclusive.
* Windows restricted filename:
    * ``CON``
    * ``PRN``
    * ``AUX``
    * ``NUL``
    * ``COM1``
    * ``COM2``
    * ``COM3``
    * ``COM4``
    * ``COM5``
    * ``COM6``
    * ``COM7``
    * ``COM8``
    * ``COM9``
    * ``LPT1``
    * ``LPT2``
    * ``LPT3``
    * ``LPT4``
    * ``LPT5``
    * ``LPT6``
    * ``LPT7``
    * ``LPT8``
    * ``LPT9``

Source: https://stackoverflow.com/a/31976060/12248328

.. versionadded:: 0.3
"""

link_name_to_attribute_mapping: Dict[str, str] = {
    "al": "anilist_id",
    "ap": "animeplanet_id",
    "bw": "bookwalker_id",
    "mu": "mangaupdates_id",
    "nu": "novelupdates_id",
    "kt": "kitsu_id",
    "amz": "amazon_id",
    "cdj": "cdjapan_id",
    "ebj": "ebookjapan_id",
    "mal": "myanimelist_id",
    "raw": "raw_url",
    "engtl": "english_translation_url",
}
"""A mapping of the MangaDex link attribute name to the AsyncDex attribute name.

.. versionadded:: 0.5
"""

ratelimit_data: List[PathRatelimit] = [
    PathRatelimit(Path("/account/create", compile(r"/account/create")), 1, 60 * 60),
    PathRatelimit(Path("/account/activate/{code}", compile(r"/account/activate/\S+")), 30, 60 * 60),
    PathRatelimit(Path("/account/activate/resend", compile(r"/account/activate/resend")), 5, 60 * 60),
    PathRatelimit(Path("/account/recover", compile(r"/account/recover")), 5, 60 * 60),
    PathRatelimit(Path("/account/recover/{code}", compile(r"/account/recover/\S+")), 5, 60 * 60),
    PathRatelimit(Path("/auth/login", compile(r"/auth/login")), 30, 30 * 60),
    PathRatelimit(Path("/auth/refresh", compile(r"/auth/refresh")), 30, 30 * 60),
    PathRatelimit(Path("/chapter/{id}/read", compile(r"/chapter/\S+/read")), 300, 10 * 60),
    PathRatelimit(Path("/upload/begin", compile(r"/upload/begin")), 30, 1 * 60),
    PathRatelimit(Path("/upload/{id}", compile(r"/upload/\S+")), 30, 1 * 60),
    PathRatelimit(Path("/upload/{id}/commit", compile(r"/upload/\S+/commit")), 30, 1 * 60),
    PathRatelimit(Path("/chapter/{id}", compile(r"/chapter/\S+"), "PUT"), 10, 1 * 60),
    PathRatelimit(Path("/chapter/{id}", compile(r"/chapter/\S+"), "DELETE"), 10, 1 * 60),
    PathRatelimit(Path("/manga", compile(r"/manga"), "POST"), 10, 60 * 60),
    PathRatelimit(Path("/manga/{id}", compile(r"/manga/\S+"), "PUT"), 10, 1 * 60),
    PathRatelimit(Path("/manga/{id}", compile(r"/manga/\S+"), "DELETE"), 10, 10 * 60),
    PathRatelimit(Path("/group", compile(r"/group"), "POST"), 10, 60 * 60),
    PathRatelimit(Path("/group/{id}", compile(r"/group/\S+"), "PUT"), 10, 1 * 60),
    PathRatelimit(Path("/group/{id}", compile(r"/group/\S+"), "DELETE"), 10, 10 * 60),
    PathRatelimit(Path("/author", compile(r"/author"), "POST"), 10, 60 * 60),
    PathRatelimit(Path("/author/{id}", compile(r"/author/\S+"), "PUT"), 10, 1 * 60),
    PathRatelimit(Path("/author/{id}", compile(r"/author/\S+"), "DELETE"), 10, 10 * 60),
    PathRatelimit(Path("/captcha/solve", compile(r"/captcha/solve"), "POST"), 10, 10 * 60),
    PathRatelimit(Path("/at-home/server/{id}", compile(r"/at-home/server/\S+"), "GET"), 60, 1 * 60),
]
"""These are the ratelimit rules taken from the API Docs. 

.. note::
    The API rules given here do not reflect all possible API ratelimit rules. The client will automatically ratelimit
    when appropriate headers are sent by the API. Check the latest API rules at
    `the official API documentation <https://api.mangadex.org/docs.html#section/Rating-limits>`_.

.. versionchanged:: 0.3
"""

routes: Dict[str, str] = {
    "activate_account": "/account/activate/{code}",
    "aggregate": "/manga/{id}/aggregate",
    "auth_check": "/auth/check",
    "author": "/author/{id}",
    "author_list": "/author",
    "batch_manga_read": "/manga/read",
    "captcha": "/captcha/solve",
    "chapter": "/chapter/{id}",
    "chapter_list": "/chapter",
    "cover": "/cover/{id}",
    "cover_list": "/cover",
    "cover_upload": "/cover/{mangaId}",
    "create_account": "/account/create",
    "finish_recover": "/account/recover/{code}",
    "group": "/group/{id}",
    "group_follow": "/group/{id}/follow",
    "group_list": "/group",
    "legacy": "/legacy/mapping",
    "list": "/list/{id}",
    "list_feed": "/list/{id}/feed",
    "logged_in_user": "/user/me",
    "logged_user_groups": "/user/follows/group",
    "logged_user_lists": "/user/list",
    "logged_user_manga": "/user/follows/manga",
    "logged_user_manga_status": "/manga/status",
    "logged_user_manga_chapters": "/user/follows/manga/feed",
    "logged_user_users": "/user/follows/user",
    "login": "/auth/login",
    "logout": "/auth/logout",
    "manga": "/manga/{id}",
    "manga_follow": "/manga/{id}/follow",
    "manga_chapters": "/manga/{id}/feed",
    "manga_list": "/manga/{id}/list/{listId}",
    "manga_read": "/manga/{id}/read",
    "manga_read_status": "/manga/{id}/status",
    "md@h": "/at-home/server/{chapterId}",  # MD@H (MangaDex at Home)
    "ping": "/ping",
    "random_manga": "/manga/random",
    "read": "/chapter/{id}/read",
    "report_page": "https://api.mangadex.network/report",
    "resend": "/account/activate/resend",
    "search": "/manga",
    "session_token": "/auth/refresh",
    "start_recover": "/account/recover",
    "tag_list": "/manga/tag",
    "user": "/user/{id}",
}
"""The various predefined routes for the client. If the API changes for a given destination, the route can easily
be modified without copy-pasting the route to the functions using it.

.. versionchanged:: 0.4
    ``mdah`` renamed to ``md@h``.
"""

permission_model_mapping: Dict[str, str] = {
    "author.view": "author",
    "chapter.view": "chapter",
    "cover.view": "cover_art",
    "manga.view": "manga",
    "scanlation_group.view": "scanlation_group",
    "user.view": "user"
}
"""A mapping containing permission names to the type of model. Used for reference expansion.

.. versionadded:: 1.1
"""
