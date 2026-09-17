from .computer import *
from .filesystem import *
from .browser import *
from .repository import *
from .research import web_search
TOOL_FUNCTIONS={name:globals()[name] for name in ("list_available_apps","open_app","open_website","open_private_browser","open_workspace_file","keyboard_action","mouse_action","take_screenshot","list_workspace","read_workspace_file","write_workspace_file","append_workspace_file","replace_workspace_text","create_workspace_directory","initialize_workspace_repository","workspace_repository_status","web_search","browser_open","browser_read_page","browser_click","browser_type","browser_wait","browser_inspect_elements","browser_press_key")}
