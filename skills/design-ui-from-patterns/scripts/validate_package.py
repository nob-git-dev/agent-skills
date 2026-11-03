#!/usr/bin/env python3
"""Check portable links, coverage, source fidelity ledger, and required metadata."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []

def require(condition, message):
    if not condition:
        ERRORS.append(message)

def slug(value):
    value = re.sub(r"[^\w\s-]", "", value.lower(), flags=re.UNICODE)
    return re.sub(r"\s+", "-", value.strip())

def main():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    require(skill.startswith("---\n"), "Missing frontmatter")
    require("name: design-ui-from-patterns\n" in skill, "Incorrect skill name")
    require("description:" in skill.split("---", 2)[1], "Missing description")
    require(len(skill.splitlines()) < 500, "SKILL.md exceeds 500 lines")
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        require(not re.search(r"/Users/|/root/|libfile_|file_000|plugin_connector_", text), f"Host-specific identity: {path.name}")
        require("TODO" not in text, f"Unfinished placeholder: {path.name}")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue
            name, sep, anchor = target.partition("#")
            dest = ((path.parent / name) if name else path).resolve()
            require(dest.is_relative_to(ROOT), f"Reference outside skill: {path.name}: {target}")
            require(dest.is_file(), f"Missing file: {path.name}: {target}")
            if sep and dest.is_file() and dest.suffix == ".md":
                body = dest.read_text(encoding="utf-8")
                anchors = {slug(x) for x in re.findall(r"^#{1,6}\s+(.+)$", body, re.M)}
                require(anchor in anchors, f"Missing anchor: {path.name}: {target}")
    themes = ["visual-design.md", "interaction.md", "settings-accessibility.md"]
    cards = []
    for theme in themes:
        text = (ROOT / "references" / theme).read_text(encoding="utf-8")
        found = re.findall(r"^## (P-[VIA]\d{2})$", text, re.M)
        cards.extend(found)
        for match in re.finditer(r"^## (P-[VIA]\d{2})\n(.*?)(?=^## |\Z)", text, re.M | re.S):
            section = match.group(2)
            for label in ["IF：", "THEN：", "確認："]:
                require(label in section, f"{match.group(1)} missing {label}")
    require(len(cards) == len(set(cards)) == 24, "Pattern IDs must be unique; expected 24")
    case_index = (ROOT / "references/case-index.md").read_text(encoding="utf-8")
    for eid in set(re.findall(r"E-[A-Z][A-Z-]+", case_index)):
        require(any(eid in (ROOT / "references" / x).read_text(encoding="utf-8") for x in themes), f"Undefined case: {eid}")
    original = (ROOT / "references/source-original.txt").read_bytes()
    corrected = (ROOT / "references/source-transcript.txt").read_text(encoding="utf-8")
    ledger = json.loads((ROOT / "references/source-ledger.json").read_text(encoding="utf-8"))
    original_lines = original.decode().splitlines()
    clean_lines = corrected.splitlines()
    n = ledger["unit_count"]
    require(len(original_lines) == len(clean_lines) == len(ledger["units"]) == n == 228, "Source unit count mismatch")
    require(hashlib.sha256(original).hexdigest() == ledger["original_sha256"], "Source hash mismatch")
    require(len(original) == ledger["original_bytes"], "Source byte count mismatch")
    require(len(corrected) >= .9 * len(original.decode()), "Transcript shrank more than 10%; fidelity audit required")
    for i, unit in enumerate(ledger["units"], 1):
        require(unit["unit"] == f"U{i:03d}" and unit["original_line"] == unit["corrected_line"] == i, f"Unit order mismatch at {i}")
        reconstructed = original_lines[i-1].strip()
        for edit in unit["edits"]:
            require(edit["from"] in reconstructed, f"Invalid source edit at {i}")
            reconstructed = reconstructed.replace(edit["from"], edit["to"])
        require(reconstructed == clean_lines[i-1], f"Unlogged correction at {i}")
    if ERRORS:
        raise SystemExit("\n".join(ERRORS))
    print(f"Package OK: {len(cards)} patterns; {n} source units; links, IDs and correction ledger verified.")

if __name__ == "__main__":
    main()
