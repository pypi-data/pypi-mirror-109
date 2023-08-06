"""Contains the order objects for all the lists."""
from dataclasses import dataclass
from typing import Dict, Optional

from .enum import OrderDirection

_known_order_mappings: Dict[str, str] = {
    "creation_time": "createdAt",
    "update_time": "updatedAt",
    "publish_time": "publishedAt",
}


@dataclass(frozen=True)
class AuthorListOrder:
    """An object representing the various options for ordering a author list returned from
    :meth:`.MangadexClient.get_authors`.

    .. versionadded:: 0.4
    """

    name: Optional[OrderDirection] = None
    """The name of an author."""


@dataclass(frozen=True)
class ChapterListOrder:
    """An object representing the various options for ordering a chapter list returned from
    :meth:`.MangadexClient.get_chapters`.

    .. versionadded:: 0.4
    """

    creation_time: Optional[OrderDirection] = None
    """The time a chapter was created."""

    update_time: Optional[OrderDirection] = None
    """The time a chapter was updated."""

    publish_time: Optional[OrderDirection] = None
    """The time a chapter was published."""

    # Undocumented in the official docs, see
    # https://discord.com/channels/403905762268545024/839817812012826644/843097446384533544
    title: Optional[OrderDirection] = None
    """The title of the chapter [#V506_CHANGELOG]_."""

    volume: Optional[OrderDirection] = None
    """The chapter's volume."""

    number: Optional[OrderDirection] = None
    """The chapter's number."""


@dataclass(frozen=True)
class CoverListOrder:
    """An object representing the various options for ordering a cover list returned from
    :meth:`.MangadexClient.get_covers`.

    .. versionadded:: 1.0
    """

    creation_time: Optional[OrderDirection] = None
    """The time a cover was created."""

    update_time: Optional[OrderDirection] = None
    """The time a cover was updated."""

    volume: Optional[OrderDirection] = None
    """The cover's volume"""


@dataclass(frozen=True)
class GroupListOrder:
    """An object representing the various options for ordering a group list returned from
    :meth:`.MangadexClient.get_groups`.

    .. versionadded:: 0.5
    """

    name: Optional[OrderDirection] = None
    """The name of the scanlation group [#V506_CHANGELOG]_."""


@dataclass(frozen=True)
class MangaListOrder:
    """An object representing the various options for ordering a manga list returned from
    :meth:`.MangadexClient.search`.

    .. versionadded:: 0.4
    """

    creation_time: Optional[OrderDirection] = None
    """The time a manga was created."""

    update_time: Optional[OrderDirection] = None
    """The time a manga was updated."""

    titles: Optional[OrderDirection] = None
    """The titles of a manga [#V506_CHANGELOG]_."""

    year: Optional[OrderDirection] = None
    """The year a manga was published.
    
    .. seealso:: :attr:`.Manga.year`
    """


@dataclass(frozen=True)
class MangaFeedListOrder:
    """An object representing the various options for ordering a manga feed list returned from the various manga feed
    endpoints.

    .. versionadded:: 0.5
    """

    volume: Optional[OrderDirection] = None
    """The volume number of a chapter."""

    chapter: Optional[OrderDirection] = None
    """The chapter number of a chapter."""


@dataclass(frozen=True)
class UserFollowsMangaFeedListOrder(MangaFeedListOrder):
    """An object representing the various options for ordering a manga feed list returned from the user followed
    manga feed.

    .. versionadded:: 1.1
    """

    creation_time: Optional[OrderDirection] = None
    """The time a chapter was created."""

    update_time: Optional[OrderDirection] = None
    """The time a chapter was updated."""

    publish_time: Optional[OrderDirection] = None
    """The time a chapter was published."""
