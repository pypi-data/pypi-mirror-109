from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from ..models import Album, Lyrics, Track
from ..utils import raise_if_error

if TYPE_CHECKING:
    from .. import Client


async def get_track(self: Client, track_id: int) -> Track:
    token = await self.session.token()
    url = f"http://api.deezer.com/track/{track_id}?access_token={token}"
    res = await self._req.get(url)
    body = await res.json()
    raise_if_error(body)
    return Track.from_dict(self, body)


async def get_album(self: Client, album_id: int) -> Album:
    token = await self.session.token()
    url = f"http://api.deezer.com/album/{album_id}?access_token={token}"
    res = await self._req.get(url)
    body = await res.json()
    raise_if_error(body)
    return Album.from_dict(self, body)


async def get_lyrics(self: Client, lyrics_id: int) -> Optional[Lyrics]:
    if lyrics_id == 0:
        return None
    token = await self.session.token()
    url = f"http://api.deezer.com/album/{lyrics_id}?access_token={token}"
    res = await self._req.get(url)
    body = await res.json()
    raise_if_error(body)
    return Lyrics.from_dict(body)
