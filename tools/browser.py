"""Headed Playwright session. Every action returns compact DOM text."""
from playwright.sync_api import sync_playwright
_pw=_browser=_page=None
def _session():
    global _pw,_browser,_page
    if _page and not _page.is_closed():return _page
    _pw=sync_playwright().start()
    try:_browser=_pw.chromium.launch(channel="msedge",headless=False)
    except Exception:_browser=_pw.chromium.launch(headless=False)
    _page=_browser.new_page(viewport={"width":1280,"height":800});_page.set_default_timeout(8000);return _page
def _result(page,message):return {"success":True,"message":message,"url":page.url,"page_text":page.locator("body").inner_text(timeout=5000).strip()[:5000]}
def browser_open(url):
    try:
        page=_session();page.goto(url if url.startswith(("http://","https://")) else "https://"+url,wait_until="domcontentloaded");return _result(page,"Browser navigated.")
    except Exception as e:return {"success":False,"error":str(e)}
def browser_read_page():
    try:return _result(_session(),"Read current page.")
    except Exception as e:return {"success":False,"error":str(e)}
def browser_click(selector):
    try:
        page=_session();page.locator(selector).first.click();return _result(page,"Clicked element.")
    except Exception as e:return {"success":False,"error":str(e)}
def browser_type(selector,text,clear=True):
    try:
        page=_session();field=page.locator(selector).first
        if clear:field.fill(text)
        else:field.press_sequentially(text)
        return _result(page,"Typed into element.")
    except Exception as e:return {"success":False,"error":str(e)}
def browser_wait(selector="",milliseconds=1000):
    try:
        page=_session()
        if selector:page.locator(selector).first.wait_for(state="visible")
        else:page.wait_for_timeout(min(max(milliseconds,0),10000))
        return _result(page,"Wait completed.")
    except Exception as e:return {"success":False,"error":str(e)}

def browser_inspect_elements():
    """Return compact actionable DOM targets without dumping the entire page."""
    try:
        page=_session()
        links=page.locator("a[href]").evaluate_all("els => els.slice(0, 30).map((e, i) => ({index:i, text:(e.innerText || e.getAttribute('aria-label') || '').trim().slice(0,120), href:e.href}))")
        fields=page.locator("input, textarea, select, button").evaluate_all("els => els.slice(0, 30).map((e, i) => ({index:i, tag:e.tagName.toLowerCase(), type:e.type || '', name:e.name || '', placeholder:e.placeholder || '', text:(e.innerText || e.getAttribute('aria-label') || '').trim().slice(0,120)}))")
        return {"success":True,"url":page.url,"links":links,"fields":fields}
    except Exception as e:return {"success":False,"error":str(e)}

def browser_press_key(key):
    try:
        page=_session(); page.keyboard.press(key); return _result(page,"Pressed browser key.")
    except Exception as e:return {"success":False,"error":str(e)}
