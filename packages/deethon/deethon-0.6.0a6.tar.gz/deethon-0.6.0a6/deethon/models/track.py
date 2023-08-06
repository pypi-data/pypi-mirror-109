from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from ..utils.api import get_stream_url
from .quality import Quality

if TYPE_CHECKING:
    from .. import Client
    from ..models import Lyrics


@dataclass
class TrackAlbum:
    id: int
    md5_image: str
    release_date: Optional[datetime]
    title: str

    @staticmethod
    def from_dict(d: dict) -> TrackAlbum:
        release_date = datetime.strptime(
            d["release_date"], "%Y-%m-%d") if "release_date" in d else None
        return TrackAlbum(
            id=d["id"],
            md5_image=d["md5_image"],
            release_date=release_date,
            title=d["title"]
        )


@dataclass
class TrackArtist:
    """
    The Artist class contains several information about an artist.

    Attributes:
        id (int): The Deezer id of the artist.
        name (str): The name of the artist.
    """
    id: int
    name: str

    @property
    def link(self):
        return f"http://www.deezer.com/artist/{self.id}"

    @staticmethod
    def from_dict(d: dict) -> TrackArtist:
        return TrackArtist(d["id"], d["name"])


@dataclass
class TrackContributor:
    id: str
    name: str
    role: str

    @property
    def link(self):
        return f"http://www.deezer.com/artist/{self.id}"

    @staticmethod
    def from_dict(d: dict) -> TrackContributor:
        return TrackContributor(
            id=d["id"],
            name=d["name"],
            role=d["role"]
        )


@dataclass
class SearchTrack:
    """
    The Track class contains several information about a track.

    Attributes:
        artist: The main artist of the track.
        duration: The duration of the track.
        id: The Deezer ID of the track.
        link: The Deezer link of the track.
        preview_link: The link to a 30 second preview of the track.
        rank: The rank of the track on Deezer
        lyrics_id: The lyrics of the track.
        md5_origin: The md5 origin of the track.
        media_version: The media version of the track.
        title: The title of the track.
        title_short: The short title of the track.
    """
    album: TrackAlbum
    artist: TrackArtist
    duration: int
    id: int
    link: str
    preview_link: str
    rank: int
    lyrics_id: int
    md5_image: str
    md5_origin: str
    media_version: int
    title: str
    title_short: str
    _client: Client

    @staticmethod
    def from_dict(client: Client, d: dict) -> SearchTrack:
        return SearchTrack(
            album=TrackAlbum.from_dict(d["album"]),
            artist=TrackArtist.from_dict(d["artist"]),
            duration=d["duration"],
            id=d["id"],
            link=d["link"],
            preview_link=d["preview"],
            rank=d["rank"],
            lyrics_id=d["lyrics_id"],
            md5_image=d["md5_image"],
            md5_origin=d["md5_origin"],
            media_version=d["media_version"],
            title=d["title"],
            title_short=d["title_short"],
            _client=client
        )

    def get_cover_url(self, size: int = 250, quality: int = 80) -> str:
        """
        Get the URL of the album cover.

        Args:
            size: The size of the album cover in pixels (should not exceed 1200).
            quality: The quality of the album cover (should be between 0 and 100).
        """
        return f"http://cdn-images.dzcdn.net/images/cover/{self.md5_image}/{size}x{size}-000000-{quality}-0-0.jpg"

    def get_stream_url(self, quality: Quality) -> str:
        """
        Get the direct download url of the track.

        Args:
            quality: The preferred quality.

        Returns:
            The direct download url.
        """
        return get_stream_url(self.id, self.md5_origin, self.media_version, quality)

    async def download_cover(self, size: int = 250, quality: int = 80) -> bytes:
        """
        Downloads the album cover.

        Args:
            size: The size of the album cover in pixels (should not exceed 1200).
            quality: The quality of the album cover (should be between 0 and 100).
        """
        cover_url = self.get_cover_url(size, quality)
        response = await self._client._req.get(cover_url)
        return await response.read()


@dataclass
class Track:
    """
    The Track class contains several information about a track.

    Attributes:
        album: The album to which the track belongs in short format.
        artist: The main artist of the track.
        bpm: Beats per minute of the track.
        contributors: A list of artists featured in the track.
        disk_number: The disc number of the track.
        duration: The duration of the track.
        id: The Deezer ID of the track.
        isrc: The International Standard Recording Code (ISRC) of the track.
        link: The Deezer link of the track.
        lyrics_id: The Deezer id of the track lyrics.
        md5_origin: The md5 origin of the track.
        media_version: The media version of the track.
        preview_link: The link to a 30 second preview of the track.
        rank: The rank of the track on Deezer
        replaygain_track_gain: The Replay Gain value of the track.
        release_date: The release date of the track.
        title: The title of the track.
        title_short: The short title of the track.
        track_position: The position of the track.
    """
    album: TrackAlbum
    artist: TrackArtist
    bpm: int
    contributors: list[TrackContributor]
    disk_number: int
    duration: int
    id: int
    isrc: str
    link: str
    lyrics_id: int
    md5_image: str
    md5_origin: str
    media_version: int
    preview_link: str
    rank: int
    replaygain_track_gain: str
    release_date: datetime
    title: str
    title_short: str
    title_version: str
    track_position: int
    _client: Client

    @staticmethod
    def from_dict(client: Client, d: dict) -> Track:
        return Track(
            album=TrackAlbum.from_dict(d["album"]),
            artist=TrackArtist.from_dict(d["artist"]),
            bpm=d["bpm"],
            contributors=[TrackContributor.from_dict(
                x) for x in d["contributors"]],
            disk_number=d["disk_number"],
            duration=d["duration"],
            id=d["id"],
            isrc=d["isrc"],
            link=d["link"],
            lyrics_id=d["lyrics_id"],
            md5_image=d["md5_image"],
            md5_origin=d["md5_origin"],
            media_version=d["media_version"],
            preview_link=d["preview"],
            rank=d["rank"],
            replaygain_track_gain=f"{((d['gain'] + 18.4) * -1):.2f} dB",
            release_date=datetime.strptime(d["release_date"], "%Y-%m-%d"),
            title=d["title"],
            title_short=d["title_short"],
            title_version=d.get("title_version") or "",
            track_position=d["track_position"],
            _client=client
        )

    def get_stream_url(self, quality: Quality) -> str:
        """
        Get the direct download url of the track.

        Args:
            quality: The preferred quality.

        Returns:
            The direct download url.
        """
        return get_stream_url(self.id, self.md5_origin, self.media_version, quality)

    def get_cover_url(self, size: int = 250, quality: int = 80) -> str:
        """
        Get the URL of the album cover.

        Args:
            size: The size of the album cover in pixels (should not exceed 1200).
            quality: The quality of the album cover (should be between 0 and 100).
        """
        return f"http://cdn-images.dzcdn.net/images/cover/{self.md5_image}/{size}x{size}-000000-{quality}-0-0.jpg"

    async def download_cover(self, size: int = 250, quality: int = 80) -> bytes:
        """
        Downloads the album cover.

        Args:
            size: The size of the album cover in pixels (should not exceed 1200).
            quality: The quality of the album cover (should be between 0 and 100).
        """
        cover_url = self.get_cover_url(size, quality)
        response = await self._client._req.get(cover_url)
        return await response.read()

    async def get_lyrics(self) -> Optional[Lyrics]:
        """
        Returns the lyrics of the track if available.
        """
        return await self._client.get_lyrics(self.lyrics_id)
