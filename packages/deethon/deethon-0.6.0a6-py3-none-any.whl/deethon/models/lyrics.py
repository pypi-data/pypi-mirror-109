from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Lyrics:
    id: int
    text: str
    copyright: str
    writers: str

    @staticmethod
    def from_dict(d: dict) -> Lyrics:
        return Lyrics(
            id=d["id"],
            text=d["test"],
            copyright=d["copyright"],
            writers=d["writers"]
        )
