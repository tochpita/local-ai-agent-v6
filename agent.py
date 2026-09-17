"""V6 local model-directed computer-use agent."""
import json
from ollama import chat
from config import MODEL,MAX_STEPS,WORKSPACE
from tools import TOOL_FUNCTIONS
from tools.schemas import TOOLS
SYSTEM_PROMPT="""You are V6, a local Windows computer-use agent. You decide each next tool from the goal and tool results; work in multiple steps only as needed. Ask list_available_apps before guessing an app name. When you create HTML in the workspace, open it with open_workspace_file, never open_website. For repository work, use only the workspace Git tools; never create a remote, commit, push, install, or transmit data without the user's explicit request. Prefer Playwright DOM tools for sites opened with browser_open; it controls its own session, not a browser opened with open_website or Edge InPrivate. Use browser_inspect_elements before guessing unfamiliar selectors. A screenshot is only an observation artifact: never claim to see it. Inspect search results rather than blindly trusting one. Recover from failures by choosing another suitable tool. Workspace paths stay inside workspace. Never bypass CAPTCHA, human verification, authentication, or security controls; stop for human verification. Ask before external submissions or installing software. Be concise and report completion honestly."""
def _call(call):
    name,args=call.function.name,call.function.arguments;print(f"\n[Tool] {name}")
    try:result=TOOL_FUNCTIONS[name](**args) if name in TOOL_FUNCTIONS else {"success":False,"error":f"Unknown tool: {name}"}
    except Exception as error:result={"success":False,"error":str(error)}
    print("[Result] Done." if result.get("success") else "[Result] Failed.");return name,result
def run_agent(user_input):
    messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":user_input}]
    for _ in range(MAX_STEPS):
        response=chat(model=MODEL,messages=messages,tools=TOOLS,think=False);messages.append(response.message);calls=response.message.tool_calls or []
        if not calls:return response.message.content or "Completed."
        for call in calls:
            name,result=_call(call);messages.append({"role":"tool","tool_name":name,"content":json.dumps(result,ensure_ascii=False)})
    return f"Stopped after {MAX_STEPS} steps to prevent a runaway loop."
def main():
    WORKSPACE.mkdir(parents=True,exist_ok=True);print("LOCAL AI AGENT V6\nModel: qwen3:1.7b\nType 'exit' to quit.\n")
    while True:
        try:
            user=input("You: ").strip()
            if user.lower()=="exit":break
            if user:print("\nAgent:",run_agent(user),"\n")
        except KeyboardInterrupt:break
        except Exception as error:print("\nERROR:",error)
if __name__=="__main__":main()
