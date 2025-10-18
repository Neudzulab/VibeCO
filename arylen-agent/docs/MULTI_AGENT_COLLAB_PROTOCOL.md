# Multi-Agent Collaboration Protocol

This document adapts the request-based collaboration flow from the myeoffice example into
an orchestra-wide standard that works for every project that plugs into the Arylen
orchestrator.  It defines how specialist agents share work safely in a monorepo without
stepping on each other while keeping humans in control of synchronization.

## Executive summary

- **Problem.** Multiple agents modifying the same repository create conflicting edits,
  hidden ownership boundaries, and no auditable history of inter-agent communication.
- **Solution.** Partition the repository into owned workspaces and coordinate changes
  exclusively through a request ledger (`AGENTS-REQUESTS.md`) that records status updates
  and implementation notes.
- **Result.** Zero-conflict collaboration, clear ownership, transparent communication, and
  repeatable sync cycles that scale to every orchestra project.

## Dual-folder workspace model

1. **Workspaces.** Each agent owns a dedicated top-level folder or git worktree. Ownership
   determines where the agent can commit code.  Cross-workspace edits require an approved
   request.
2. **Ledger hub.** A single `AGENTS-REQUESTS.md` lives in the orchestrator root. It is the
   source of truth for new requests, status transitions, and implementation summaries.
3. **Read-only visibility.** Agents may read other workspaces to understand the system, but
   write access is confined to their own workspace.  This prevents surprise overwrites and
   clarifies responsibility.
4. **Human-controlled sync.** A maintainer pulls requests from the ledger and selectively
   merges the resulting status updates back to the authoritative copy.  No agent edits
   another agent's files directly.

```
repo/
├── <project>-orchestrator/
│   ├── AGENTS-REQUESTS.md        # Canonical request log (authoritative copy)
│   ├── <agent-a>/                # Owned workspace (write access: Agent A)
│   ├── <agent-b>/                # Owned workspace (write access: Agent B)
│   └── scripts/sync-agent-requests.(ps1|sh)
└── other-projects/
```

## Request lifecycle

| Stage        | Description | Required action |
|--------------|-------------|-----------------|
| `📋 Pending` | New request logged with context, expected outputs, and dependencies. | Requesting agent updates ledger. |
| `🔄 In Progress` | Assigned agent has started work and notes the start timestamp. | Implementing agent updates status. |
| `✅ Done`    | Implementation complete. Include commit hash, affected files, breaking change callouts, and migration notes. | Implementing agent finalizes entry. |
| `❌ Rejected`| Request declined. Add rationale and alternative ideas. | Implementing agent or maintainer updates status. |

**Immutable requests.** Request text remains unchanged after submission. All follow-up
context is appended as new notes under the same entry to preserve history.

## Implementation notes section

Every completed request appends an `Implementation Notes` block that captures:

- responsible agent and hand-off date;
- commits or pull requests that fulfilled the request;
- impacted files or modules; and
- any migrations, smoke tests, or manual QA steps.

This detail allows downstream agents to audit the change before consuming it.

## Sync automation hooks

Create a lightweight sync script per project (PowerShell or shell) that:

1. Fetches the authoritative `AGENTS-REQUESTS.md` from the shared orchestration repo;
2. Merges or replaces the local copy, favoring the authoritative version when conflicts
   occur;
3. Pushes local status changes upstream only after human review; and
4. Notifies the relevant Slack/Teams channel when new requests or completions are detected.

Scripts should log each run (timestamp, operator, results) to `reports/agent-sync.log` to
maintain traceability.

## Adoption checklist for new projects

1. **Bootstrap folders.** Create dedicated workspaces for each agent under the project
   orchestrator directory.
2. **Publish CODEOWNERS.** Map each workspace path to the owning agent role.
3. **Add the ledger.** Copy `AGENTS-REQUESTS.md` template into the orchestrator root with
   starter sections for pending, in progress, done, and rejected items.
4. **Configure sync automation.** Customize `scripts/sync-agent-requests` with project
   paths and notification hooks.
5. **Train agents.** Share this protocol during onboarding and reinforce "requests only"
   collaboration during retrospectives.
6. **Measure success.** Track request throughput, average cycle time, and number of sync
   conflicts resolved manually. Target zero unsanctioned cross-workspace commits.

## Scaling guidance

- Add new agents by creating additional workspaces and CODEOWNERS rules. The protocol does
  not change as the team grows.
- Use tags in the request ledger (e.g., `[priority-high]`, `[security]`) to help agents
  triage work asynchronously.
- Archive completed requests into quarterly files (e.g., `AGENTS-REQUESTS-2025Q1.md`) to
  keep the main ledger lightweight while preserving history.
- Integrate dashboards later (Phase 4) by parsing the ledger into the reporting system
  without altering the underlying workflow.

## Human-in-the-loop guardrails

- Maintainers review ledger merges before publishing to ensure compliance with security and
  regulatory policies.
- Emergency overrides allow maintainers to pause sync scripts if suspicious changes are
  detected.
- Root-cause analyses for any unsanctioned edits feed improvements back into onboarding and
  automation scripts.

## References

- `AGENTS-REQUESTS.md` (canonical ledger template shared across projects).
- `scripts/sync-agent-requests.ps1` (PowerShell reference implementation).
- `scripts/sync-agent-requests.sh` (shell reference implementation).

By standardizing on this protocol, every Arylen-orchestrated project can scale its agent
crew with confidence, maintain a clean Git history, and guarantee traceable communication.
