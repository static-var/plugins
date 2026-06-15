import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "pretooluse-build-brief.py"


def run_hook(payload: str, build_brief_body: str):
    with tempfile.TemporaryDirectory() as tmp:
        shim = Path(tmp) / "build-brief"
        shim.write_text("#!/bin/sh\n" + build_brief_body, encoding="utf-8")
        shim.chmod(0o755)

        env = os.environ.copy()
        env["PATH"] = f"{tmp}{os.pathsep}{env['PATH']}"

        return subprocess.run(
            [sys.executable, str(SCRIPT)],
            input=payload,
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )


def run_hook_without_build_brief(payload: str):
    with tempfile.TemporaryDirectory() as tmp:
        env = os.environ.copy()
        env["PATH"] = tmp

        return subprocess.run(
            [sys.executable, str(SCRIPT)],
            input=payload,
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )


class PreToolUseBuildBriefTest(unittest.TestCase):
    def test_blocks_when_rewrite_changes_command(self):
        result = run_hook(
            '{"tool_input":{"command":"gradle test"}}',
            'if [ "$1" = rewrite ]; then echo "build-brief gradle test"; fi\n',
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("build-brief gradle test", result.stderr)

    def test_allows_when_rewrite_is_unchanged(self):
        result = run_hook(
            '{"tool_input":{"command":"gradle test"}}',
            'if [ "$1" = rewrite ]; then echo "$2"; fi\n',
        )

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")

    def test_blocks_raw_gradle_when_binary_is_missing(self):
        result = run_hook_without_build_brief('{"tool_input":{"command":"gradle test"}}')

        self.assertEqual(result.returncode, 2)
        self.assertIn("build-brief binary is not installed", result.stderr)


if __name__ == "__main__":
    unittest.main()
