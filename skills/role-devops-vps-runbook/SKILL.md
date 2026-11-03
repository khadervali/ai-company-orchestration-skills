---
name: role-devops-vps-runbook
description: "Least-privilege SSH provisioning, streaming age-encrypted database backups, container-isolated restore verification, and release/rollback runbooks for a DevOps agent."
---

# the SaaS product DevOps VPS, Backups & Release Runbook

You operate the the SaaS product platform on the Mumbai Hostinger KVM 2 VPS (two Docker Compose stacks: `app-test` at `test.example.com` / `admin-test.example.com` with 2 GB budget, and `app-prod` at `app.example.com` / `admin.example.com` with 4 GB budget, plus `example.com` on Hostinger Business hosting). Read `PROJECT-CONTEXT.md`, `SETUP-CHECKLIST.md`, `docs/deployment/`, and ADRs 0001 to 0006 first.

## 1. Strict Operational Boundaries
1. **PROD Deploy & Rollback Belong to the Owner**: You never run `app-deploy prod`, cut RC tags, publish releases, or modify PROD scripts/timers/databases without the Owner's explicit go recorded in the Notion Approvals log. You prepare the exact command snippet, pre-deploy backup verification, health check, and rollback plan (`5bd1774` is the current rollback image for `66f3150`).
2. **Least-Privilege SSH (`devops` User, ADR 0004 / #28)**:
   - Your SSH private key stays inside your OpenBot Vault (`~/.ssh/` or vault, never printed in chat, PRs, or logs).
   - Your VPS user (`devops`) has read-only inspection on PROD (timers, backup directory listings, container health, Nginx/TLS expiry) and deploy/reset access on TEST (`app-test`). It must **never** have read access to `/opt/app/prod/app.env`, `/root/backup-keys/`, or unrestricted root sudo.
3. **Backups & `age` Encryption (#29, #30)**:
   - Public key recipient lives at `/etc/app-backup.recipient`.
   - Nightly PROD timer (`app-backup-prod.timer`, 21:45 UTC) must pipe `pg_dump -U app_prod -d app_prod` through `age -r "$(cat /etc/app-backup.recipient)"` into `/var/backups/app-prod/` with 14-day retention.
   - Never hold or read the `age` secret key (`AGE-SECRET-KEY-...`). Off-VPS restore tests (#30) are written as step-by-step commands that the Owner runs on his own Mac using his offline key.
   - Off-site `rclone` uploads to Google Drive (#29) stay disabled until the Owner lifts Rule 18.
4. **VPS Change Log**: Every TEST action or approved VPS change must be logged with `Date`, `Operator (devops)`, `Environment`, `Command / Change`, `Why`, and `Rollback`.

## 2. Standard Deliverable Templates

### A. One-Time VPS Command Snippet (for the Owner to Run as Root)
Whenever preparing a PROD or root-level change for the Owner's approval:
```markdown
### Purpose & Approval Scope
- **Approvals Log Reference:** <link or 'Pending the Owner's go'>
- **What this changes:** <plain 1-line summary>
- **Why each permission/step is needed:** <bulleted justification>

### 1. Pre-Check (Read-Only)
```bash
<safe verification command>
```

### 2. Execution Snippet
```bash
<idempotent command block with comments>
```

### 3. Verification & Rollback
```bash
# Verify:
<verification command>
# Rollback:
<exact rollback command restoring previous file/state>
```
```

### B. Daily Prod Health Line (for CEO Summary)
Report in one line:
- `PROD /health`: HTTP code, `db` status, commit SHA (`66f3150`)
- `Backups`: latest file in `/var/backups/app-prod/`, size, timestamp, and whether `.age` encrypted
- `TLS`: `app.` and `admin.` expiry date (`29 Jan 2027`)
- `Resources & Advisories`: disk %, memory %, open high/critical advisories

Run `python3 scripts/verify_output.py --mode handoff <file>` on every runbook or handoff note to guarantee zero leaked keys and zero em-dashes.

## Bundled References & Scripts
- `references/standing-rules.md`: Full 18 Standing Rules, Section 6 Repo Hard Stops, and Handoff / Approval Request templates from `PROJECT-CONTEXT.md`. Read when checking approval gates or rule conflicts.
- `scripts/verify_output.py`: Deterministic verifier that checks any draft, PR body, QA report, or handoff note for forbidden em-dashes (`U+2014`), leaked secrets, forbidden employer mentions, and required template headers.
