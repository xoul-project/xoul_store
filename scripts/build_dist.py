#!/usr/bin/env python3
"""
xoul-store dist builder.
Reads individual workflow/code/persona files and aggregates them into dist/*.json.
Run after merging PRs to update the distribution files.
"""
import json
import os
from pathlib import Path

STORE_ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = STORE_ROOT / "dist"

def build_workflows():
    """Aggregate individual workflow JSON files into dist/workflows.json"""
    manifest_path = STORE_ROOT / "workflows" / "manifest.json"
    if not manifest_path.exists():
        print("⚠ workflows/manifest.json not found")
        return

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    existing_dist = DIST_DIR / "workflows.json"

    # Load existing dist as base (preserves manually curated entries)
    if existing_dist.exists():
        existing = json.loads(existing_dist.read_text(encoding="utf-8"))
        existing_ids = {w.get("id") for w in existing if isinstance(w, dict)}
    else:
        existing = []
        existing_ids = set()

    # Find new workflow files not yet in dist
    added = 0
    for entry in manifest:
        wf_id = entry.get("id", "")
        file_path = entry.get("file", "")
        if not file_path:
            continue

        full_path = STORE_ROOT / "workflows" / file_path
        if not full_path.exists():
            print(f"⚠ File not found: {file_path}")
            continue

        if wf_id in existing_ids:
            continue

        try:
            wf_data = json.loads(full_path.read_text(encoding="utf-8"))
            wf_data["id"] = wf_id
            # author 필드 — manifest에 있으면 사용, 없으면 "Xoul"
            if "author" not in wf_data:
                wf_data["author"] = entry.get("author", "Xoul")
            existing.append(wf_data)
            existing_ids.add(wf_id)
            added += 1
            print(f"  ✅ Added: {wf_id} ({wf_data.get('name', '?')})")
        except Exception as e:
            print(f"  ❌ Error reading {file_path}: {e}")

    # Write updated dist
    DIST_DIR.mkdir(exist_ok=True)
    (DIST_DIR / "workflows.json").write_text(
        json.dumps(existing, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"\n📦 dist/workflows.json updated ({len(existing)} total, {added} new)")


def build_personas():
    """Aggregate individual persona files into dist/personas.json with author field"""
    manifest_path = STORE_ROOT / "personas" / "manifest.json"
    if not manifest_path.exists():
        print("⚠ personas/manifest.json not found")
        return

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    existing_dist = DIST_DIR / "personas.json"

    # Load existing dist as base (preserves stats like views/downloads)
    if existing_dist.exists():
        existing = json.loads(existing_dist.read_text(encoding="utf-8"))
        existing_map = {p.get("id"): p for p in existing if isinstance(p, dict)}
    else:
        existing = []
        existing_map = {}

    result = []
    for entry in manifest:
        p_id = entry.get("id", "")
        if p_id in existing_map:
            # Merge: keep existing stats, ensure author is present
            merged = existing_map[p_id]
            if "author" not in merged:
                merged["author"] = entry.get("author", "Xoul")
            result.append(merged)
        else:
            # New entry from manifest
            persona_data = dict(entry)
            if "author" not in persona_data:
                persona_data["author"] = entry.get("author", "Xoul")
            # Remove file path (not needed in dist)
            persona_data.pop("file", None)
            result.append(persona_data)

    DIST_DIR.mkdir(exist_ok=True)
    (DIST_DIR / "personas.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"📦 dist/personas.json updated ({len(result)} total)")


def build_codes():
    """Aggregate codes.json with author field"""
    codes_path = STORE_ROOT / "codes" / "codes.json"
    dist_path = DIST_DIR / "codes.json"

    # Source can be either codes/codes.json or existing dist
    if codes_path.exists():
        codes = json.loads(codes_path.read_text(encoding="utf-8"))
    elif dist_path.exists():
        codes = json.loads(dist_path.read_text(encoding="utf-8"))
    else:
        print("⚠ No codes source found")
        return

    # Inject author field if missing
    for c in codes:
        if isinstance(c, dict) and "author" not in c:
            c["author"] = "Xoul"

    DIST_DIR.mkdir(exist_ok=True)
    dist_path.write_text(
        json.dumps(codes, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"📦 dist/codes.json updated ({len(codes)} total)")


if __name__ == "__main__":
    print("🔨 Building xoul-store dist...\n")
    build_workflows()
    build_personas()
    build_codes()
    print("\n✅ Done!")
