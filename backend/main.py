import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "api"))

from app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, use_colors=False, log_level="info")
