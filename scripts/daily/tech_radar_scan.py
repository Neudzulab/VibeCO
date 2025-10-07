import json
from pathlib import Path

import feedparser
import requests
import yaml


def main():
    cfg = yaml.safe_load(Path("configs/tech_feeds.yaml").read_text())
    items = []
    for feed in cfg.get("feeds", []):
        url = feed["url"]
        try:
            if url.endswith((".rss", ".atom")) or "feed" in url or "rss" in url:
                parsed = feedparser.parse(url)
                entries = parsed.entries[: cfg.get("max_items_per_feed", 10)]
                for entry in entries:
                    title = getattr(entry, "title", "")
                    link = getattr(entry, "link", "")
                    stage = "assess"
                    haystack = " ".join(
                        [
                            title.lower(),
                            getattr(entry, "summary", "").lower(),
                        ]
                    )
                    keywords = cfg.get("keywords", {})
                    if any(keyword.lower() in haystack for keyword in keywords.get("adopt", [])):
                        stage = "adopt"
                    elif any(keyword.lower() in haystack for keyword in keywords.get("trial", [])):
                        stage = "trial"
                    items.append({"feed": feed["name"], "title": title, "link": link, "level": stage})
            else:
                response = requests.get(url, timeout=cfg.get("timeout_seconds", 20))
                items.append(
                    {
                        "feed": feed["name"],
                        "title": f"Fetched {len(response.text)} chars",
                        "link": url,
                        "level": "assess",
                    }
                )
        except Exception as exc:
            items.append({"feed": feed["name"], "error": str(exc)})
    Path("artifacts/tech.json").write_text(json.dumps({"items": items}, indent=2))
    print(json.dumps({"count": len(items)}))


if __name__ == "__main__":
    main()
