import json
import os
from pathlib import Path

import requests


def main():
    webhook = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook:
        print("No SLACK_WEBHOOK_URL; skip.")
        return
    slo = json.loads(Path("artifacts/slo.json").read_text())
    if not slo["slo_ok"]:
        requests.post(
            webhook,
            json={
                "text": f"[ALERT] SLO ihlali: availability={slo['availability_pct']} p95={slo['p95_ms']}ms",
            },
            timeout=10,
        )
        print("Slack alerted.")
    else:
        print("SLO OK; no alert.")


if __name__ == "__main__":
    main()
