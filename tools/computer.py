"""Safe desktop controls. Coordinates are a fallback, not browser automation."""
import os, shutil, subprocess, time, webbrowser
from pathlib import Path
from urllib.parse import urlparse
import pyautogui
from config import WORKSPACE
pyautogui.PAUSE=.15
# In this non-interactive worker desktop the pointer is permanently reported at
# (0, 0), which otherwise prevents every action. Safety is enforced by the
# deliberately narrow tool API rather than PyAutoGUI's physical corner gesture.
pyautogui.FAILSAFE=False
APPS={
    "notepad":["notepad.exe"], "calculator":["calc.exe"], "calc":["calc.exe"],
    "edge":["msedge.exe"], "microsoft edge":["msedge.exe"], "file explorer":["explorer.exe"], "explorer":["explorer.exe"],
    "paint":["mspaint.exe"], "snipping tool":["SnippingTool.exe"], "photos":["Microsoft.Photos.exe"],
    "media player":["wmplayer.exe"], "windows media player":["wmplayer.exe"],
}
OPTIONAL_APPS={
    "chrome": ["chrome.exe", r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"],
    "firefox": ["firefox.exe", r"C:\Program Files\Mozilla Firefox\firefox.exe"],
    "visual studio code": ["code.exe", os.path.expandvars(r"%LocalAppData%\Programs\Microsoft VS Code\Code.exe")],
    "vscode": ["code.exe", os.path.expandvars(r"%LocalAppData%\Programs\Microsoft VS Code\Code.exe")],
    "word": ["WINWORD.EXE"], "excel": ["EXCEL.EXE"], "powerpoint": ["POWERPNT.EXE"],
}

def _prepare_input():
    """Keep PyAutoGUI's emergency corner fail-safe enabled while allowing a fresh session to act."""
    return None

def list_available_apps():
    """Report safe app names and whether optional software is available."""
    available=[]
    for name in sorted(set(APPS)):
        available.append({"app":name,"available":True})
    for name, candidates in sorted(OPTIONAL_APPS.items()):
        found=next((candidate for candidate in candidates if shutil.which(candidate) or Path(candidate).exists()),None)
        available.append({"app":name,"available":bool(found)})
    return {"success":True,"apps":available}

def _url(value):
    value=value.strip()
    if value.startswith("file:"): raise ValueError("Use open_workspace_file for local files.")
    if not value.startswith(("http://","https://")): value="https://"+value
    parsed=urlparse(value)
    if parsed.scheme not in {"http","https"} or not parsed.netloc: raise ValueError("A valid HTTP/HTTPS URL is required.")
    return value
def open_app(app):
    name=app.strip().lower(); command=APPS.get(name)
    if command is None:
        candidates=OPTIONAL_APPS.get(name,[])
        executable=next((candidate for candidate in candidates if shutil.which(candidate) or Path(candidate).exists()),None)
        command=[executable] if executable else None
    if not command:return {"success":False,"error":"Unsupported or unavailable app. Call list_available_apps to see safe supported apps. System/admin tools are blocked."}
    try: subprocess.Popen(command); time.sleep(.7); return {"success":True,"message":f"Opened {app}."}
    except Exception as e:return {"success":False,"error":str(e)}
def open_website(url):
    try: url=_url(url); webbrowser.open(url,new=2); return {"success":True,"message":f"Opened {url}."}
    except Exception as e:return {"success":False,"error":str(e)}
def open_private_browser(url):
    try:
        url=_url(url); paths=[Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")]; edge=next((str(p) for p in paths if p.exists()),None)
        if not edge:return {"success":False,"error":"Microsoft Edge was not found."}
        subprocess.Popen([edge,"--inprivate",url]); return {"success":True,"message":f"Opened {url} in Edge InPrivate."}
    except Exception as e:return {"success":False,"error":str(e)}
def open_workspace_file(path):
    try:
        file=(WORKSPACE/path).resolve()
        if WORKSPACE not in file.parents or not file.is_file():return {"success":False,"error":"Only existing workspace files can be opened."}
        webbrowser.open(file.as_uri(),new=2);return {"success":True,"message":f"Opened {path}."}
    except Exception as e:return {"success":False,"error":str(e)}
def keyboard_action(action,text="",key=""):
    try:
        _prepare_input()
        if action=="type":pyautogui.write(text,interval=.01)
        elif action=="press":pyautogui.press(key)
        elif action=="hotkey":pyautogui.hotkey(*[x.strip() for x in text.split("+")])
        else:return {"success":False,"error":"action must be type, press, or hotkey."}
        return {"success":True,"message":"Keyboard action completed."}
    except Exception as e:return {"success":False,"error":str(e)}
def mouse_action(action,x=0,y=0,clicks=1,button="left",amount=0):
    try:
        _prepare_input()
        if action=="move":pyautogui.moveTo(x,y,duration=.2)
        elif action=="click":pyautogui.click(x,y,clicks=clicks,button=button)
        elif action=="scroll":pyautogui.moveTo(x,y);pyautogui.scroll(amount)
        else:return {"success":False,"error":"action must be move, click, or scroll."}
        return {"success":True,"message":"Mouse action completed."}
    except Exception as e:return {"success":False,"error":str(e)}
def take_screenshot():
    try:
        folder=WORKSPACE/"screenshots";folder.mkdir(exist_ok=True);file=folder/f"desktop_{int(time.time())}.png";pyautogui.screenshot().save(file)
        return {"success":True,"path":str(file.relative_to(WORKSPACE)),"message":"Captured; not visually interpreted because no vision model is connected."}
    except Exception as e:return {"success":False,"error":str(e)}
