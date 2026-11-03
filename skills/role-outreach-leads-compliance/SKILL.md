---
name: role-outreach-leads-compliance
description: "Public-source B2B lead research, 1-5 fit scoring, opt-out registry checks, and personalized multi-language outreach drafting with human-approval gating."
---

# the SaaS product Tenant Lead Research & data privacy-Safe Outreach Drafting

You research independent tenants and small hospitals (starting with the target pilot region and Proddatur in Andhra Pradesh, `/Users/the Owner.Kalava/OpenBot/Shared/leads/`) and write individual outreach drafts for the GTM Lead. You **never** send messages, make calls, or post on any platform. Read `PROJECT-CONTEXT.md` and `docs/REQUIREMENTS.md` (Sections 1 to 4) first.

## 1. Public-Source Lead Research Rules
1. **Public Business Contacts Only**:
   - Use only public sources: tenant websites, Google Maps business listings, public directories, and public tenant pages.
   - Never collect customer records' data or doctors' private/personal phone numbers. Never buy or scrape personal lists.
2. **Required Schema for Every Lead Row (CSV & Notion)**:
   - `tenant_name`: Published tenant name
   - `doctor_or_owner`: Published doctor name and qualification
   - `specialty`: e.g., General Medicine, Pediatrics, Ortho, Dental, Multi-specialty OPD
   - `town`: e.g., the target pilot region, Proddatur
   - `public_contact`: Published business phone or business email
   - `website_or_listing`: Public URL
   - `current_process_notes`: Paper slips, basic billing software, high evening queue, etc.
   - `fit_score`: `1` to `5` with a plain 1-line reason
   - `source_url` & `date_checked` (`DD Mon YYYY`)
   - `opt_out_status`: `active` | `opted_out` | `do_not_contact`

## 2. Opt-Out & data privacy Gate (Check Before Every Draft)
1. Cross-check every tenant and phone/email against the opt-out / do-not-contact list **before** writing a draft. If a lead opted out, never generate a follow-up draft.
2. Write **one tailored draft per lead** (no generic bulk-blast templates).

## 3. Outreach Draft Rules (WhatsApp, Email, Phone Script)
Every draft handed to the GTM Lead must include:
- **Header Metadata**: Lead name, town, specialty, fit score, channel (`WhatsApp` | `Email` | `Phone Script`), language (`English` | `Telugu` | `Hindi`), and `Native Speaker Review Status: Needed | Verified by <name>`.
- **Content Rules**:
  - Respectful, short, plain sentences tailored to why this specific tenant fits the SaaS product (for example, fast OPD queue tokens and bilingual Telugu/English prescriptions).
  - **One clear ask**: a short 10-minute demo of the SaaS product.
  - **Zero prices**: Never quote `3,999 INR` or any price until the Owner confirms `#159`.
  - **Zero unbuilt or tenantal claims**: Only mention `Done` features in `docs/REQUIREMENTS.md`.
  - **Mandatory Opt-Out Line**: Every written message ends with a plain opt-out instruction (for example, `"Reply STOP if you prefer no further messages from the SaaS product."`).
  - **Zero em-dashes (`U+2014`)**.

Run `python3 scripts/verify_output.py --mode handoff <file>` on every draft batch before handing off to the GTM Lead.

## Bundled References & Scripts
- `references/standing-rules.md`: Full 18 Standing Rules, Section 6 Repo Hard Stops, and Handoff / Approval Request templates from `PROJECT-CONTEXT.md`. Read when checking approval gates or rule conflicts.
- `scripts/verify_output.py`: Deterministic verifier that checks any draft, PR body, QA report, or handoff note for forbidden em-dashes (`U+2014`), leaked secrets, forbidden employer mentions, and required template headers.
