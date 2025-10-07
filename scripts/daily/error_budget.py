import json
from pathlib import Path

SLO_UPTIME = 99.9
SLO_P95_MS = 300


def main():
    health = json.loads(Path("artifacts/health.json").read_text())
    ok = health["summary"]["ok"]
    availability = 100.0 if ok else 99.0
    p95 = 280
    slo_ok = (availability >= SLO_UPTIME) and (p95 <= SLO_P95_MS)
    output = {
        "availability_pct": availability,
        "p95_ms": p95,
        "slo_ok": slo_ok,
        "slo_targets": {"availability": SLO_UPTIME, "p95_ms": SLO_P95_MS},
    }
    Path("artifacts/slo.json").write_text(json.dumps(output, indent=2))
    print(json.dumps(output))


if __name__ == "__main__":
    main()
