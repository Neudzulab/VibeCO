import argparse
import json
import pathlib
import subprocess


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a refactor impact map")
    parser.add_argument("--out", type=pathlib.Path, default=pathlib.Path("artifacts/impact.json"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    files = subprocess.check_output(["git", "diff", "--name-only", "origin/HEAD...HEAD"], text=True).splitlines()
    tests = [f for f in files if f.startswith("tests/")]
    out = {"changed": files, "tests": tests}
    args.out.parent.mkdir(exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2))
    print(f"impact map written: {args.out}")


if __name__ == "__main__":
    main()
