# Contributing to OpenBot Role Skills

Contributions, new role checks, and evaluation test cases are welcome!

## Adding or Updating a Role Skill

1. Keep every skill in `skills/role-*/` **100% project-agnostic**. Project-specific URLs, domain rules, and environment names belong in `PROJECT-CONTEXT.md` (see `templates/PROJECT-CONTEXT.template.md`).
2. Follow the standard directory layout:
   - `SKILL.md` (YAML frontmatter + concise workflow steps)
   - `agents/openai.yaml` (Codex / Agent Skills display metadata)
   - `references/standing-rules.md` (shared guardrails and templates)
   - `scripts/verify_output.py` (deterministic output verifier)
   - `evals/evals.json` (evaluation prompts and assertions)
3. Run the deterministic verifier across all markdown files before opening a PR:
   ```bash
   python3 skills/role-ceo-governance/scripts/verify_output.py --mode general README.md
   ```
