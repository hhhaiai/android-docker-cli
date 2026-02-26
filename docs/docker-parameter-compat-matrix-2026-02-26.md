# Docker 参数兼容清单（归档）

更新时间：2026-02-26  
环境：`jincs@192.168.137.133`（Ubuntu 24.04）  
镜像：`swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/library/alpine:latest`

## 1. 结论概览

- 兼容（通过）：11 项
- 语义不兼容（命令返回成功但行为偏离 Docker）：3 项
- 不兼容（参数未实现或解析错误）：23 项

## 2. 完整测试清单（归档结果）

| ID | 命令 | 结果 | 现象归类 | 可修复性 |
|---|---|---|---|---|
| RUN-001 | `docker run <img> echo basic-ok` | 通过 | 基础前台运行正常 | 保持 |
| RUN-002 | `docker run -e A=1 -v /tmp:/mnt -w / <img> ...` | 通过 | `-e/-v/-w` 正常 | 保持 |
| RUN-003 | `docker run <img> -e A=1 ...` | 通过 | 镜像后参数可被识别 | 保持 |
| RUN-004 | `docker run --name matrix-rm --rm <img> ...` | 失败（语义） | `--rm` 被吞并到容器命令，容器未自动删除 | 可修复（P0） |
| RUN-005 | `docker run --name matrix-port -p 8080:80 <img> ...` | 失败 | `8080:80` 被误当镜像名 | 不建议完整支持（NP），应先做显式报错（P0） |
| RUN-006 | `docker run --publish 8081:81 <img> ...` | 失败 | 端口参数被误解析 | 同上 |
| RUN-007 | `docker run --network host <img> ...` | 失败 | `host` 被误当镜像 | 不建议完整支持（NP），先显式报错（P0） |
| RUN-008 | `docker run --restart always <img> ...` | 失败 | `always` 被误当镜像 | 不建议完整支持（NP），先显式报错（P0） |
| RUN-009 | `docker run --privileged <img> ...` | 失败（语义） | 返回 0，但 `--privileged` 进入容器命令文本 | 不建议完整支持（NP），先显式报错（P0） |
| RUN-010 | `docker run --user 1000:1000 <img> id` | 失败 | `1000:1000` 被误当镜像 | 可部分修复（P1） |
| RUN-011 | `docker run --entrypoint /bin/sh <img> ...` | 失败 | `/bin/sh` 被误当镜像 | 可修复（P1） |
| RUN-012 | `docker run --platform linux/amd64 <img> ...` | 失败 | `linux/amd64` 被误当镜像 | 可部分修复（P1，作为校验/提示） |
| RUN-013 | `docker run --pull always <img> ...` | 失败 | `always` 被误当镜像 | 可部分修复（P1，可映射到 `--force-download`） |
| RUN-014 | `docker run --add-host ...` | 失败 | 参数被误解析 | 可部分修复（P2） |
| RUN-015 | `docker run --dns 8.8.8.8 ...` | 失败 | 参数被误解析 | 可部分修复（P2） |
| RUN-016 | `docker run --env-file /tmp/matrix.env ...` | 失败 | `/tmp/matrix.env` 被误当镜像 | 可修复（P1） |
| RUN-017 | `docker run -d --name matrix-mix --rm <img> ...` | 失败（语义） | `--rm` 未生效，容器保留 | 可修复（P0） |
| PS-001 | `docker ps -q` | 失败 | 参数未实现 | 可修复（P1） |
| PS-002 | `docker ps --format ...` | 失败 | 参数未实现 | 可修复（P1） |
| LOG-001 | `docker logs --tail 10 ...` | 失败 | 参数未实现 | 可修复（P1） |
| LOG-002 | `docker logs --since 1m ...` | 失败 | 参数未实现 | 可修复（P1） |
| EXEC-001 | `docker exec <c> sh -c ...` | 通过 | 基础执行正常 | 保持 |
| EXEC-002 | `docker exec -it <c> sh -c ...` | 通过 | 交互参数正常 | 保持 |
| EXEC-003 | `docker exec <c> -e A=1 ...` | 失败 | `-e` 透传给 proot 报错 | 可部分修复（P1） |
| EXEC-004 | `docker exec --user 0 <c> id` | 失败 | `0` 被当容器名，解析错位 | 可部分修复（P1） |
| IMG-001 | `docker images --digests` | 失败 | 参数未实现 | 可修复（P1） |
| IMG-002 | `docker images --format ...` | 失败 | 参数未实现 | 可修复（P1） |
| PULL-001 | `docker pull --platform linux/amd64 <img>` | 失败 | 参数未实现 | 可部分修复（P1，校验/提示） |
| STOP-001 | `docker stop -t 1 <c>` | 失败 | 参数未实现 | 可修复（P1） |
| STOP-002 | `docker stop <c>` | 通过 | 正常停止 | 保持 |
| START-001 | `docker start <c>` | 通过 | 可启动；存在少量 PID 清理 warning | 可优化（P2） |
| RESTART-001 | `docker restart <c>` | 通过 | 可重启；同上 warning | 可优化（P2） |
| RM-001 | `docker rm -v <c>` | 失败 | 参数未实现 | 可修复（P1，兼容性忽略/提示） |
| RM-002 | `docker rm -f <c>` | 通过 | 强制删除正常 | 保持 |
| CMP-001 | `docker compose version` | 失败 | 未支持子命令 `compose` | 可修复（P0） |
| CMP-002 | `docker-compose -f ... up -d` | 通过 | 当前推荐路径 | 保持 |
| CMP-003 | `docker-compose -f ... down` | 通过 | 当前推荐路径 | 保持 |

补充观测（不在上表 ID 内）：

- `docker rm -f a b c` 当前不支持一次删除多个容器（解析器仅接受一个容器参数）。  
  结论：可修复（P1）。

## 3. 修复分层建议（项目参考）

### P0（应优先）

- `run`/`exec` 参数解析：禁止把未知参数静默拼入容器命令，至少做到“显式报错”。
- `run --rm`：支持真实自动删除语义。
- `docker compose` 兼容：增加 `compose` 子命令并转发到 `docker-compose` 逻辑。

### P1（可逐步补齐）

- 常用输出/过滤参数：
  - `ps -q`
  - `ps --format`
  - `logs --tail/--since`
  - `images --format/--digests`
- 常用兼容参数（即使先做“受限实现”也有价值）：
  - `run --env-file`
  - `run --entrypoint`
  - `run --user`
  - `exec -e`
  - `exec --user`
  - `stop -t`
  - `rm -v`
  - `pull --platform`（至少给出清晰提示）
- `docker rm` 多容器参数支持。

### P2（择机）

- `run --add-host` / `run --dns`（需要和现有 hosts/resolv 绑定逻辑整合）
- `start/restart` 时 rootfs 下陈旧 PID 清理 warning 的可见性与噪音控制。

### NP（不建议按 Docker 完整语义实现）

- `run -p/--publish`
- `run --network`
- `run --privileged`
- `run --restart`

原因：这些能力与 Docker 引擎/内核隔离强绑定，`proot` 路径难以提供等价语义。建议保持“不支持且显式报错”。

## 4. 使用侧建议（用户参考）

- 优先使用已验证组合：
  - `docker run -e ... -v ... -w ... <image> <cmd>`
  - `docker exec [-it] <container> <cmd>`
  - `docker stop/start/restart/rm -f`
  - `docker-compose up -d` / `docker-compose down`
- 避免直接粘贴 Docker Engine 专属参数：
  - `-p`、`--network`、`--privileged`、`--restart`。
- 当前应使用 `docker-compose`，不要使用 `docker compose`。

## 5. 回归建议（基于本清单）

- 每次调整 CLI 参数解析后，至少回归以下关键项：
  - `RUN-004` / `RUN-017`（`--rm` 语义）
  - `RUN-005`~`RUN-016`（未知参数误解析）
  - `EXEC-003` / `EXEC-004`（exec 参数错位）
  - `CMP-001`（`docker compose`）
  - `CMP-002` / `CMP-003`（compose 主路径不回退）

## 6. 修复后复测状态（本地修复分支）

基于同一镜像与同一远端环境，已完成一轮修复后复测（2026-02-26）：

- 已修复并通过：
  - `CMP-001`：`docker compose version`
  - `RUN-004` / `RUN-017`：`--rm` 语义（后台容器退出后会自动清理）
  - `RUN-016`：`--env-file`
  - `RUN-011`：`--entrypoint`
  - `RUN-010`：`--user`（部分支持，附带明确 warning）
  - `EXEC-003`：`docker exec -e`
  - `EXEC-004`：`docker exec --user`（部分支持）
  - `PS-001` / `PS-002`：`ps -q` / `ps --format`
  - `LOG-001` / `LOG-002`：`logs --tail` / `logs --since`
  - `IMG-001` / `IMG-002`：`images --digests` / `images --format`
  - `PULL-001`：`pull --platform`（显式提示“忽略平台，仅按宿主架构”）
  - `STOP-001`：`stop -t`
  - `RM-001` + 多容器：`rm -v`（兼容参数，显式提示）与 `rm` 多容器
  - `docker-compose up -d` 失败路径（坏镜像）返回非 0，不再“假成功”

- 按设计显式拒绝（符合 NP 预期）：
  - `RUN-005` / `RUN-006`：`-p/--publish`
  - `RUN-007`：`--network`
  - `RUN-008`：`--restart`
  - `RUN-009`：`--privileged`

- P2 说明：
  - `--add-host` / `--dns` 已接入 Android hosts/resolv 绑定链路。
  - 在非 Android 环境不会覆写 `/etc/hosts` 与 `/etc/resolv.conf`，因此不会出现 Docker Engine 等价效果（这是当前设计边界）。
