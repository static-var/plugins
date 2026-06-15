#!/usr/bin/env python3
import json
import re
import subprocess
import sys

try:
    payload = json.load(sys.stdin)
except Exception:
    raise SystemExit(0)

if not isinstance(payload, dict):
    raise SystemExit(0)

tool_input = payload.get('tool_input')
if not isinstance(tool_input, dict):
    raise SystemExit(0)

command = tool_input.get('command', '')
if not isinstance(command, str) or not command.strip():
    raise SystemExit(0)
if 'build-brief' in command:
    raise SystemExit(0)

gradle_command_pattern = re.compile(r'(^|[\s;&|()])(\./gradlew|gradlew|gradle)(\s|$)')

try:
    result = subprocess.run(
        ['build-brief', 'rewrite', command],
        check=False,
        capture_output=True,
        text=True,
    )
except FileNotFoundError:
    if gradle_command_pattern.search(command):
        sys.stderr.write(
            '[build-brief] Codex intercepted a raw Gradle command, but the '
            'build-brief binary is not installed or not on PATH.\n\n'
            'Install build-brief first:\n\n'
            '  brew tap static-var/tap\n'
            '  brew install static-var/tap/build-brief\n\n'
            'or:\n\n'
            '  curl -fsSL https://bb.staticvar.dev/install.sh | bash\n'
        )
        raise SystemExit(2)
    raise SystemExit(0)

rewritten = result.stdout.strip()
if result.returncode != 0 or not rewritten or rewritten == command.strip():
    raise SystemExit(0)

sys.stderr.write(
    '[build-brief] Codex blocked a routine Gradle command or chain.\n'
    '[build-brief] Use this instead:\n\n'
    '  ' + rewritten + '\n\n'
    'This Codex PreToolUse hook can block and suggest a safer replacement,\n'
    'but it cannot transparently rewrite and continue in place.\n'
)
raise SystemExit(2)
