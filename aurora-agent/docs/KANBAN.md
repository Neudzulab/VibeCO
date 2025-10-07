# Kanban Tahtası

## Sütunlar (WIP Limitleri)
- Backlog (∞)
- Ready (10)
- In Progress (7)
- In Review (5)
- QA (4)
- Done (∞)

## Kurallar
- Bir kart `In Progress` → atanan rol/kişi zorunlu.
- `In Review` → Reviewer ≠ Implementer.
- `QA` → otomatik test + manuel kabul kriteri.
- Her kartın `Role:` alanı, `agents/roles` ile eşleşir.

## Kart Şablonu
**Title:** `<STEP-ID> Kısa açıklama`  
**Role:** `<role-id>`  
**Acceptance Criteria:** madde madde  
**Tests:** birim + entegrasyon  
**Links:** PR, ilgili RFC/Issue
