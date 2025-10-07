import os
import time
import yaml
import json
import requests
from pathlib import Path


def getenv_expand(value: str) -> str:
    """Replace ${VAR} placeholders using environment variables."""
    if not isinstance(value, str):
        return value
    out = value
    for key, val in os.environ.items():
        out = out.replace("${" + key + "}", val)
    return out


def check_target(target):
    url = getenv_expand(target["url"])
    method = target.get("method", "GET").upper()
    headers = {key: getenv_expand(val) for key, val in target.get("headers", {}).items()}
    try:
        response = requests.request(method, url, headers=headers, timeout=10)
        ok = response.status_code == target["expect"]["status"]
        body = response.text[:2000]
        contains = target["expect"].get("contains")
        contains_any = target["expect"].get("contains_any", [])
        if contains:
            ok = ok and (contains in body)
        if contains_any:
            ok = ok and any(item in body for item in contains_any)
        return {
            "name": target["name"],
            "ok": ok,
            "status": response.status_code,
            "sample": body[:200],
        }
    except Exception as exc:
        return {"name": target["name"], "ok": False, "error": str(exc)}


def main():
    cfg = yaml.safe_load(Path("configs/prod_targets.yaml").read_text())
    results = [check_target(target) for target in cfg.get("targets", [])]
    summary = {"ok": all(result.get("ok") for result in results), "checked": len(results)}
    output = {"summary": summary, "results": results, "ts": int(time.time())}
    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/health.json").write_text(json.dumps(output, indent=2))
    print(json.dumps(output))


if __name__ == "__main__":
    main()
