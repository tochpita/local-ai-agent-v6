"""Small, project-local Git helpers; no remote or credential actions."""
import subprocess
from config import PROJECT_ROOT

def _git(*args):
    # Keep the exception process-local: do not alter the user's global Git config.
    return subprocess.run(["git", "-c", f"safe.directory={PROJECT_ROOT.as_posix()}", "-C", str(PROJECT_ROOT), *args], capture_output=True, text=True, timeout=15)

def initialize_workspace_repository():
    try:
        result = _git("rev-parse", "--is-inside-work-tree")
        if result.returncode == 0:
            return {"success":True,"message":"The V6 project is already a Git repository."}
        result = _git("init")
        if result.returncode != 0:return {"success":False,"error":result.stderr.strip() or "git init failed."}
        return {"success":True,"message":"Initialized a local Git repository for V6. No remote was created."}
    except FileNotFoundError:return {"success":False,"error":"Git is not installed or is unavailable on PATH."}
    except Exception as e:return {"success":False,"error":str(e)}

def workspace_repository_status():
    try:
        result = _git("status", "--short")
        if result.returncode != 0:return {"success":False,"error":"The V6 project is not a Git repository. Initialize it first."}
        return {"success":True,"status":result.stdout.strip() or "Working tree is clean."}
    except FileNotFoundError:return {"success":False,"error":"Git is not installed or is unavailable on PATH."}
    except Exception as e:return {"success":False,"error":str(e)}
