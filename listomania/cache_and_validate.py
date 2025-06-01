import asyncio
import httpx
import os
from pathlib import Path
from listomania.main import TRACKLISTS, parse_tracklist, TrackList

CACHE_DIR = Path(__file__).parent.parent / "html_cache"
CACHE_DIR.mkdir(exist_ok=True)

async def fetch_and_cache(client, entry):
    html_path = CACHE_DIR / f"{entry.id}.html"
    if html_path.exists():
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
    else:
        try:
            resp = await client.get(str(entry.url))
            resp.raise_for_status()
            html = resp.text
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html)
        except Exception as e:
            print(f"Error fetching {entry.url}: {e}")
            html = ""
    return entry, html

async def main():
    async with httpx.AsyncClient() as client:
        tasks = [fetch_and_cache(client, entry) for entry in TRACKLISTS]
        results = await asyncio.gather(*tasks)
    all_passed = True
    for entry, html in results:
        if not html:
            print(f"[FAIL] {entry.id}: No HTML fetched.")
            all_passed = False
            continue
        try:
            tracks = parse_tracklist(html, entry.url)
            TrackList(id=entry.id, url=entry.url, tracks=tracks)
            print(f"[PASS] {entry.id}")
        except Exception as e:
            print(f"[FAIL] {entry.id}: {e}")
            all_passed = False
    if all_passed:
        print("All tracklists validated successfully.")
    else:
        print("Some tracklists failed validation.")

if __name__ == "__main__":
    asyncio.run(main())
