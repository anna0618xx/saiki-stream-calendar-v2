#!/usr/bin/env python3
"""Collect public stream metadata for Usami Rito using YouTube Data API v3."""
import datetime as dt
import json
import os
import pathlib
import urllib.parse
import urllib.request
import urllib.error

CHANNEL_ID = "UCambvP8yxNDot4FzQc9cgiw"
OUT = pathlib.Path("data/usami-streams.json")
KEY = os.environ.get("YOUTUBE_API_KEY", "")
BASE = "https://www.googleapis.com/youtube/v3/"

def request(resource, **params):
    params["key"] = KEY
    url = BASE + resource + "?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=35) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        # Show Google's error code/message, but never print the API key or URL.
        try:
            payload = json.loads(exc.read().decode("utf-8"))
            err = payload.get("error", {})
            code = err.get("code", exc.code)
            message = str(err.get("message", "Unknown API error"))
            reason = ", ".join(str(v.get("reason", "")) for v in err.get("errors", []))
        except (ValueError, UnicodeError):
            code, message, reason = exc.code, "Unparseable API error", ""
        # Secrets are masked by Actions, and additionally redacted here.
        message = message.replace(KEY, "[REDACTED]") if KEY else message
        raise RuntimeError(f"YouTube API {resource}: HTTP {code}, reason={reason}, message={message}") from None

def collect_ids():
    response = request("channels", part="contentDetails", id=CHANNEL_ID)
    channel = response.get("items", [])
    if not channel:
        raise RuntimeError("Channel not found")
    playlist = channel[0]["contentDetails"]["relatedPlaylists"]["uploads"]
    ids = set()
    page = None
    # Last ~500 uploads, covering current and historical recent months.
    for _ in range(10):
        p = {"part": "contentDetails", "playlistId": playlist, "maxResults": 50}
        if page:
            p["pageToken"] = page
        data = request("playlistItems", **p)
        ids.update(x["contentDetails"]["videoId"] for x in data.get("items", []) if x.get("contentDetails", {}).get("videoId"))
        page = data.get("nextPageToken")
        if not page:
            break
    # Upcoming and currently live items may not appear in uploads playlist.
    for event in ("upcoming", "live"):
        page = None
        for _ in range(2):
            p = {"part": "id", "channelId": CHANNEL_ID, "type": "video", "eventType": event, "maxResults": 50}
            if page:
                p["pageToken"] = page
            data = request("search", **p)
            ids.update(x["id"]["videoId"] for x in data.get("items", []) if x.get("id", {}).get("videoId"))
            page = data.get("nextPageToken")
            if not page:
                break
    return ids

def main():
    if not KEY:
        raise RuntimeError("Set YOUTUBE_API_KEY in GitHub Actions secrets")
    found = collect_ids()
    streams = {}
    for ids in (list(found)[n:n+50] for n in range(0, len(found), 50)):
        data = request("videos", part="snippet,liveStreamingDetails", id=",".join(ids), maxResults=50)
        for item in data.get("items", []):
            details = item.get("liveStreamingDetails")
            if not details:
                continue
            snippet = item.get("snippet", {})
            if snippet.get("channelId") != CHANNEL_ID:
                continue
            start = details.get("actualStartTime") or details.get("scheduledStartTime")
            if not start:
                continue
            status = "ended" if details.get("actualEndTime") else ("live" if details.get("actualStartTime") else "upcoming")
            streams[item["id"]] = {
                "videoId": item["id"],
                "title": snippet.get("title", "配信"),
                "start": start,
                "end": details.get("actualEndTime"),
                "status": status,
            }
    # Merge previously captured streams to avoid losing older history when it
    # falls outside the uploads scan. Do not keep deleted/private duplicates.
    if OUT.exists():
        try:
            prior = json.loads(OUT.read_text(encoding="utf-8"))
            for s in prior.get("streams", []):
                if s.get("videoId") not in found and s.get("status") == "ended":
                    streams.setdefault(s["videoId"], s)
        except (ValueError, KeyError, TypeError):
            pass
    output = {
        "generatedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "channelId": CHANNEL_ID,
        "streams": sorted(streams.values(), key=lambda s: s["start"]),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {len(output['streams'])} public livestreams")

if __name__ == "__main__":
    main()
