<!--
  Scope: Canonical cross-agent request ledger for the Arylen orchestrator workspace.
  Last updated: Established explicit instructions for agents to log synchronization-bound requests themselves and seeded status sections.
-->

# Agents Request Ledger

This ledger captures every cross-workspace request that requires human-coordinated
synchronisation. The requesting agent must log the item here so the maintainer can
propagate it to the authoritative copy during the next sync.

## Submission checklist
- Summarise the requested change and why it matters.
- Identify the target owner or team and include relevant dependencies.
- Set the entry status to `📋 Pending` until the assignee acknowledges ownership.
- Append implementation notes (commits, tests, migrations) once the work completes.

## 📋 Pending
| ID | Request | Requested by | Target owner | Date | Notes |
|----|---------|--------------|--------------|------|-------|
| _example_ | Sync the Kanban board WIP limits with policy doc | Agent Alpha | Kanban Ops | 2025-10-23 | Link the policy section that needs alignment. |

## 🔄 In Progress
| ID | Request | Assigned to | Start date | Notes |
|----|---------|-------------|------------|-------|

## ✅ Done
| ID | Request | Completed by | Completion date | Implementation notes |
|----|---------|---------------|-----------------|----------------------|

## ❌ Rejected
| ID | Request | Reviewed by | Decision date | Rationale |
|----|---------|-------------|---------------|-----------|
