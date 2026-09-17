"""Workspace-only file operations."""
from config import WORKSPACE, MAX_FILE_BYTES

def _target(path):
    if not isinstance(path, str) or not path.strip(): raise ValueError("A workspace path is required.")
    result = (WORKSPACE / path).resolve()
    if result != WORKSPACE and WORKSPACE not in result.parents: raise PermissionError("Access outside workspace is blocked.")
    return result

def list_workspace(path="."):
    try:
        folder = _target(path)
        if not folder.is_dir(): return {"success": False, "error": "Directory does not exist."}
        items = [{"name": p.name, "path": str(p.relative_to(WORKSPACE)), "type": "directory" if p.is_dir() else "file"} for p in sorted(folder.iterdir(), key=lambda x:(not x.is_dir(),x.name.lower()))]
        return {"success": True, "files": items[:200], "truncated": len(items)>200}
    except Exception as e: return {"success": False, "error": str(e)}

def read_workspace_file(path):
    try:
        file = _target(path)
        if not file.is_file(): return {"success": False, "error": "File does not exist."}
        if file.stat().st_size > MAX_FILE_BYTES: return {"success": False, "error": "File is too large."}
        return {"success": True, "path": str(file.relative_to(WORKSPACE)), "content": file.read_text(encoding="utf-8")}
    except UnicodeDecodeError: return {"success": False, "error": "Only UTF-8 text files are supported."}
    except Exception as e: return {"success": False, "error": str(e)}

def write_workspace_file(path, content):
    try:
        if not isinstance(content, str) or len(content.encode()) > MAX_FILE_BYTES: return {"success":False,"error":"Content must be text below the size limit."}
        file = _target(path)
        if file == WORKSPACE: return {"success":False,"error":"A file path is required."}
        file.parent.mkdir(parents=True, exist_ok=True); file.write_text(content, encoding="utf-8")
        return {"success":True,"path":str(file.relative_to(WORKSPACE)),"bytes":file.stat().st_size}
    except Exception as e: return {"success":False,"error":str(e)}

def append_workspace_file(path, content):
    """Append text without allowing the model to escape the workspace."""
    try:
        if not isinstance(content, str) or len(content.encode()) > MAX_FILE_BYTES: return {"success":False,"error":"Content must be text below the size limit."}
        file = _target(path)
        if file == WORKSPACE: return {"success":False,"error":"A file path is required."}
        old_size = file.stat().st_size if file.exists() else 0
        if old_size + len(content.encode()) > MAX_FILE_BYTES: return {"success":False,"error":"The resulting file would be too large."}
        file.parent.mkdir(parents=True, exist_ok=True)
        with file.open("a", encoding="utf-8") as handle: handle.write(content)
        return {"success":True,"path":str(file.relative_to(WORKSPACE)),"bytes":file.stat().st_size}
    except Exception as e: return {"success":False,"error":str(e)}

def replace_workspace_text(path, old_text, new_text):
    """Safely make a targeted edit only when the old text occurs exactly once."""
    try:
        file = _target(path)
        if not file.is_file(): return {"success":False,"error":"File does not exist."}
        content = file.read_text(encoding="utf-8")
        occurrences = content.count(old_text)
        if occurrences != 1: return {"success":False,"error":f"Expected the old text once, found {occurrences}. Read the file and try a more specific replacement."}
        updated = content.replace(old_text, new_text, 1)
        if len(updated.encode()) > MAX_FILE_BYTES:return {"success":False,"error":"The resulting file would be too large."}
        file.write_text(updated,encoding="utf-8")
        return {"success":True,"path":str(file.relative_to(WORKSPACE)),"message":"Targeted text replacement completed."}
    except UnicodeDecodeError:return {"success":False,"error":"Only UTF-8 text files are supported."}
    except Exception as e:return {"success":False,"error":str(e)}

def create_workspace_directory(path):
    try:
        folder=_target(path); folder.mkdir(parents=True,exist_ok=True)
        return {"success":True,"path":str(folder.relative_to(WORKSPACE))}
    except Exception as e: return {"success":False,"error":str(e)}
