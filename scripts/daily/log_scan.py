import datetime
import json
import re
from pathlib import Path

import yaml


def subst(datefmt: str, current: datetime.date) -> str:
    yesterday = current - datetime.timedelta(days=1)
    return (
        datefmt.replace("${YYYY}", f"{current.year:04d}")
        .replace("${MM}", f"{current.month:02d}")
        .replace("${DD}", f"{current.day:02d}")
        .replace("${DD-1}", f"{yesterday.day:02d}")
    )


def scan_file(path: str, patterns):
    findings = []
    file_path = Path(path)
    if not file_path.exists():
        return findings
    text = file_path.read_text(errors="ignore")
    for severity, pats in patterns.items():
        for pattern in pats:
            for match in re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE):
                start = max(0, match.start() - 80)
                end = min(len(text), match.end() + 80)
                findings.append(
                    {
                        "severity": severity,
                        "pattern": pattern,
                        "sample": text[start:end],
                    }
                )
    return findings


def main():
    cfg = yaml.safe_load(Path("configs/log_rules.yaml").read_text())
    today = datetime.date.today()
    patterns = {key: val for key, val in cfg.get("rules", {}).items()}
    all_findings = []
    for source in cfg.get("sources", []):
        path = subst(source["path"], today)
        all_findings.extend(scan_file(path, patterns))
    severity_rank = {"critical": 3, "security": 3, "high": 2}
    worst = max([severity_rank.get(item["severity"], 1) for item in all_findings], default=0)
    output = {"count": len(all_findings), "worst": worst, "items": all_findings}
    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/logs.json").write_text(json.dumps(output, indent=2))
    print(json.dumps(output))


if __name__ == "__main__":
    main()
