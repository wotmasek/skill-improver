#!/usr/bin/env python3
"""Best-effort PostToolUse hook: log an *observed* error when a test/build
command clearly fails.

Conservative by design — a false "observed error" could trigger a wrong
rollback, so this logs ONLY when it can see an unambiguous non-zero exit code
for a recognized test/build command. When in doubt it does nothing, and it never
blocks (always exits 0).
"""

import json
import os
import re
import subprocess
import sys

LEDGER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ledger.py")

# Recognized test/build commands — narrow on purpose.
CMD_RE = re.compile(
    r"\b(pytest|npm (run )?(test|build)|yarn (test|build)|jest|"
    r"make( |$)|cargo (test|build)|go test|go build|tox|mvn|gradle)\b"
)


def exit_code(resp):
    """Return an int exit code if the response clearly carries one, else None."""
    if isinstance(resp, dict):
        for key in ("exit_code", "exitCode", "code", "returncode"):
            if isinstance(resp.get(key), int):
                return resp[key]
    return None


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return  # no parseable input → do nothing

    if data.get("tool_name") != "Bash":
        return

    command = (data.get("tool_input") or {}).get("command", "")
    if not command or not CMD_RE.search(command):
        return

    code = exit_code(data.get("tool_response"))
    if not code:  # None or 0 → not a clear failure
        return

    desc = f"command failed (exit {code}): {command[:120]}"
    try:
        subprocess.run(
            ["python3", LEDGER, "log-error",
             "--description", desc,
             "--cause", "mechanical failure detected by PostToolUse hook",
             "--severity", "bad", "--source", "observed"],
            check=False, capture_output=True, timeout=15,
        )
    except Exception:
        pass  # never let the hook break the session


if __name__ == "__main__":
    main()
    sys.exit(0)
