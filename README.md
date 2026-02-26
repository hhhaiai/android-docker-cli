# Android Docker CLI

English | [中文](README_ZH.md)

A tool to run Docker images on Android using `proot`, without needing a Docker engine. This project is designed to be used within the [Termux](https://github.com/termux/termux-app) application, providing a Docker-like command-line interface to manage persistent containers.

## Core Features

- **Modular Codebase**: All core logic is organized within the `android_docker` package.
- **Main CLI**: The main entry point is `android_docker/docker_cli.py`, providing a Docker-style CLI for full container lifecycle management.
- **Persistent Containers**: Containers have a persistent filesystem and can be started, stopped, and restarted.
- **Underlying Engine**: Uses `android_docker/proot_runner.py` to execute containers and `android_docker/create_rootfs_tar.py` to download and prepare container images.

## Installation

You can install this tool with a single command:

```bash
# Install latest version (main branch)
curl -sSL https://raw.githubusercontent.com/jinhan1414/android-docker-cli/main/scripts/install.sh | sh

# Install specific version (e.g., v1.2.15)
curl -sSL https://raw.githubusercontent.com/jinhan1414/android-docker-cli/v1.2.15/scripts/install.sh | sh

# Or use environment variable to specify version
INSTALL_VERSION=v1.2.15 curl -sSL https://raw.githubusercontent.com/jinhan1414/android-docker-cli/main/scripts/install.sh | sh
```

This will create an executable `docker` command in your path. After installation, you can run the tool by simply typing `docker`.

## Install Dependencies

```bash
# Android Termux
pkg update && pkg install python proot curl tar

# Ubuntu/Debian
sudo apt install python3 proot curl tar
```

## Quick Start

After installation, you can use this tool just like the standard Docker command line.

```bash
# Log in to a Docker registry (e.g., Docker Hub)
docker login

# Pull an image from a private registry after logging in
docker login your-private-registry.com
docker pull your-private-registry.com/my-image

# Pull a public image
docker pull alpine:latest

# Run a container in the foreground
docker run alpine:latest echo "Hello from container"

# Run a container in the background (detached)
docker run -d -e "API_KEY=sk-12345" --volume /sdcard:/data nginx:alpine

# Run a container interactively
docker run -it swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/library/alpine:latest /bin/sh

# Run an Nginx container with a custom configuration file from the project
# This example uses the `examples/nginx.conf` file, which listens on port 8777.
docker run -d --name my-nginx -v $(pwd)/examples/nginx.conf:/etc/nginx/nginx.conf nginx:alpine

# Auto-remove container after exit
docker run --rm alpine:latest sh -c "echo done"

# Use env file / entrypoint / user
docker run --env-file .env --entrypoint /bin/sh --user 0 alpine:latest -c "env | head"

# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# View container logs
docker logs <container_id>
docker logs -f <container_id>  # Follow logs
docker logs --tail 20 <container_id>
docker logs --since 1m <container_id>

# Stop a container
docker stop <container_id>
docker stop -t 1 <container_id>

# Start a stopped container
docker start <container_id>

# Restart a container
docker restart <container_id>

# Remove a container
docker rm <container_id>
docker rm -f -v <container_id_1> <container_id_2>

# Attach to a running container
docker attach <container_id>

# Execute a command in a running container
docker exec <container_id> ls -l
docker exec -it <container_id> /bin/sh
docker exec -e A=1 --user 0 <container_id> sh -c "echo \$A"

# List cached images
docker images
docker images --digests
docker images --format "{{.Repository}}:{{.Tag}} {{.Digest}}"

# Load an image from a local tar file
docker load -i alpine.tar
docker load -i /path/to/my-image.tar

# Remove a cached image
docker rmi alpine:latest

# Log in to a registry
docker login your-private-registry.com
```

## Loading Local Images

You can load Docker images from local tar archives without needing to pull them from a registry. This is useful for:
- Using pre-downloaded images
- Loading images built on other systems
- Working offline

### Requirements

The tar file must be a valid Docker image archive containing:
- `manifest.json` - Image manifest
- Layer tar files (e.g., `<hash>/layer.tar`)
- Config JSON file (e.g., `<hash>.json`)

### Usage

```bash
# Load an image from a tar file
docker load -i alpine.tar

# Load an image from a specific path
docker load -i /sdcard/Download/my-image.tar

# After loading, the image will appear in your image list
docker images
```

### Creating Docker Image Tar Files

You can create compatible tar files using standard Docker:

```bash
# On a system with Docker installed
docker save alpine:latest -o alpine.tar

# Transfer the tar file to your Android device
# Then load it
docker load -i alpine.tar
```

## Docker Compose Support

This tool supports both `docker compose` and `docker-compose` to manage multi-container applications.

```bash
# Start services defined in docker-compose.yml
docker compose up

# Run in detached mode
docker compose -f docker-compose.yml up -d

# Stop and remove services
docker compose down

# Legacy command is still supported
docker-compose up -d
```

### Sample `docker-compose.yml`

```yaml
version: '3'
services:
  web:
    image: nginx:alpine
    container_name: my-web-server
  db:
    image: redis:alpine
    container_name: my-redis-db
```

## Key Features

- ✅ **Full Container Lifecycle**: `run`, `ps`, `stop`, `start`, `restart`, `logs`, `rm`, `attach`, `exec`.
- ✅ **Registry Authentication**: `login` to private or public registries.
- ✅ **Local Image Loading**: Load Docker images from local tar files with `docker load`.
- ✅ **OCI Registry Support**: Pull images from OCI-compliant registries like GitHub Container Registry (ghcr.io).
- ✅ **Docker Compose Support**: Manage multi-container setups with both `docker compose` and `docker-compose`.
- ✅ **Docker-Style CLI**: A familiar and intuitive command-line interface.
- ✅ **Persistent Storage**: Containers maintain their state and filesystem across restarts, stored in `~/.docker_proot_cache/`.
- ✅ **Android Optimized**: Specially optimized for the Termux environment.

## Parameter Compatibility Notes (v1.2.15)

Supported common combinations:
- `docker run --rm`
- `docker run --env-file`
- `docker run --entrypoint`
- `docker run --user` (partial support)
- `docker run --add-host` and `docker run --dns` (Android path support)
- `docker ps -q` and `docker ps --format`
- `docker logs --tail` and `docker logs --since`
- `docker exec -e` and `docker exec --user` (partial support)
- `docker images --digests` and `docker images --format`
- `docker pull --platform` (accepted with explicit "platform ignored" warning)
- `docker stop -t`
- `docker rm -v`
- `docker rm` with multiple container arguments

Explicitly unsupported `run` options (returns clear error):
- `-p` and `--publish`
- `--network`
- `--restart`
- `--privileged`

Full archived compatibility matrix:
- `docs/docker-parameter-compat-matrix-2026-02-26.md`

## Troubleshooting

```bash
# Check dependencies
curl --version && tar --version && proot --version

# Use verbose logging for more details
docker --verbose run alpine:latest
```

### Common Android Issues

#### Permission Denied Errors

If you encounter permission errors like:
```
nginx: [alert] could not open error log file: open() "/var/log/nginx/error.log" failed (13: Permission denied)
```

**Solution**: The tool automatically creates writable system directories on Android. Ensure you're using the latest version.

#### Whiteout File Warnings

If you see warnings about `.wh.auxfiles` or similar whiteout files:
```
tar: ./var/lib/apt/lists/.wh.auxfiles: Cannot open: Permission denied
```

**Solution**: These files are automatically skipped on Android. Layer deletion semantics may not be fully preserved, but containers will run normally.

#### Extraction Failures

If image extraction fails:
- Use `--verbose` flag to see detailed error messages
- Check available disk space in Termux
- Try pulling a smaller image first (e.g., `alpine:latest`)
- Ensure all dependencies are installed: `pkg install python proot curl tar`

#### Container Startup Issues

If containers fail to start:
- Check logs with `docker logs <container_id>`
- Verify the image is compatible with your architecture
- Some images may require specific capabilities not available in proot
- Try running with `--verbose` for detailed debugging information

If you see errors like `chown ... Operation not permitted` or `Can't drop privilege as nonroot user` on Android/Termux:
- Update to a recent version. Android runs include additional compatibility behavior so images that expect to start as root and then drop privileges can run without extra flags.

## Limitations

- Based on `proot`, not full containerization (no kernel-level process or network isolation).
- Some system calls may not be supported.
- Performance is lower compared to native Docker.
- Network isolation is limited.

### Android-Specific Limitations

- **Whiteout Files**: Docker layer deletion semantics (whiteout files) are skipped on Android due to permission restrictions. This means deleted files from previous layers may still be present in the final container filesystem.
- **System Directories**: Writable system directories (`/var/log`, `/var/cache`, `/tmp`, etc.) are automatically bind-mounted from host storage to work around Android permission restrictions.
- **File Permissions**: Some file permission and ownership operations may not work as expected on Android filesystems.
- **Process Isolation**: proot provides process isolation but not full containerization. Containers share the same kernel and have limited resource isolation.

## License

MIT License
