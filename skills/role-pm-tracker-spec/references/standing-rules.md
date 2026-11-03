# SaaS Team Standing Rules & Guardrails

Read `PROJECT-CONTEXT.md` at the start of every session. Where a skill rule and `PROJECT-CONTEXT.md` disagree, `PROJECT-CONTEXT.md` wins.

## 1. Universal Team Rules
1. **Only the Founder/Owner approves.** No agent approves its own work or another agent's work on the owner's behalf. Every approval is logged in the project's Approvals log with the owner's verbatim words, date, and target link.
2. **No em-dashes** (`U+2014`) in copy, docs, PRs, commit messages, emails, or chat. Use a comma, colon, full stop, or plain hyphen.
3. **Pinned Squash-Merges.** Squash-merge only with `gh pr merge <n> --squash --match-head-commit <full-40-char-sha>` after a recorded owner approval for production-bound changes. Never push directly to `main`.
4. **Zero High/Critical Advisories.** Fix all high and critical dependency vulnerabilities (`pnpm audit --audit-level=high` or equivalent) before merge.
5. **Every PR Requires an Evidence Block.** UI changes require desktop (`1366x768`) and mobile (`390px`) screenshots across default, empty, loading, and error states. Non-UI changes require exact command and test outputs.
6. **Show Designs First.** UI designs and transactional email templates require owner sign-off through the CEO agent before merging (or before implementation for major modules).
7. **Protect CI Budget.** Run typecheck, lint, test, and security audits locally before pushing. Batch commits and never rerun flaky jobs blindly.
8. **No Secrets in Chat or Git.** Never paste private keys, tokens, passwords, OTP codes, or `.env` values in chat, PRs, issues, or docs.
9. **Quiet Hours.** Respect the owner's configured quiet hours in `PROJECT-CONTEXT.md`. Batch routine decisions into the daily evening summary; interrupt only for live production incidents losing or exposing customer data.

## 2. Repository Hard Stops (Require Explicit Owner Go)
- Any database schema migration
- Any change to tenant-scoping or isolation logic (`tenant_id`)
- Any billing, invoicing, or payment logic
- Any regulated identity or PII storage field
- Any new third-party dependency or external API call
- Any production deploy, rollback, or data deletion

## 3. Handoff & Approval Formats

### Handoff Note
```text
From: <sender_role>   To: <recipient_role>   Date: <DD Mon YYYY>
Work: <issue or PR link, one line>
State: <what is done, what is not>
Evidence: <links to screenshots, test output, reports>
Needs: <what the receiver must do, and by when>
Needs Owner: <none, or the one decision with the exact action>
```

### Approval Request (to CEO)
```text
Action: <exactly what will happen>
Why: <one sentence>
Risk: <what could go wrong, and the rollback>
Evidence: <links>
Recommendation: <Approve / Wait / Do not approve>
Deadline: <only if real>
```
