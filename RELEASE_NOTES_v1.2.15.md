# Release v1.2.15 - Docker Parameter Compatibility (P0-P2)

- 完成 P0-P2 参数兼容修复并复测：
  - 新增 `docker compose` 子命令兼容，并保留 `docker-compose`。
  - 修复 `docker-compose up -d` 失败路径返回码，不再“假成功”。
  - 修复 `docker run --rm` 真实自动删除语义（含后台容器退出场景）。
  - 新增常见参数支持：`run --env-file/--entrypoint/--user/--add-host/--dns`、`exec -e/--user`、`ps -q/--format`、`logs --tail/--since`、`images --digests/--format`、`stop -t`、`rm -v`、`rm` 多容器。
  - 对 `-p/--publish`、`--network`、`--restart`、`--privileged` 改为显式拒绝（避免静默误解析）。
- 新增参数兼容回归测试与文档归档：
  - `tests/test_cli_parameter_compat_repro.py`
  - `docs/docker-parameter-compat-matrix-2026-02-26.md`

Install:
```bash
curl -sSL https://raw.githubusercontent.com/jinhan1414/android-docker-cli/v1.2.15/scripts/install.sh | sh
```

Update:
```bash
curl -sSL https://raw.githubusercontent.com/jinhan1414/android-docker-cli/main/scripts/update.sh | sh
```

