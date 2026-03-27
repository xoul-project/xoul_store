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


def build_codes():
    """Aggregate codes.json (already aggregated)"""
    codes_path = STORE_ROOT / "codes" / "codes.json"
    if codes_path.exists():
        import shutil
        shutil.copy2(codes_path, DIST_DIR / "codes.json")
        print("📦 dist/codes.json updated")


if __name__ == "__main__":
    print("🔨 Building xoul-store dist...\n")
    build_workflows()
    build_codes()
    print("\n✅ Done!")
