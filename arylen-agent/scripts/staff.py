#!/usr/bin/env python
"""
Amaç:
- `project/spec.yaml` içindeki kuralları okuyarak `agents/roster.yaml` için önerilen ekip
  kadrosunu üretir ve isteğe bağlı olarak CODEOWNERS listesini günceller.

Ana Akış:
- `main` CLI bağımsız değişkenlerini ayrıştırır ve yapılandırmayı `load_spec` ile okur.
- `compute_team_counts`, ölçekleme ve kısıt parametrelerini kullanarak rol başına kişi
  sayısını hesaplar; üst limit aşıldığında `balance_team` ile öncelik sırasına göre
  azaltım yapar.
- `build_roster`, rol adlarını ve beceri eşlemlerini kullanarak YAML çıktısını
  yapılandırır, `write_roster` dosyaya yazar ve `--codeowners` seçildiğinde
  `scripts/gen_codeowners.py` ile CODEOWNERS dosyasını yeniler.

İlgili Testler:
- Otomatik test bulunmuyor; çıktıyı doğrulamak için render edilen `agents/roster.yaml`
  ve CODEOWNERS dosyalarının gözlemi gerekir.
"""
from __future__ import annotations

import argparse
import math
import pathlib
import subprocess
import sys
from typing import Dict, List

import yaml

SPEC_PATH = pathlib.Path("project/spec.yaml")
ROSTER_PATH = pathlib.Path("agents/roster.yaml")

ROLE_NAME_MAP = {
    "product_manager": "ProductManager",
    "engineering_manager": "EngineeringManager",
    "tech_lead": "TechLead",
    "ux_ui_designer": "UXUIDesigner",
    "frontend_engineer": "FrontendEngineer",
    "backend_engineer_php": "BackendEngineerPHP",
    "backend_engineer_python": "BackendEngineerPython",
    "devops_engineer": "DevOpsEngineer",
    "data_engineer": "DataEngineer",
    "ml_engineer": "MLEngineer",
    "qa_engineer": "QAEngineer",
    "sre_engineer": "SREEngineer",
    "security_engineer": "SecurityEngineer",
}

SENIORITY_OVERRIDES = {
    "CTO": "exec",
    "EngineeringManager": "senior",
    "TechLead": "principal",
}

SKILL_MAP = {
    "CTO": ["vision", "architecture", "risk_management"],
    "EngineeringManager": ["resource_planning", "delivery_coaching", "feedback"],
    "TechLead": ["architecture", "code_standards", "technical_reviews"],
    "ProductManager": ["roadmapping", "stakeholder_alignment", "analytics"],
    "UXUIDesigner": ["research", "prototyping", "design_systems"],
    "FrontendEngineer": ["react", "typescript", "testing"],
    "BackendEngineerPHP": ["php82", "framework_design", "api_security"],
    "BackendEngineerPython": ["python", "asyncio", "data_services"],
    "DevOpsEngineer": ["ci_cd", "iac", "containers"],
    "DataEngineer": ["etl", "data_modeling", "workflow_automation"],
    "MLEngineer": ["model_serving", "evaluation", "monitoring"],
    "QAEngineer": ["automation", "e2e", "quality_gates"],
    "SREEngineer": ["observability", "incident_response", "slo_management"],
    "SecurityEngineer": ["appsec", "threat_modeling", "compliance"],
}

REDUCTION_PRIORITY = [
    "qa_engineer",
    "sre_engineer",
    "security_engineer",
    "data_engineer",
    "ml_engineer",
    "frontend_engineer",
    "backend_engineer_php",
    "backend_engineer_python",
    "ux_ui_designer",
    "product_manager",
    "engineering_manager",
    "tech_lead",
]


class StaffingError(RuntimeError):
    """Raised when staffing cannot be generated."""


def load_spec() -> dict:
    if not SPEC_PATH.exists():
        raise StaffingError("project/spec.yaml not found")
    return yaml.safe_load(SPEC_PATH.read_text(encoding="utf-8"))


def compute_team_counts(spec: dict) -> Dict[str, int]:
    rules = spec["definitions"]["staffing_rules"]
    base_team = dict(rules["base_team"])

    complexity_factor = rules["multipliers"]["complexity"][spec["scaling"]["complexity"]]
    budget_factor = rules["multipliers"]["budget_level"][spec["constraints"]["budget_level"]]
    risk_map = rules["multipliers"]["risk_profile"][spec["constraints"]["risk_profile"]]

    team: Dict[str, int] = {}
    for role_key, base_count in base_team.items():
        multiplier = complexity_factor * budget_factor
        if role_key in risk_map:
            multiplier *= risk_map[role_key]
        count = max(1, int(math.ceil(base_count * multiplier)))
        team[role_key] = count

    # Ensure executive oversight
    team["cto"] = 1

    cap = spec["scaling"]["team_max"]
    total_people = sum(team.values())
    if total_people > cap:
        team = balance_team(team, cap)
    return team


def balance_team(team: Dict[str, int], cap: int) -> Dict[str, int]:
    adjusted = dict(team)
    idx = 0
    priority_cycle = REDUCTION_PRIORITY
    while sum(adjusted.values()) > cap and idx < len(priority_cycle):
        role = priority_cycle[idx]
        if role in adjusted and adjusted[role] > 1:
            adjusted[role] -= 1
        else:
            idx += 1
    if sum(adjusted.values()) > cap:
        raise StaffingError("Unable to fit team within cap without removing essential roles")
    return adjusted


def build_roster(team_counts: Dict[str, int]) -> List[dict]:
    roster_entries: List[dict] = []
    for key, count in sorted(team_counts.items(), key=lambda item: ROLE_NAME_MAP.get(item[0], item[0])):
        if key == "cto":
            role_name = "CTO"
        else:
            role_name = ROLE_NAME_MAP[key]
        entry = {
            "role": role_name,
            "count": int(count),
            "seniority": SENIORITY_OVERRIDES.get(role_name, "senior"),
            "skills": SKILL_MAP.get(role_name, []),
        }
        roster_entries.append(entry)
    return roster_entries


def write_roster(roster: List[dict]) -> None:
    data = {"team": roster}
    ROSTER_PATH.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def run_codeowners() -> None:
    subprocess.check_call([sys.executable, "scripts/gen_codeowners.py"])


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate staffing roster")
    parser.add_argument(
        "--codeowners",
        action="store_true",
        help="Generate CODEOWNERS after producing the roster",
    )
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    spec = load_spec()
    team_counts = compute_team_counts(spec)
    roster = build_roster(team_counts)
    write_roster(roster)
    print(f"Wrote {ROSTER_PATH}")

    if args.codeowners:
        run_codeowners()
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
