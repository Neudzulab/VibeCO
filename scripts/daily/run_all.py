import subprocess
import sys
from pathlib import Path


COMMANDS = [
    [sys.executable, "scripts/daily/health_check.py"],
    [sys.executable, "scripts/daily/log_scan.py"],
    [sys.executable, "scripts/daily/error_budget.py"],
    [sys.executable, "scripts/daily/tech_radar_scan.py"],
    [sys.executable, "scripts/daily/post_report.py"],
    [sys.executable, "scripts/daily/notify.py"],
]


def run(cmd):
    print("+", " ".join(cmd))
    subprocess.check_call(cmd)


def main():
    Path("artifacts").mkdir(exist_ok=True)
    for cmd in COMMANDS:
        try:
            run(cmd)
        except subprocess.CalledProcessError as exc:
            print(f"Command failed: {cmd} -> {exc}")
            if cmd[-1].endswith("notify.py"):
                continue
            raise


if __name__ == "__main__":
    main()
