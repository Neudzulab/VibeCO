import datetime
import json
from pathlib import Path


def badge(ok: bool) -> str:
    return "✅" if ok else "❌"


def main():
    today = datetime.date.today().isoformat()
    health = json.loads(Path("artifacts/health.json").read_text())
    logs = json.loads(Path("artifacts/logs.json").read_text())
    slo = json.loads(Path("artifacts/slo.json").read_text())
    tech = json.loads(Path("artifacts/tech.json").read_text())

    lines = [f"# Günlük Rapor — {today}"]
    lines.append(f"- Health: {badge(health['summary']['ok'])} (targets: {health['summary']['checked']})")
    lines.append(f"- Logs: {logs['count']} bulgu, worst={logs['worst']}")
    lines.append(
        f"- SLO: {badge(slo['slo_ok'])} (availability={slo['availability_pct']}%, p95={slo['p95_ms']}ms)"
    )
    lines.append(f"- Tech radar item sayısı: {len(tech['items'])}")
    lines.append("\n## Tech Radar Özet")
    for item in tech["items"][:10]:
        title = item.get("title", "")
        link = item.get("link", "")
        level = item.get("level", "assess")
        lines.append(f"- **[{level.upper()}]** {title}  {link}")
    Path("reports/daily").mkdir(parents=True, exist_ok=True)
    Path(f"reports/daily/{today}.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote reports/daily/{today}.md")


if __name__ == "__main__":
    main()
