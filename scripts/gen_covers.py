#!/usr/bin/env python3
"""Generate cover images for blog posts using Gemini API."""

import os
import sys
import json
import base64
import urllib.request

POSTS_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "blog", "posts")
COVERS_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "assets", "images", "blog", "covers")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent"


def extract_frontmatter(content):
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    fm = {}
    for line in parts[1].strip().split("\n"):
        if ":" in line and not line.startswith("  "):
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip().strip('"')
    return fm, parts[2]


def gen_cover(api_key, title, body_snippet):
    """Call Gemini to generate a cover image."""
    prompt = (
        f"Generate a modern, clean tech blog cover image for an article titled '{title}'. "
        f"The article is about: {body_snippet[:300]}. "
        "Style: minimalist gradient background, subtle tech-themed abstract shapes or icons, "
        "no text on the image, 16:9 aspect ratio, suitable as a blog thumbnail. "
        "Color palette: blue and white tones with subtle accents."
    )

    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
        },
    }).encode()

    req = urllib.request.Request(
        f"{GEMINI_URL}?key={api_key}",
        data=payload,
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = json.loads(resp.read())

        for part in data.get("candidates", [{}])[0].get("content", {}).get("parts", []):
            if "inlineData" in part:
                img_data = base64.b64decode(part["inlineData"]["data"])
                mime = part["inlineData"].get("mimeType", "image/png")
                ext = "png" if "png" in mime else "jpg"
                return img_data, ext

    except urllib.error.HTTPError as e:
        body = e.read().decode() if hasattr(e, 'read') else str(e)
        print(f"  API error {e.code}: {body[:300]}")
    except Exception as e:
        print(f"  Error: {e}")
    return None, None


def slug_from_fm(fm, fname):
    """Get slug from frontmatter or filename."""
    if fm.get("slug"):
        return fm["slug"]
    # Derive from filename
    name = os.path.splitext(fname)[0]
    # Remove date prefix
    parts = name.split("-", 3)
    if len(parts) >= 4 and parts[0].isdigit():
        return parts[3]
    return name


def main():
    api_key = os.environ.get("GEMINI_API_KEY") or (sys.argv[1] if len(sys.argv) > 1 else None)
    if not api_key:
        print("Usage: GEMINI_API_KEY=xxx python gen_covers.py")
        sys.exit(1)

    os.makedirs(COVERS_DIR, exist_ok=True)
    posts_dir = os.path.abspath(POSTS_DIR)
    generated = 0

    for fname in sorted(os.listdir(posts_dir)):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(posts_dir, fname)
        with open(fpath, "r") as f:
            content = f.read()

        fm, body = extract_frontmatter(content)
        if not fm.get("date"):
            continue

        slug = slug_from_fm(fm, fname)
        # Check if cover already exists
        for ext in ["png", "jpg"]:
            if os.path.exists(os.path.join(COVERS_DIR, f"{slug}.{ext}")):
                print(f"SKIP {fname} (cover exists)")
                slug = None
                break
        if not slug:
            continue

        title = fm.get("title", fname)
        # Use first H1 as title if not in frontmatter
        for line in body.split("\n"):
            if line.startswith("# "):
                title = line[2:].strip()
                break

        print(f"Generating cover for: {title}...")
        img_data, ext = gen_cover(api_key, title, body[:500])
        if img_data:
            out_path = os.path.join(COVERS_DIR, f"{slug}.{ext}")
            with open(out_path, "wb") as f:
                f.write(img_data)
            print(f"  Saved: covers/{slug}.{ext} ({len(img_data)} bytes)")
            generated += 1
        else:
            print(f"  Failed to generate")

    print(f"\nDone. Generated {generated} covers.")
    if generated > 0:
        print(f"Covers saved to: {os.path.abspath(COVERS_DIR)}")


if __name__ == "__main__":
    main()
