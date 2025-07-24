# plugins/file_editor.py

import os
import shutil

def read(filepath: str) -> str:
    if not os.path.exists(filepath):
        return "❌ File not found."
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def write(filepath: str, content: str) -> str:
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return f"✅ Written to {filepath}"
    except Exception as e:
        return f"❌ Write failed: {e}"

def append(filepath: str, content: str) -> str:
    try:
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(content)
        return f"✅ Appended to {filepath}"
    except Exception as e:
        return f"❌ Append failed: {e}"

def replace(filepath: str, old_text: str, new_text: str) -> str:
    if not os.path.exists(filepath):
        return "❌ File not found."

    try:
        # Backup before editing
        backup_path = filepath + ".bak"
        shutil.copy2(filepath, backup_path)

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        modified = content.replace(old_text, new_text)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(modified)

        return f"🔄 Replaced '{old_text}' with '{new_text}' in {filepath}"
    except Exception as e:
        return f"❌ Replace failed: {e}"
