import os
import subprocess
import tempfile
from typing import Dict


def execute_code(code: str, timeout: int = 8) -> Dict:
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as f:
            f.write(code)
            tmp_path = f.name

        proc = subprocess.run(
            ["python", tmp_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )

        stdout = proc.stdout or ""
        stderr = proc.stderr or ""
        max_chars = 4000
        if len(stdout) > max_chars:
            stdout = stdout[:max_chars] + "\n...[truncated]"
        if len(stderr) > max_chars:
            stderr = stderr[:max_chars] + "\n...[truncated]"

        return {"success": proc.returncode == 0, "stdout": stdout, "stderr": stderr, "error": None}
    except subprocess.TimeoutExpired:
        return {"success": False, "stdout": "", "stderr": "", "error": "timeout"}
    except Exception as e:
        return {"success": False, "stdout": "", "stderr": "", "error": str(e)}
    finally:
        try:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass
