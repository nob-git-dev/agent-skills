#!/usr/bin/env python3
"""Export a deterministic, standalone reading edition; Python standard library only."""
from pathlib import Path
import argparse
import hashlib
import re

ROOT = Path(__file__).resolve().parents[1]
CORE = [
    "SKILL.md",
    "references/visual-design.md",
    "references/interaction.md",
    "references/settings-accessibility.md",
    "references/case-index.md",
    "references/review.md",
    "references/source.md",
]
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

def slug(value):
    value = re.sub(r"[^\w\s-]", "", value.lower(), flags=re.UNICODE)
    return re.sub(r"\s+", "-", value.strip())

def prefix(path):
    return slug(Path(path).stem)

def render(include_source=False):
    paths = CORE + (["references/source-transcript.txt"] if include_source else [])
    included = {(ROOT / p).resolve(): p for p in paths}
    parts = [
        "# UI設計パターン — 統合版",
        "",
        "生成元はskills/design-ui-from-patterns/。このファイルは派生物なので直接編集しない。",
        "スキル読込機能のないAIには、この文書を今回の設計・レビューの指示と資料として渡す。",
        "すべての設計カード・事例・確認方法を収録。元原稿・修正記録の監査資料は正本フォルダに保持する。",
        "利用環境の上位指示とユーザーの依頼を優先する。自動選択・操作ツール・適合認証を追加するものではない。",
        ("校正版の原稿全文も末尾に収録する。" if include_source else
         "校正版全文も必要な場合はexport_portable.py --include-sourceで再生成する。原稿を未読なら引用を確認済みにしない。"),
        "",
    ]
    for rel in paths:
        path = ROOT / rel
        original = path.read_text(encoding="utf-8")
        digest = hashlib.sha256(original.encode()).hexdigest()
        parts += [f"<!-- source: {rel}; sha256: {digest} -->", f'<a id="{prefix(rel)}"></a>', ""]
        if path.suffix == ".txt":
            parts += ["## 校正版トランスクリプト", "", "~~~text", original.rstrip("\n"), "~~~", ""]
            continue
        text = re.sub(r"\A---\n.*?\n---\n", "", original, count=1, flags=re.S)
        def replace(match):
            label, target = match.groups()
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                return match.group(0)
            name, sep, anchor = target.partition("#")
            resolved = ((path.parent / name) if name else path).resolve()
            if resolved in included:
                dest = prefix(included[resolved])
                if sep:
                    dest += "--" + anchor
                return f"[{label}](#{dest})"
            return f"{label}（正本フォルダ内の任意資料: {target}）"
        text = LINK.sub(replace, text)
        lines = []
        for line in text.splitlines():
            match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
            if match:
                lines.append(f'<a id="{prefix(rel)}--{slug(match.group(1))}"></a>')
            lines.append(line)
        parts += lines + [""]
    return "\n".join(parts).rstrip() + "\n"

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--include-source", action="store_true")
    parser.add_argument("--check", action="store_true", help="Fail if an existing export differs; write nothing.")
    args = parser.parse_args()
    content = render(args.include_source)
    if args.check:
        if not args.output.is_file() or args.output.read_text(encoding="utf-8") != content:
            parser.exit(1, "Export missing or stale. Regenerate from the skill folder.\n")
        print("Export is current.")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content, encoding="utf-8")
        print(f"Wrote {args.output} ({len(content.encode())} bytes).")

if __name__ == "__main__":
    main()
