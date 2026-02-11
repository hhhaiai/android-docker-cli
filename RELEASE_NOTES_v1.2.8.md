# Release v1.2.8 - Supervisord Socket Compatibility

- Ensure Android/Termux writable system directories include `/var/run` so images that use supervisord sockets under `/var/run` can start reliably.

Install:
```bash
curl -sSL https://raw.githubusercontent.com/jinhan1414/android-docker-cli/v1.2.8/scripts/install.sh | sh
```

Update:
```bash
curl -sSL https://raw.githubusercontent.com/jinhan1414/android-docker-cli/main/scripts/update.sh | sh
```

