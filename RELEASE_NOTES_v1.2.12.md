# Release v1.2.12 - No-Shell Entrypoint Fallback (Android/Termux)

- 修复 Android/Termux 下无 shell 镜像启动失败问题：当镜像不包含 `/bin/sh`、`/bin/bash` 等可用 shell 时，不再强制通过 `startup.sh` 启动，而是直接执行镜像 `Entrypoint/Cmd`（例如 `/app/server`）。
- 在“无 shell 回退”路径中，用户通过 `-e` 传入的环境变量（如 `CERBER_API_KEY`、`CERBER_BASE_URL`、`CERBER_MODEL`）会被正确注入，避免运行时配置丢失。
- 优化日志行为：不再重复输出“未找到可用的shell执行脚本”告警。
- 新增回归测试覆盖无 shell 镜像入口执行与环境变量注入场景。

Install:
```bash
curl -sSL https://raw.githubusercontent.com/jinhan1414/android-docker-cli/v1.2.12/scripts/install.sh | sh
```

Update:
```bash
curl -sSL https://raw.githubusercontent.com/jinhan1414/android-docker-cli/main/scripts/update.sh | sh
```

