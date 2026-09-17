from pathlib import Path
MODEL = "qwen3:1.7b"
MAX_STEPS = 20
PROJECT_ROOT = Path(__file__).parent.resolve()
WORKSPACE = (PROJECT_ROOT / "workspace").resolve()
MAX_FILE_BYTES = 500_000
