import httpx
from bs4 import BeautifulSoup
import asyncio
import re
from pydantic import BaseModel, field_validator
from typing import List, Optional, Union, NamedTuple
from pydantic import HttpUrl



# TrackListEntry for initial (id, url) pairs
class TrackListEntry(NamedTuple):
    id: str
    url: HttpUrl

# Initial TRACKLISTS: list of (id, url)
TRACKLISTS: List[TrackListEntry] = [
    TrackListEntry("hank-the-dj-1", "https://www.2manybootlegs.com/radio-shows/hank-the-dj/hank-the-dj-1/"),
    TrackListEntry("hank-the-dj-2", "https://www.2manybootlegs.com/radio-shows/hank-the-dj/hank-the-dj-2/"),
    TrackListEntry("hank-the-dj-3", "https://www.2manybootlegs.com/radio-shows/hank-the-dj/hank-the-dj-3/"),
    TrackListEntry("hank-the-dj-4", "https://www.2manybootlegs.com/radio-shows/hank-the-dj/hank-the-dj-4/"),
    TrackListEntry("hank-the-dj-5", "https://www.2manybootlegs.com/radio-shows/hank-the-dj/hank-the-dj-5/"),
    TrackListEntry("hank-the-dj-6", "https://www.2manybootlegs.com/radio-shows/hank-the-dj/hank-the-dj-6/"),
    TrackListEntry("hank-the-dj-7", "https://www.2manybootlegs.com/radio-shows/hank-the-dj/hank-the-dj-7/"),
    TrackListEntry("hank-the-dj-8", "https://www.2manybootlegs.com/radio-shows/hank-the-dj/hank-the-dj-8/"),
    TrackListEntry("hank-the-dj-9", "https://www.2manybootlegs.com/radio-shows/hank-the-dj/hank-the-dj-9/"),
    TrackListEntry("hank-the-dj-10", "https://www.2manybootlegs.com/radio-shows/hank-the-dj/hank-the-dj-10/"),
    TrackListEntry("hang-the-dj-1", "https://www.2manybootlegs.com/radio-shows/hang-the-dj/hang-the-dj-1/"),
    TrackListEntry("hang-the-dj-2", "https://www.2manybootlegs.com/radio-shows/hang-the-dj/hang-the-dj-2/"),
    TrackListEntry("hang-the-dj-3", "https://www.2manybootlegs.com/radio-shows/hang-the-dj/hang-the-dj-3/"),
    TrackListEntry("hang-the-dj-4", "https://www.2manybootlegs.com/radio-shows/hang-the-dj/hang-the-dj-4/"),
    TrackListEntry("hang-the-dj-5", "https://www.2manybootlegs.com/radio-shows/hang-the-dj/hang-the-dj-5/"),
    TrackListEntry("hang-the-dj-6", "https://www.2manybootlegs.com/radio-shows/hang-the-dj/hang-the-dj-6/"),
    TrackListEntry("hang-the-dj-7", "https://www.2manybootlegs.com/radio-shows/hang-the-dj/hang-the-dj-7/"),
    TrackListEntry("hang-the-dj-8", "https://www.2manybootlegs.com/radio-shows/hang-the-dj/hang-the-dj-8/"),
    TrackListEntry("hang-the-dj-9", "https://www.2manybootlegs.com/radio-shows/hang-the-dj/hang-the-dj-9/"),
    TrackListEntry("hang-the-dj-10", "https://www.2manybootlegs.com/radio-shows/hang-the-dj/hang-the-dj-10/"),
    TrackListEntry("hang-the-dj-11", "https://www.2manybootlegs.com/radio-shows/hang-the-dj/hang-the-dj-11/"),
    TrackListEntry("more-hang-the-dj-1", "https://www.2manybootlegs.com/radio-shows/more-hang-the-dj/more-hang-the-dj-1/"),
    TrackListEntry("more-hang-the-dj-2", "https://www.2manybootlegs.com/radio-shows/more-hang-the-dj/more-hang-the-dj-2/"),
    TrackListEntry("more-hang-the-dj-3", "https://www.2manybootlegs.com/radio-shows/more-hang-the-dj/more-hang-the-dj-3/"),
    TrackListEntry("more-hang-the-dj-4", "https://www.2manybootlegs.com/radio-shows/more-hang-the-dj/more-hang-the-dj-4/"),
    TrackListEntry("more-hang-the-dj-5", "https://www.2manybootlegs.com/radio-shows/more-hang-the-dj/hang-the-dj-3-5/"),
    TrackListEntry("more-hang-the-dj-6", "https://www.2manybootlegs.com/radio-shows/more-hang-the-dj/more-hang-the-dj-6/"),
    TrackListEntry("hang-the-dj-christmas-2001", "https://www.2manybootlegs.com/radio-shows/hang-the-dj-christmas-2001/"),
    TrackListEntry("mixsession-1", "https://www.2manybootlegs.com/radio-shows/other/mixsession-1/"),
    TrackListEntry("mixsession-2", "https://www.2manybootlegs.com/radio-shows/other/mixsession-2/"),
    TrackListEntry("untitled-mix-1", "https://www.2manybootlegs.com/radio-shows/other/untitled-mix-1/"),
    TrackListEntry("untitled-mix-2", "https://www.2manybootlegs.com/radio-shows/other/untitled-mix-2/"),
    #TrackListEntry("as-heard-on-radio-soulwax-2", "https://www.2manybootlegs.com/bootleg-albums/as-heard-on-radio-soulwax/part-2/"),
]


class TrackBase(BaseModel):
    artist: str
    title: str
    notes: Optional[str] = None  # e.g., remix info, version, etc.

    class Config:
        extra = 'forbid'  # Forbid extra fields
        validate_assignment = True  # Validate on assignment
        frozen = True  # Make immutable

    @field_validator('artist')
    @classmethod
    def validate_artist(cls, v):
        if not v or not v.strip():
            raise ValueError("artist must not be empty")
        return v.strip()

    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError("title must not be empty")
        return v.strip()

class Recording(TrackBase):
    pass

class MashupPart(TrackBase):
    pass

class Mashup(TrackBase):
    parts: List[MashupPart]

class TrackList(BaseModel):
    id: str  # e.g., "hank-the-dj-1"
    url: Optional[HttpUrl] = None  # URL of the tracklist page
    tracks: List[Union[Recording, Mashup]]

    class Config:
        extra = 'forbid'
        validate_assignment = True
        frozen = True

async def fetch_html(client, url):
    try:
        response = await client.get(url)
        response.raise_for_status()
        return response.text
    except httpx.HTTPError as e:
        print(f"Error fetching {url}: {e}")
        return ""

def parse_tracklist(html_content, show_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    tracklist_div = soup.find('div', class_='tracklist')
    if not tracklist_div:
        print(f"No tracklist found in {show_url}")
        return []

    tracks = []
    rows = tracklist_div.find_all('tr')
    for row in rows:
        td = row.find('td', colspan='2')
        if not td:
            continue
        # Check for mashup
        mash_title = td.find('span', class_='mashtitle')
        mash_tracks = td.find_all('span', class_='mashtrack')
        if mash_title and mash_tracks:
            mashup_name = mash_title.get_text(strip=True)
            parts = []
            for mt in mash_tracks:
                text = mt.get_text(strip=True)
                match = re.match(r'^(.*?)\s*[-–]\s*(.*)$', text)
                if match:
                    artist, title = match.groups()
                else:
                    artist, title = "N/A", text
                parts.append(MashupPart(artist=artist.strip(), title=title.strip()))
            match = re.match(r'^(.*?)\s*[-–]\s*(.*)$', mashup_name)
            if match:
                artist, title = match.groups()
            else:
                artist, title = "N/A", mashup_name
            tracks.append(Mashup(artist=artist.strip(), title=title.strip(), parts=parts))
        else:
            text = td.get_text(strip=True)
            match = re.match(r'^(.*?)\s*[-–]\s*(.*)$', text)
            if match:
                artist, title = match.groups()
            else:
                artist, title = "N/A", text
            tracks.append(Recording(artist=artist.strip(), title=title.strip()))
    return tracks

async def main():
    async with httpx.AsyncClient() as client:
        urls = [entry.url for entry in TRACKLISTS]
        tasks = [fetch_html(client, url) for url in urls]
        html_pages = await asyncio.gather(*tasks)
        for html, url in zip(html_pages, urls):
            if html:
                # Extract ID from URL, e.g., "hank-the-dj-1"
                id_match = re.search(r'/([^/]+)/?$', url.rstrip('/'))
                list_id = id_match.group(1) if id_match else "unknown"
                tracks = parse_tracklist(html, url)
                tracklist = TrackList(id=list_id, tracks=tracks)
                # Here you can process the tracklist as needed
                print(f"TrackList ID: {tracklist.id}")
                for track in tracklist.tracks:
                    if isinstance(track, Recording):
                        print(f"Recording: {track.artist} - {track.title}")
                    elif isinstance(track, Mashup):
                        print(f"Mashup: {track.artist} - {track.title}")
                        for part in track.parts:
                            print(f"  Part: {part.artist} - {part.title}")

# Run the script
if __name__ == "__main__":
    asyncio.run(main())