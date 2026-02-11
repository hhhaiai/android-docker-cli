# Release v1.2.9 - /run and /var/run Compatibility

- Make Android/Termux writable runtime dirs consistent by binding `/run` and `/var/run` to the same host directory.
- Best-effort cleanup of common stale supervisord artifacts (like `supervisor.sock`) in the host-side runtime dir to avoid startup loops.

Install:
```bash
curl -sSL https://raw.githubusercontent.com/jinhan1414/android-docker-cli/v1.2.9/scripts/install.sh | sh
```

Update:
```bash
curl -sSL https://raw.githubusercontent.com/jinhan1414/android-docker-cli/main/scripts/update.sh | sh
```

