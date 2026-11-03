#!/usr/bin/env python3
"""Generate skills-index.json from SKILL.md metadata without loading every skill at runtime."""
from pathlib import Path
import argparse
import ast
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ALIASES = {"edit-speech-transcripts", "edit-with-editing-engineering", "write-clear-business-docs"}

def metadata(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
    if not match:
        raise ValueError(f"Missing frontmatter: {path}")
    head = match.group(1)
    result = {}
    for key in ("name", "description"):
        found = re.search(r"^" + key + r":\s*(.*)$", head, re.M)
        if not found:
            raise ValueError(f"Missing {key}: {path}")
        value = found.group(1).strip()
        if value in ("|", ">", "|-", ">-"):
            tail = head[found.end():].splitlines()
            chunks = []
            for line in tail:
                if line and not line.startswith((" ", "\t")):
                    break
                if line.strip():
                    chunks.append(line.strip())
            value = (" " if value.startswith(">") else "\n").join(chunks)
        elif value.startswith(('"', "'")):
            value = ast.literal_eval(value)
        if not isinstance(value, str) or not value:
            raise ValueError(f"Empty/nontext {key}: {path}")
        result[key] = value
    if result["name"] != path.parent.name:
        raise ValueError(f"Folder/name mismatch: {path}")
    return result

def build():
    files = sorted(ROOT.glob("skills/*/SKILL.md")) + sorted(ROOT.glob("plugins/*/skills/*/SKILL.md"))
    groups = {}
    for path in files:
        item = metadata(path)
        item["entrypoint"] = path.relative_to(ROOT).as_posix()
        item["directory"] = path.parent.relative_to(ROOT).as_posix()
        groups.setdefault(item["name"], []).append(item)
    skills = []
    for name, variants in sorted(groups.items()):
        if len(variants) > 1 and name not in ALIASES:
            raise ValueError(f"Unreviewed duplicate skill name: {name}")
        variants.sort(key=lambda x: (not x["entrypoint"].startswith("skills/"), x["entrypoint"]))
        primary = variants[0]
        primary["aliases"] = [
            {"entrypoint":v["entrypoint"],"directory":v["directory"],"description":v["description"]}
            for v in variants[1:]
        ]
        primary["selection"] = ("ui-design-decisions" if name == "design-ui-from-patterns" else
                                "ui-implementation" if name == "ui" else "match-description")
        skills.append(primary)
    return {
        "schema_version": 1,
        "entry_guide": "SKILLS.md",
        "agent_instructions": "AGENTS.md",
        "path_base": "repository-root",
        "selection_rule": "Match the user goal to descriptions, choose the narrowest suitable skill, read its complete SKILL.md, then only the referenced files needed. Aliases are alternative packages, not additional skills to run.",
        "skills": skills,
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    path = ROOT / "skills-index.json"
    content = json.dumps(build(), ensure_ascii=False, indent=2) + "\n"
    if args.check:
        if not path.is_file() or path.read_text(encoding="utf-8") != content:
            parser.exit(1, "skills-index.json is missing or stale. Run scripts/build_skill_catalog.py.\n")
        print("Skill catalog is current.")
    else:
        path.write_text(content, encoding="utf-8")
        print(f"Wrote {path.name} with {len(build()['skills'])} unique skills.")

if __name__ == "__main__":
    main()
