#!/usr/bin/env python3
"""YouTube Subtitle Extractor (Main)
Priority: 1 (Primary)
Method: youtube-transcript-api (Patched)

Description:
Extracts auto-generated subtitles using the youtube-transcript-api library.
Includes a patch to support non-standard versions requiring instantiation.
This is the preferred method to avoid yt-dlp rate limits.

Usage:
python yt-transcript-api.py "URL"
"""
import sys
import json
import re
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple

# 3rd party imports
try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    print("❌youtube-transcript-api not found. python -m pip install youtube-transcript-api")
    sys.exit(1)

# Windows Console Encoding Fix
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

def _find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / ".python-version").exists() or (candidate / "AGENTS.md").exists() or (candidate / ".git").exists():
            return candidate
    return start

def extract_video_id(url: str) -> Optional[str]:
    if len(url) == 11 and all(c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in url):
        return url
    patterns = [
        r"(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/shorts\/)([^&\n?#]+)",
        r"youtube\.com\/embed\/([^&\n?#]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def _serialize_translation_langs(trans_langs: List[Any]) -> List[Dict[str, str]]:
    return [
        {
            "language": getattr(lang, "language", None),
            "language_code": getattr(lang, "language_code", None),
        }
        for lang in trans_langs or []
    ]


def _serialize_available_transcripts(transcript_list: Any) -> List[Dict[str, Any]]:
    serializable = []
    try:
        for t in transcript_list:
            serializable.append(
                {
                    "language": getattr(t, "language", None),
                    "language_code": getattr(t, "language_code", None),
                    "is_generated": getattr(t, "is_generated", None),
                    "is_translatable": getattr(t, "is_translatable", None),
                }
            )
    except Exception:
        pass
    return serializable


def get_transcript(video_id: str) -> Optional[Tuple[Any, Dict[str, Any]]]:
    """Extracts transcript using patched youtube-transcript-api logic."""
    print(f"🔍 Fetching transcript for {video_id}...")
    try:
        # Try standard static method first
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        except AttributeError:
            # Fallback for non-standard version (requires instantiation)
            print("⚠️ Standard API failed, using instance method (Patched).")
            api = YouTubeTranscriptApi()
            transcript_list = api.list(video_id)

        # Find generated transcript (prefer auto-generated)
        target_transcript = None
        
        # Handle list vs TranscriptList object
        if isinstance(transcript_list, list):
             for t in transcript_list:
                is_gen = getattr(t, 'is_generated', False)
                if is_gen:
                    target_transcript = t
                    break
        else:
            for t in transcript_list:
                if t.is_generated:
                    target_transcript = t
                    break
        
        if not target_transcript:
            print("❌No auto-generated transcript found.")
            return None

        print(f"✅Found transcript: {target_transcript.language_code}")
        fetched = target_transcript.fetch()

        meta = {
            "id": video_id,
            "language": getattr(target_transcript, "language", None),
            "language_code": getattr(target_transcript, "language_code", None),
            "is_generated": getattr(target_transcript, "is_generated", None),
            "is_translatable": getattr(target_transcript, "is_translatable", None),
            "translation_languages": _serialize_translation_langs(
                getattr(target_transcript, "translation_languages", [])
            ),
            "available_transcripts": _serialize_available_transcripts(transcript_list),
            "source": "youtube-transcript-api",
            "extracted_at": datetime.now().isoformat(),
        }

        return fetched, meta

    except Exception as e:
        print(f"❌Transcript Error: {e}")
        return None

def save_to_json(data: Tuple[Any, Dict[str, Any]]):
    """Saves transcript to JSON file."""
    # Determine repo root safely (workspace root)
    script_path = Path(__file__).resolve()
    repo_root = _find_repo_root(script_path.parent)

    output_dir = repo_root / "30-collected" / "32-youtube"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    transcript_payload, meta = data
    video_id = meta.get("id", "")

    today = datetime.now().strftime("%Y%m%d")
    filename = f"{today}_{video_id}_transcript.json"
    save_path = output_dir / filename
    
    # Standardize format
    
    # Handle FetchedTranscript object (Non-standard API return)
    transcript_items = []
    if hasattr(transcript_payload, 'snippets'):
        transcript_items = transcript_payload.snippets
    elif isinstance(transcript_payload, list):
        transcript_items = transcript_payload
    else:
        # Try to iterate anyway if it looks iterable
        try:
            transcript_items = list(transcript_payload)
        except:
            pass

    # Ensure data is a list of dicts
    serializable_transcript = []
    for item in transcript_items:
        if isinstance(item, dict):
            serializable_transcript.append(item)
        else:
            # If it's an object, try to convert it to dict or use __dict__
            try:
                # Try standard dict conversion first
                serializable_transcript.append(dict(item))
            except (ValueError, TypeError):
                # Fallback: manual mapping if it has known attributes (FetchedTranscriptSnippet)
                if hasattr(item, 'text') and hasattr(item, 'start') and hasattr(item, 'duration'):
                    serializable_transcript.append({
                        "text": item.text,
                        "start": item.start,
                        "duration": item.duration
                    })
                else:
                    # Last resort: stringify
                    serializable_transcript.append(str(item))

    meta["transcript_count"] = len(serializable_transcript)
    formatted_data = {
        "meta": meta,
        "transcript": serializable_transcript
    }

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(formatted_data, f, ensure_ascii=False, indent=2)
    
    print(f"💾Saved to: {save_path}")
    return save_path

def main():
    if len(sys.argv) < 2:
        print("Usage: python yt-transcript-api.py \"URL\"")
        sys.exit(1)
        
    url = sys.argv[1]
    video_id = extract_video_id(url)
    
    if not video_id:
        print("❌Invalid URL")
        sys.exit(1)
        
    transcript = get_transcript(video_id)
    
    if transcript:
        save_to_json(transcript)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
