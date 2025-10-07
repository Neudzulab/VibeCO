# VibeCO
Vibe Coding Orchestrator

# Reviewer
Kod/doküman inceleme.
FILE: agents/roles/QA.md

markdown
Kodu kopyala
# QA
Test ve kalite kapısı.
FILE: .github/workflows/ci.yml

yaml
Kodu kopyala
name: ci
on:
  pull_request:
  push:
    branches: [ main, master ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: python -m pip install --upgrade pip
      - run: pip install -r requirements.txt
      - run: make ci
FILE: .github/ISSUE_TEMPLATE/agent_proposal.yml

yaml
Kodu kopyala
name: Agent Proposal (RFC)
description: Bir agent'tan öneri / plan değişikliği
title: "RFC: <kısa başlık>"
labels: ["agent", "proposal"]
body:
  - type: textarea
    attributes:
      label: Problem / Fırsat
      description: Neyi çözmek istiyoruz?
    validations:
      required: true
  - type: textarea
    attributes:
      label: Öneri
      description: Yaklaşım, kapsam ve etkiler
    validations:
      required: true
  - type: textarea
    attributes:
      label: Test Stratejisi
      description: Başarıyı nasıl doğrulayacağız?
    validations:
      required: true
FILE: .github/ISSUE_TEMPLATE/task.yml

yaml
Kodu kopyala
name: Task
description: Plan maddesine karşılık gelen iş
title: "<STEP-ID> <kısa açıklama>"
labels: ["task"]
body:
  - type: input
    attributes:
      label: STEP-ID
      description: PLAN.md'deki adım kimliği (örn. STEP-003)
    validations:
      required: true
  - type: textarea
    attributes:
      label: Kabul Kriterleri
    validations:
      required: true
  - type: textarea
    attributes:
      label: Testler
    validations:
      required: true
🚀 Git ve Yayın Komutları (örnek)
bash
Kodu kopyala
git init
git add .
git commit -m "chore: bootstrap agent plan template"

# GitHub: gh CLI varsa
gh repo create YOUR_GITHUB_USER_OR_ORG/agent-plan-template --public --source=. --push

# gh yoksa (HTTPS):
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USER_OR_ORG/agent-plan-template.git
git push -u origin main
✅ Doğrulama
bash
Kodu kopyala
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
make ci
python scripts/next.py --dry-run
python scripts/next.py --lock     # ilk adımı kilitle
python scripts/next.py            # adımı [x] yapar ve PLAN.md'yi günceller
python scripts/next.py --unlock   # kilitleri temizler

GitHub Actions’a otomatik “progress badge” güncellemesi ekleyelim.

“priority lanes” ve “blocked-by” etiketleriyle depends_on’u Issue otomasyonuna bağlayalım.
