## Refactor Flow
- [ ] STEP-RF-001: Analyze target module and capture baseline metrics
  - owner: @TechLead
- [ ] STEP-RF-002: Lock external behaviour tests
  - owner: @QAEngineer
  - depends_on: STEP-RF-001
- [ ] STEP-RF-003: Simplify internal structure (no public API change)
  - owner: @BackendEngineerPHP
  - depends_on: STEP-RF-002
- [ ] STEP-RF-004: Validate metrics and scan for regressions
  - owner: @QAEngineer
  - depends_on: STEP-RF-003

## Plan Hygiene Improvements
- [ ] STEP-PH-001: Document the "done means locked" rule for all agents and update onboarding references
  - owner: @ProjectCoordinator
- [ ] STEP-PH-002: Add process checklists to ensure agents focus on active items (README, PLAN, AGENTS.md)
  - owner: @ProjectCoordinator
  - depends_on: STEP-PH-001
- [ ] STEP-PH-003: Implement monitoring to flag attempts to modify completed work items
  - owner: @QAEngineer
  - depends_on: STEP-PH-002
- [ ] STEP-PH-004: Run a retrospective to confirm agents no longer revisit done tasks
  - owner: @ProjectCoordinator
  - depends_on: STEP-PH-003
