#!/usr/bin/env python3
"""
Deterministic output verifier for OpenBot / Claude Code multi-agent SaaS teams.
Scans drafts, PR bodies, slice reports, QA reports, and handoff notes for:
1. Forbidden em-dashes (U+2014)
2. Leaked secret/key patterns (private keys, tokens, connection strings)
3. Required template sections (--mode summary|approval|handoff|slice|qa|general)
"""
import argparse
import pathlib
import re
import sys

SECRET_PATTERNS = [
    (r"AGE-SECRET-KEY-1[A-Z0-9]+", "age private key"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "PEM/OpenSSH private key"),
    (r"gh[pousr]_[A-Za-z0-9_]{20,}", "GitHub token"),
    (r"github_pat_[A-Za-z0-9_]{20,}", "GitHub fine-grained PAT"),
    (r"sk-[A-Za-z0-9]{20,}", "API secret key"),
    (r"postgres(?:ql)?://[^\s]+:[^\s]+@", "Database connection string with credentials"),
]

REQUIRED_HEADERS = {
    "summary": ["Needs your go", "Shipped today", "In progress and blocked", "Prod health", "Tomorrow"],
    "approval": ["Action:", "Why:", "Risk:", "Evidence:", "Recommendation:"],
    "handoff": ["From:", "To:", "Work:", "State:", "Evidence:", "Needs:"],
    "slice": ["Slice:", "Tests:", "Tenant isolation:", "Commands run:"],
    "qa": ["Round", "Environment", "Commit", "Findings"],
    "general": [],
}

def verify_text(text: str, mode: str) -> list[str]:
    errors = []
    if "\u2014" in text:
        count = text.count("\u2014")
        errors.append(f"Found {count} forbidden em-dash character(s) (U+2014). Replace with comma, colon, period, or hyphen.")
    for pattern, label in SECRET_PATTERNS:
        if re.search(pattern, text):
            errors.append(f"Potential secret detected: {label}")
    for header in REQUIRED_HEADERS.get(mode, []):
        if header.lower() not in text.lower():
            errors.append(f"Missing required '{mode}' section/field: '{header}'")
    return errors

def main() -> int:
    parser = argparse.ArgumentParser(description="Verify agent output against team standing rules.")
    parser.add_argument("--mode", choices=list(REQUIRED_HEADERS.keys()), default="general")
    parser.add_argument("file", help="Path to markdown or text file to verify")
    args = parser.parse_args()
    text = pathlib.Path(args.file).read_text(encoding="utf-8")
    errors = verify_text(text, args.mode)
    if errors:
        for err in errors:
            print(f"[FAIL] {err}", file=sys.stderr)
        return 1
    print(f"[PASS] {args.file} passed all '{args.mode}' verification checks.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
