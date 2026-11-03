# PROJECT-CONTEXT.md (Template)

Copy this file to your shared workspace root as `PROJECT-CONTEXT.md`. Every role skill in `openbot-role-skills` reads this file first at the start of each session.

## 1. Product Overview
- **Product Name:** `<Your SaaS Name>`
- **Owner / Founder:** `<Owner Name>` (`<Timezone, e.g. Europe/Stockholm>`)
- **Core Stack:** `<e.g. TypeScript, NestJS / Next.js, PostgreSQL, Prisma, Vue / React>`
- **Multi-Tenancy Model:** `<e.g. Shared database, every table scoped by tenant_id>`
- **Primary User Roles:** `<e.g. Primary User, Staff, Tenant Admin, Super Admin>`

## 2. Environments & Repositories
| Resource | Location / URL |
|---|---|
| Product Repository | `<org>/<product-repo>` (`main`) |
| Marketing Site Repository | `<org>/<marketing-repo>` |
| Requirements Source of Truth | `docs/REQUIREMENTS.md` |
| Approvals Log | `<Notion / Linear / GitHub URL>` |
| Staging / TEST Environment | `https://test.example.com` |
| Production Environment | `https://app.example.com` |

## 3. Standing Rules
1. **Single Approvals Gate:** Only the Owner approves production merges, deploys, schema changes, billing logic, deletions, and external sends.
2. **Quiet Hours:** `<e.g. Weekdays 08:00 to 17:00 Europe/Stockholm>`. Batch non-urgent updates into one evening summary.
3. **CI Budget & Quality Gate:** Run `typecheck`, `lint`, `test`, and `audit` locally before pushing. Squash-merge only with `--match-head-commit`.
4. **Formatting & Privacy:** Zero em-dashes (`U+2014`). Zero secrets or customer PII in chat, PRs, screenshots, or logs.
