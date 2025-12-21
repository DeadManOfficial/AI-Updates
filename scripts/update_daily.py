#!/usr/bin/env python3
"""Daily AI updates generator.

Usage:
  python scripts/update_daily.py --date YYYY-MM-DD
"""
import argparse
import html
import os
import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

OPENAI_RSS = "https://openai.com/blog/rss.xml"
GOOGLE_AI_RSS = "https://blog.google/technology/ai/rss/"
DEEPMIND_RSS = "https://deepmind.google/blog/rss.xml"
MITTR_RSS = "https://www.technologyreview.com/topic/artificial-intelligence/feed/"
ANTHROPIC_SITEMAP = "https://www.anthropic.com/sitemap.xml"

MAX_AGE_DAYS = 14
OPENAI_LIMIT = 10
ANTHROPIC_LIMIT = 10
GOOGLE_LIMIT = 8
DEEPMIND_LIMIT = 8
INDUSTRY_LIMIT = 6

UA = "AI-Updates/1.0"

REPLACEMENTS = {
    "\u2019": "'",
    "\u2018": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u2013": "-",
    "\u2014": "-",
    "\u2026": "...",
}


def clean_text(text):
    if text is None:
        return None
    text = html.unescape(text)
    for k, v in REPLACEMENTS.items():
        text = text.replace(k, v)
    text = re.sub(r"\s+", " ", text).strip()
    text = text.encode("ascii", "ignore").decode("ascii")
    return text


def strip_html(text):
    if not text:
        return None
    return re.sub(r"<[^>]+>", " ", text)


def fetch_url(url):
    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=30) as resp:
        return resp.read()


def parse_date(value):
    if not value:
        return None
    value = value.strip()
    try:
        dt = parsedate_to_datetime(value)
        if dt and dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        pass
    try:
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        dt = datetime.fromisoformat(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None


def localname(tag):
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def find_child_text(el, names):
    for child in el:
        if localname(child.tag) in names and child.text:
            return child.text
    return None


def find_child_link(el):
    for child in el:
        if localname(child.tag) == "link":
            href = child.attrib.get("href")
            if href:
                return href
            if child.text:
                return child.text
    return None


def parse_feed(url, limit):
    items = []
    xml_bytes = fetch_url(url)
    root = ET.fromstring(xml_bytes)
    tag = localname(root.tag)
    if tag == "rss":
        channel = root.find("channel") or root.find("{*}channel")
        if channel is None:
            return items
        entries = channel.findall("item")
        for e in entries[:limit]:
            title = find_child_text(e, {"title"})
            link = find_child_text(e, {"link"})
            pub = find_child_text(e, {"pubDate", "published", "updated"})
            desc = find_child_text(e, {"description"})
            dt = parse_date(pub or "")
            items.append({
                "title": clean_text(title),
                "link": link,
                "published": dt,
                "description": clean_text(strip_html(desc) or ""),
            })
    elif tag == "feed":
        entries = root.findall("{*}entry")
        for e in entries[:limit]:
            title = find_child_text(e, {"title"})
            link = find_child_link(e)
            pub = find_child_text(e, {"published", "updated"})
            desc = find_child_text(e, {"summary", "content"})
            dt = parse_date(pub or "")
            items.append({
                "title": clean_text(title),
                "link": link,
                "published": dt,
                "description": clean_text(strip_html(desc) or ""),
            })
    return items


def filter_recent(items, now, max_age_days):
    out = []
    for it in items:
        dt = it.get("published")
        if dt is None:
            continue
        age = (now - dt.astimezone(timezone.utc)).days
        if age <= max_age_days:
            out.append(it)
    out.sort(key=lambda x: x.get("published") or now, reverse=True)
    return out


def fetch_meta_description(url):
    try:
        html_bytes = fetch_url(url)
        html_text = html_bytes.decode("utf-8", errors="replace")
        m = re.search(r'<meta[^>]+property="og:description"[^>]+content="([^"]+)"', html_text)
        if not m:
            m = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', html_text)
        if m:
            return clean_text(m.group(1))
    except Exception:
        return None
    return None


def fetch_meta_title(url):
    try:
        html_bytes = fetch_url(url)
        html_text = html_bytes.decode("utf-8", errors="replace")
        m = re.search(r'<title>(.*?)</title>', html_text, re.S)
        if m:
            title = clean_text(m.group(1))
            if title and "\\" in title:
                title = title.replace("\\", "|")
            return title
    except Exception:
        return None
    return None


def clean_title_suffix(title):
    if not title:
        return None
    title = title.replace("\\", "|")
    for suffix in [" | Anthropic", " | OpenAI", " | Google", " | Google DeepMind"]:
        if title.endswith(suffix):
            return title[: -len(suffix)].strip()
    return title


def fetch_anthropic_news(now, limit, max_age_days):
    entries = []
    xml_bytes = fetch_url(ANTHROPIC_SITEMAP)
    root = ET.fromstring(xml_bytes)
    ns = ""
    if root.tag.startswith("{"):
        ns = root.tag.split("}")[0] + "}"
    for url in root.findall(f"{ns}url"):
        loc = url.find(f"{ns}loc")
        lastmod = url.find(f"{ns}lastmod")
        if loc is None or not loc.text:
            continue
        if "/news/" not in loc.text:
            continue
        dt = parse_date(lastmod.text if lastmod is not None else "")
        if dt is None:
            continue
        age = (now - dt.astimezone(timezone.utc)).days
        if age > max_age_days:
            continue
        entries.append({"link": loc.text, "published": dt})

    entries.sort(key=lambda x: x.get("published") or now, reverse=True)
    entries = entries[:limit]

    for it in entries:
        title = fetch_meta_title(it["link"]) or it["link"].rstrip("/").split("/")[-1]
        it["title"] = clean_title_suffix(title)
        it["description"] = None
    return entries


def format_date(dt):
    if not dt:
        return "n/a"
    return dt.astimezone(timezone.utc).date().isoformat()


def build_focus(openai_items, anthropic_items, google_items, sora_items):
    parts = []
    if openai_items:
        parts.append("OpenAI: " + (openai_items[0].get("title") or "update"))
    if anthropic_items:
        parts.append("Anthropic: " + (anthropic_items[0].get("title") or "update"))
    if google_items:
        parts.append("Google: " + (google_items[0].get("title") or "update"))
    if sora_items:
        parts.append("Sora 2: " + (sora_items[0].get("title") or "update"))
    focus = "; ".join(parts)
    if len(focus) > 140:
        focus = focus[:137] + "..."
    return focus or "Daily AI briefing"


def write_section(lines, title, items):
    lines.append("## " + title)
    if not items:
        lines.append("- No recent updates found in the last %d days." % MAX_AGE_DAYS)
        lines.append("")
        return
    for it in items:
        date_str = format_date(it.get("published"))
        line = "- %s - [%s](%s)" % (date_str, it.get("title") or "Update", it.get("link"))
        desc = it.get("description")
        if desc:
            line += " - " + desc
        lines.append(line)
    lines.append("")


def write_index(updates_dir, date_str, focus):
    entries = []
    for path in sorted(updates_dir.glob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        entries.append(path.stem)
    entries = sorted(entries, reverse=True)

    lines = ["# Updates Index", "", "| Date | Focus | File |", "| --- | --- | --- |"]
    for d in entries:
        if d == date_str:
            focus_text = focus
        else:
            focus_text = "Daily AI briefing"
        lines.append("| %s | %s | [%s](./%s.md) |" % (d, focus_text, d, d))
    (updates_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="ascii")


def update_root_readme(root, date_str):
    readme = root / "README.md"
    if not readme.exists():
        return
    text = readme.read_text(encoding="ascii")
    text = re.sub(r"\(\./updates/\d{4}-\d{2}-\d{2}\.md\)", "(./updates/%s.md)" % date_str, text)
    readme.write_text(text, encoding="ascii")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="Override date as YYYY-MM-DD")
    args = parser.parse_args()

    now_utc = datetime.now(timezone.utc)
    if args.date:
        date_str = args.date
    else:
        date_str = now_utc.date().isoformat()

    root = Path(__file__).resolve().parents[1]
    updates_dir = root / "updates"
    updates_dir.mkdir(parents=True, exist_ok=True)

    errors = []
    openai_items = []
    google_items = []
    deepmind_items = []
    mittr_items = []

    try:
        openai_items = parse_feed(OPENAI_RSS, OPENAI_LIMIT)
        openai_items = filter_recent(openai_items, now_utc, MAX_AGE_DAYS)
        for it in openai_items:
            if it.get("link"):
                it["description"] = fetch_meta_description(it["link"]) or it.get("description")
    except Exception as exc:
        errors.append("OpenAI RSS failed: %s" % exc)

    try:
        google_items = parse_feed(GOOGLE_AI_RSS, GOOGLE_LIMIT)
        google_items = filter_recent(google_items, now_utc, MAX_AGE_DAYS)
        for it in google_items:
            if it.get("link"):
                it["description"] = fetch_meta_description(it["link"]) or it.get("description")
    except Exception as exc:
        errors.append("Google AI RSS failed: %s" % exc)

    try:
        deepmind_items = parse_feed(DEEPMIND_RSS, DEEPMIND_LIMIT)
        deepmind_items = filter_recent(deepmind_items, now_utc, MAX_AGE_DAYS)
        for it in deepmind_items:
            if it.get("link"):
                it["description"] = fetch_meta_description(it["link"]) or it.get("description")
    except Exception as exc:
        errors.append("DeepMind RSS failed: %s" % exc)

    try:
        mittr_items = parse_feed(MITTR_RSS, INDUSTRY_LIMIT)
        mittr_items = filter_recent(mittr_items, now_utc, MAX_AGE_DAYS)
        for it in mittr_items:
            if it.get("link"):
                it["description"] = fetch_meta_description(it["link"]) or it.get("description")
    except Exception as exc:
        errors.append("MIT TR RSS failed: %s" % exc)

    try:
        anthropic_items = fetch_anthropic_news(now_utc, ANTHROPIC_LIMIT, MAX_AGE_DAYS)
    except Exception as exc:
        anthropic_items = []
        errors.append("Anthropic sitemap failed: %s" % exc)

    sora_items = []
    for it in openai_items:
        title = it.get("title") or ""
        if "sora" in title.lower():
            sora_items.append(it)

    google_combined = google_items + deepmind_items
    seen = set()
    deduped = []
    for it in google_combined:
        link = it.get("link")
        if not link or link in seen:
            continue
        seen.add(link)
        deduped.append(it)
    deduped.sort(key=lambda x: x.get("published") or now_utc, reverse=True)
    google_combined = deduped

    focus = build_focus(openai_items, anthropic_items, google_combined, sora_items)

    lines = []
    lines.append("# AI Updates Daily Briefing - %s" % date_str)
    lines.append("")
    lines.append("As of: %s (local) | Generated UTC: %s" % (date_str, now_utc.isoformat()))
    lines.append("")
    lines.append("## Executive Summary")
    lines.append("- OpenAI: %d updates" % len(openai_items))
    lines.append("- Sora 2: %d updates" % len(sora_items))
    lines.append("- Anthropic / Claude: %d updates" % len(anthropic_items))
    lines.append("- Google / Gemini: %d updates" % len(google_combined))
    lines.append("- Industry highlights: %d items" % len(mittr_items))
    lines.append("")

    write_section(lines, "OpenAI", openai_items)
    write_section(lines, "Sora 2", sora_items)
    write_section(lines, "Anthropic / Claude", anthropic_items)
    write_section(lines, "Google / Gemini", google_combined)
    write_section(lines, "Industry Highlights", mittr_items)

    lines.append("## Coverage Notes")
    lines.append("- Anthropic dates use sitemap lastmod values (official feed unavailable).")
    if errors:
        for err in errors:
            lines.append("- %s" % clean_text(err))
    else:
        lines.append("- All primary sources fetched successfully.")
    lines.append("")

    lines.append("## Sources")
    lines.append("- OpenAI Blog: https://openai.com/blog")
    lines.append("- Anthropic News: https://www.anthropic.com/news")
    lines.append("- Google AI Blog: https://blog.google/technology/ai/")
    lines.append("- DeepMind Blog: https://deepmind.google/blog/")
    lines.append("- MIT Technology Review AI: https://www.technologyreview.com/topic/artificial-intelligence/")
    lines.append("")

    out_path = updates_dir / (date_str + ".md")
    out_path.write_text("\n".join(lines) + "\n", encoding="ascii")

    write_index(updates_dir, date_str, focus)
    update_root_readme(root, date_str)


if __name__ == "__main__":
    main()
