---
name: build-brief
description: Use when running Gradle builds, tests, checks, Android/Java/Kotlin build tasks, or when raw Gradle output is too noisy and should be reduced while preserving the raw log.
---

# build-brief

Use `build-brief` for routine Gradle commands so the terminal stays concise
while the full raw log remains available on disk.

Before using it, check whether the binary is installed:

```bash
command -v build-brief
```

If it is missing, install it with Homebrew:

```bash
brew tap static-var/tap
brew install static-var/tap/build-brief
```

or with the install script:

```bash
curl -fsSL https://bb.staticvar.dev/install.sh | bash
```

Prefer:

- `build-brief gradle ...` for a PATH Gradle binary
- `build-brief ./gradlew ...` for a project wrapper

For chained shell commands, rewrite each Gradle segment individually, for
example:

```bash
build-brief gradle test && build-brief gradle check
```

Use raw Gradle only when the user explicitly wants unfiltered Gradle output or
when a tool integration requires exact raw command behavior.
