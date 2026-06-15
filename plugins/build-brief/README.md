# build-brief Codex plugin

This plugin adds a Codex `PreToolUse` guardrail for routine Gradle Bash
commands. When a command can be rewritten by `build-brief rewrite`, the hook
blocks the raw Gradle command and prints the replacement.

The plugin expects the `build-brief` binary to be available on `PATH`. Install
it before relying on the hook:

```bash
brew tap static-var/tap
brew install static-var/tap/build-brief
```

or:

```bash
curl -fsSL https://bb.staticvar.dev/install.sh | bash
```

If the binary is missing and Codex tries to run a raw Gradle command, the hook
blocks the command and prints the install options. If a command does not need
rewriting, the hook exits without changing Codex behavior.

The hook delegates all command parsing and rewrite decisions to the local
`build-brief` CLI so the plugin does not duplicate Gradle command parsing
logic.
