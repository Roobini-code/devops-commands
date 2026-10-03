# Docker Commands: Basic to Advanced

A practical reference for Docker Engine, Docker Compose, Buildx, and Swarm. Commands use POSIX-style environment-variable syntax where useful; replace placeholders such as `<container>` and `<image>` with your values. On PowerShell, set variables with `$name = "value"` and refer to them as `$name`.

## 1. Check Docker installation and daemon

```sh
docker --version
docker version
docker info
docker help
docker <command> --help
docker context ls
docker context show
```

`docker version` reports both client and server versions. If the server section is unavailable, start Docker Desktop or the Docker Engine service.

## 2. Find and download images

```sh
docker search nginx
docker pull nginx
docker pull nginx:1.27
docker images
docker image ls
docker image ls --digests
docker image history nginx:latest
docker image inspect nginx:latest
```

Image references have the form `registry/namespace/name:tag`. An omitted tag defaults to `latest`; pin an explicit version for reproducible deployments.

## 3. Run and manage containers

```sh
docker run hello-world
docker run --rm alpine:latest echo "Hello from a container"
docker run -it ubuntu:24.04 bash
docker run -d --name web nginx:latest
docker run -d --name web -p 8080:80 nginx:latest
docker run -d --name web -p 127.0.0.1:8080:80 nginx:latest
docker run -d --name web --restart unless-stopped nginx:latest
docker run -d --name app --env NODE_ENV=production my-app:latest
docker run -d --name app --env-file .env my-app:latest
docker run -d --name app --cpus=1.5 --memory=512m my-app:latest
docker run -d --name app --read-only --tmpfs /tmp my-app:latest
docker ps
docker ps -a
docker ps --filter status=exited
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
docker start <container>
docker stop <container>
docker restart <container>
docker pause <container>
docker unpause <container>
docker rename <old-name> <new-name>
docker rm <container>
docker rm -f <container>
```

`-d` runs in the background, `-it` attaches an interactive terminal, `--rm` removes the container when it exits, and `-p HOST_PORT:CONTAINER_PORT` publishes a port. Use `-p 127.0.0.1:HOST_PORT:CONTAINER_PORT` to bind only to localhost.

## 4. Inspect, access, and troubleshoot containers

```sh
docker logs <container>
docker logs -f --tail 100 <container>
docker logs --since 10m <container>
docker inspect <container>
docker inspect --format '{{.State.Status}}' <container>
docker stats
docker stats <container>
docker top <container>
docker port <container>
docker diff <container>
docker events --since 10m
docker exec -it <container> sh
docker exec -it <container> bash
docker exec <container> <command>
docker attach <container>
docker cp <container>:/path/in/container ./local-path
docker cp ./local-file <container>:/path/in/container
docker wait <container>
docker update --memory 1g --cpus 2 <container>
docker kill --signal SIGTERM <container>
```

Use `docker exec` for a new shell or command in a running container. `docker attach` connects to its primary process and may affect that process when detaching.

## 5. Build and publish images

```sh
docker build -t my-app:1.0 .
docker build -f path/to/Dockerfile -t my-app:1.0 .
docker build --no-cache -t my-app:dev .
docker build --pull -t my-app:latest .
docker build --build-arg APP_VERSION=1.0 -t my-app:1.0 .
docker tag my-app:1.0 username/my-app:1.0
docker login
docker login registry.example.com
docker push username/my-app:1.0
docker logout
docker save -o my-app.tar my-app:1.0
docker load -i my-app.tar
docker export <container> -o container-rootfs.tar
docker import container-rootfs.tar imported-image:latest
docker image rm my-app:1.0
```

Use `docker save`/`load` to transfer images with their layers and tags. `docker export`/`import` transfers a container filesystem and does not preserve image metadata or history.

### BuildKit and Buildx

```sh
docker buildx version
docker buildx ls
docker buildx create --name multiarch --use
docker buildx inspect --bootstrap
docker buildx build -t username/my-app:1.0 --push .
docker buildx build --platform linux/amd64,linux/arm64 -t username/my-app:1.0 --push .
docker buildx build --platform linux/amd64 -t my-app:local --load .
docker buildx prune
```

Buildx supports multi-platform builds. `--push` publishes the result; `--load` loads a single-platform result into the local image store.

## 6. Networks

```sh
docker network ls
docker network create app-net
docker network create --driver bridge --subnet 172.20.0.0/16 app-net
docker network inspect app-net
docker network connect app-net <container>
docker network disconnect app-net <container>
docker network rm app-net
docker network prune
```

Containers on a user-created bridge network can reach each other by container name. Prefer user-defined networks over the legacy default bridge for application communication.

## 7. Persistent data and volumes

```sh
docker volume ls
docker volume create app-data
docker volume inspect app-data
docker run -d --name db -v app-data:/var/lib/postgresql/data postgres:16
docker run --rm -v "${PWD}:/workspace" -w /workspace alpine ls
docker run --rm --mount type=volume,src=app-data,dst=/data alpine ls /data
docker volume rm app-data
docker volume prune
```

Named volumes are managed by Docker and are generally preferred for persistent container data. A bind mount (`-v HOST_PATH:CONTAINER_PATH`) maps a host directory or file into a container; check host-path and file-sharing rules for your operating system.

## 8. Docker Compose

Run these from a directory containing `compose.yaml` or `docker-compose.yml`:

```sh
docker compose version
docker compose config
docker compose config --quiet
docker compose pull
docker compose build
docker compose build --no-cache
docker compose up
docker compose up -d
docker compose up -d --build
docker compose ps
docker compose logs
docker compose logs -f --tail 100
docker compose logs -f <service>
docker compose exec <service> sh
docker compose run --rm <service> <command>
docker compose restart
docker compose restart <service>
docker compose stop
docker compose start
docker compose down
docker compose down --remove-orphans
docker compose down --volumes
docker compose -f compose.yaml -f compose.prod.yaml up -d
docker compose --profile monitoring up -d
```

`docker compose down --volumes` deletes Compose-managed volumes and their data; use it only when that data is disposable or backed up.

## 9. Docker contexts and remote daemons

```sh
docker context ls
docker context inspect default
docker context create staging --docker "host=ssh://user@server.example.com"
docker context use staging
docker --context staging ps
docker context use default
docker context rm staging
```

Contexts select which Docker daemon the CLI targets. Confirm the active context before running commands that create or remove resources.

## 10. Cleanup and disk usage

```sh
docker system df
docker system df -v
docker container prune
docker image prune
docker image prune -a
docker volume prune
docker network prune
docker builder prune
docker system prune
docker system prune -a
docker system prune -a --volumes
```

Prune commands permanently remove unused resources. `-a` includes all unused images, not only dangling images; `--volumes` can remove data volumes. Review the confirmation prompt and back up anything important first.

## 11. Docker Swarm

```sh
docker swarm init
docker swarm init --advertise-addr <manager-ip>
docker swarm join-token worker
docker swarm join-token manager
docker swarm join --token <token> <manager-ip>:2377
docker node ls
docker node inspect <node>
docker node update --availability drain <node>
docker service create --name web --replicas 3 -p 8080:80 nginx:latest
docker service ls
docker service ps web
docker service logs -f web
docker service scale web=5
docker service update --image nginx:stable web
docker service update --rollback web
docker service rm web
docker stack deploy -c compose.yaml my-stack
docker stack ls
docker stack services my-stack
docker stack ps my-stack
docker stack rm my-stack
docker swarm leave
docker swarm leave --force
```

Swarm mode is built into Docker Engine. `docker stack deploy` deploys a Compose-format stack to a Swarm; not every Compose feature is supported in stack files.

## 12. Credentials, access, and security checks

```sh
docker login
docker logout
docker scout quickview
docker scout cves <image>
docker scout recommendations <image>
docker run --rm --read-only --cap-drop=ALL --security-opt=no-new-privileges <image>
```

Avoid putting passwords, tokens, or other secrets directly in command-line arguments, image layers, or committed `.env` files. Use a secret manager or the platform's supported secret mechanism.

## 13. Useful command patterns

```sh
docker ps -aq
docker stop $(docker ps -q)
docker rm $(docker ps -aq)
docker image ls --format '{{.Repository}}:{{.Tag}}'
docker inspect --format '{{json .NetworkSettings.Networks}}' <container>
docker run --rm -e KEY=value --entrypoint sh <image> -c 'echo "$KEY"'
```

The command-substitution examples use POSIX shells. In PowerShell, pipe IDs instead:

```powershell
docker ps -q | ForEach-Object { docker stop $_ }
docker ps -aq | ForEach-Object { docker rm $_ }
```

## 14. Quick workflow

```sh
# Build an image from the current directory
docker build -t my-app:dev .

# Start it and publish container port 3000 on localhost port 3000
docker run -d --name my-app -p 127.0.0.1:3000:3000 my-app:dev

# Check status and follow logs
docker ps
docker logs -f my-app

# Stop and remove the container
docker stop my-app
docker rm my-app
```
