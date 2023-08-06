from typing import Any, Dict, List, Optional


class VolumeAggregate(Dict[Optional[str], int]):
    """Represents the aggregate of the chapters in a volume.

    .. versionadded:: 0.5

    .. note::
        The data returned from the server does not have an aggregate for chapters without a name. However,
        a total count is given including the no-number chapters, which can be used to infer the number of chapters
        without a number. This number is stored as the ``None`` key.

    .. versionchanged:: 1.1
        The server now returns the actual count for chapters without a number. This can still be found in the
        ``None`` key.

    Usage:

    .. code-block:: python

        print(aggregate["1"]) # Prints the number of chapters for the chapter with number ``1``.

    """

    def chapters(self) -> List[Optional[str]]:
        """Get the chapters contained in the aggregate.

        :return: The list of chapter numbers (including None if chapters without a chapter number exist)
        :rtype: List[Optional[str]]
        """
        return list(self.keys())

    def total(self) -> int:
        """Get the total amount of chapters contained in this aggregate, or the sum of the individual chapter
        aggregates.

        :return: The sum of chapters in the aggregate
        :rtype: int
        """
        return sum(self.values())

    def parse(self, data: Dict[str, Any]):
        """Parse aggregate data."""
        total_count = data["count"]
        if isinstance(data["chapters"], dict):
            for item in data["chapters"].values():
                if item["chapter"] == "none":
                    item["chapter"] = None
                self[item["chapter"]] = item["count"]

    def __repr__(self) -> str:
        """Provide a string representation of the object.

        :return: The string representation
        :rtype: str
        """
        return f"{type(self).__name__}{super().__repr__()}"


class MangaAggregate(Dict[Optional[str], VolumeAggregate]):
    """Represents the aggregate of the volumes in a manga.

    .. versionadded:: 0.5

    .. note::
        Use ``None`` to get the aggregate for chapters without a volume number.

    Usage:

    .. code-block:: python

        print(aggregate["N/A"]["1"]) # Prints the number of chapters for the chapter with number ``1``.
    """

    def volumes(self) -> List[Optional[str]]:
        """Get the volumes contained in the aggregate.

        :return: The list of volume numbers (including None if chapters without a volume name exist)
        :rtype: List[Optional[str]]
        """
        return list(self.keys())

    def total(self) -> int:
        """Get the total amount of chapters contained in this aggregate, or the sum of the individual volume
        aggregates.

        :return: The sum of chapters in the aggregate
        :rtype: int
        """
        return sum(item.total() for item in self.values())

    def parse(self, data: Dict[str, Any]):
        """Parse aggregate data."""
        for key, value in data["volumes"].items():
            if key == "none":
                key = None
            va = VolumeAggregate()
            va.parse(value)
            self[key] = va

    def __repr__(self) -> str:
        """Provide a string representation of the object.

        :return: The string representation
        :rtype: str
        """
        return f"{type(self).__name__}{super().__repr__()}"
