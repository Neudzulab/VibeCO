import argparse, json, subprocess, sys, re, pathlib

API_PATTERN = re.compile(r'^(public|export)\s', re.M)

def changed_files():
    out = subprocess.check_output(["git", "diff", "--name-only", "origin/HEAD...HEAD"], text=True)
    return [x for x in out.splitlines() if x.strip()]


def grep_api_changes(paths):
    count = 0
    for p in paths:
        if not p.endswith((".py", ".php", ".ts", ".js")):
            continue
        text = pathlib.Path(p).read_text(errors="ignore")
        # heuristic API hint: count public/export declarations
        count += len(API_PATTERN.findall(text))
    return count


def coverage_ok(min_cov: int):
    # read the pytest --cov report (xml or summary). Assume a summary file for now:
    summary_path = pathlib.Path(".coverage-summary")
    s = summary_path.read_text() if summary_path.exists() else ""
    m = re.search(r"TOTAL\s+(\d+)%", s)
    if not m:
        return False, 0
    cov = int(m.group(1))
    return cov >= min_cov, cov


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--coverage-min", type=int, required=True)
    ap.add_argument("--max-public-api-changes", type=int, default=0)
    args = ap.parse_args()

    files = changed_files()
    api_count = grep_api_changes(files)
    ok_cov, cov = coverage_ok(args.coverage_min)

    result = {"api_count": api_count, "coverage": cov, "coverage_min": args.coverage_min}
    print(json.dumps(result, indent=2))

    errors = []
    if api_count > args.max_public_api_changes:
        errors.append(f"Public API change hints: {api_count} > {args.max_public_api_changes}")
    if not ok_cov:
        errors.append(f"Coverage {cov}% < {args.coverage_min}%")

    if errors:
        for error in errors:
            print("ERROR:", error, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
