"""
manifest.json + .py/.md 파일 → dist/codes.json, dist/personas.json 빌드
GitHub Action에서 실행됨
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIST = os.path.join(ROOT, "dist")
os.makedirs(DIST, exist_ok=True)

# ─── CODES ───
codes_manifest = os.path.join(ROOT, "codes", "manifest.json")
with open(codes_manifest, "r", encoding="utf-8") as f:
    codes = json.load(f)

for entry in codes:
    py_path = os.path.join(ROOT, "codes", entry["file"])
    if os.path.isfile(py_path):
        with open(py_path, "r", encoding="utf-8") as f:
            entry["code"] = f.read()
    else:
        entry["code"] = ""

with open(os.path.join(DIST, "codes.json"), "w", encoding="utf-8") as f:
    json.dump(codes, f, ensure_ascii=False, indent=2)

# ─── PERSONAS ───
personas_manifest = os.path.join(ROOT, "personas", "manifest.json")
with open(personas_manifest, "r", encoding="utf-8") as f:
    personas = json.load(f)

for entry in personas:
    md_path = os.path.join(ROOT, "personas", entry["file"])
    if os.path.isfile(md_path):
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
        # .md에서 프롬프트 추출 (# 제목과 > 설명 뒤의 내용)
        lines = content.split("\n")
        prompt_lines = []
        skip_header = True
        for line in lines:
            if skip_header and (line.startswith("# ") or line.startswith("> ") or not line.strip()):
                continue
            skip_header = False
            prompt_lines.append(line)
        entry["prompt"] = "\n".join(prompt_lines).strip()

with open(os.path.join(DIST, "personas.json"), "w", encoding="utf-8") as f:
    json.dump(personas, f, ensure_ascii=False, indent=2)

print(f"✅ Built: {len(codes)} codes, {len(personas)} personas → dist/")
