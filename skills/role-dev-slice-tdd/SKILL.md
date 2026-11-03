---
name: role-dev-slice-tdd
description: "Test-Driven Development (TDD) slice workflow, tenant and role isolation testing, parameterized SQL verification, and local pre-push checks for a Developer agent."
---

# the SaaS product Developer TDD Slice & Multi-Tenant Implementation

You build the SaaS product slices in local clones (`<org>/<product-repo>` and `<org>/<marketing-repo>`) on Node 24 LTS. Read `PROJECT-CONTEXT.md`, `AGENTS.md`, `docs/agent-comms/STATUS.md`, and `docs/DECISIONS.md` before touching code.

## 1. Hard Stops Before Writing Code
Stop and ask the Engineering Lead (who escalates to the Owner via Product Manager and CEO) before starting any code that touches:
1. A Prisma schema migration (`schema.prisma` / `migrations/`).
2. Tenant-scoping or isolation logic (`tenant_id` extension or raw SQL).
3. Billing, invoicing, GST, or payment logic.
4. Identity document fields (Aadhaar is strictly forbidden; ABHA `AbhaNumber`/`AbhaAddress` are nullable schema-readiness fields only, no live ABDM calls).
5. Any new third-party dependency or external API (including Meta WhatsApp API).
6. Anything in Phase 4 (hardening, security, data privacy audit) or Add-on Module build issues (#137 to #142) before #144 designs are approved.

## 2. Step-by-Step Slice Execution
1. **Branching**: Branch from `main` as `feat/<short-name>` or `fix/<short-name>`. Never push to `main`. Never touch Dependabot PRs #74 or #75.
2. **Write Failing Tests First (TDD)**:
   - Backend (`apps/api`): Vitest + Supertest integration tests and unit tests. Every data-scoped endpoint must include a **cross-tenant test** (Tenant A cannot read/write Tenant B) and a **role/cross-doctor test** (Staff cannot access tenantal notes).
   - Frontend (`apps/web`): Vitest + Vue Test Utils using the 4-file Vue component convention (`vue-facing-decorator` class components, Pinia, PrimeVue, brand palette tokens from `DESIGN.md`).
3. **Implement Minimum Code**:
   - Follow `controller -> service -> repository` architecture (`docs/dev/architecture.md`).
   - Scope every query by `tenant_id` from the authenticated session, never from request body/query params. Follow D-026 for any raw SQL (including inner subqueries).
   - Never log request/response bodies containing customer record PII, phone numbers, diagnoses, or secrets.
   - Respect The One Rule: *a consultation must be faster than paper*.
4. **Run All Checks Locally (Save CI Budget)**:
   Run these locally before pushing a single batched commit:
   ```bash
   pnpm typecheck
   pnpm lint
   pnpm test
   pnpm audit --audit-level=high
   ```
   Never push to test in CI, and never rerun CI jobs.
5. **PR & Evidence Section**:
   Open the PR with `gh pr create` (never merge it yourself) and include:
   - Issue link and `docs/REQUIREMENTS.md` row status update in the same PR.
   - Exact local commands run and pass counts.
   - `## Evidence` section: desktop + 390 px mobile screenshots (default, empty, loading, error states) for UI/email, or terminal test output for backend.
6. **Status Report Format**:
   Always report to the Engineering Lead using this exact structure:
   ```text
   SLICE: <issue # and slice name>
   STATUS: done | blocked | in-progress
   TESTS: <passed>/<total> (plus full regression suite result)
   ADVERSARIAL QA: <what cross-tenant, role, and edge cases were tested>
   NEXT: <handoff to Engineering Lead and QA Engineer>
   ```
    verify your PR body and report with `python3 scripts/verify_output.py --mode slice`.

## Bundled References & Scripts
- `references/standing-rules.md`: Full 18 Standing Rules, Section 6 Repo Hard Stops, and Handoff / Approval Request templates from `PROJECT-CONTEXT.md`. Read when checking approval gates or rule conflicts.
- `scripts/verify_output.py`: Deterministic verifier that checks any draft, PR body, QA report, or handoff note for forbidden em-dashes (`U+2014`), leaked secrets, forbidden employer mentions, and required template headers.
