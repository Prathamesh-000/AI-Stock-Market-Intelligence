"""Helper patch script for fixing frontend number formatting."""

from pathlib import Path

target = Path("frontend/src/App.tsx")
if target.exists():
    content = target.read_text(encoding="utf-8")
    content = content.replace(
        "{pred.finbert?.score || '0.84'}",
        "{pred.finbert?.score?.toFixed(2) || '0.84'}"
    )
    target.write_text(content, encoding="utf-8")
    print("Frontend patch applied successfully.")
else:
    print(f"Target file {target} not found.")
