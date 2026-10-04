# Docker Commands: Basic to Advanced

A workflow-oriented reference for commonly used Docker Engine, Docker Compose, Buildx, and Swarm commands. Every command has a short explanation beside it. Replace placeholders such as `<container>`, `<image>`, and `<service>` with your values. Commands use POSIX shell syntax unless labeled PowerShell.

## 1. Check Docker installation and daemon

```sh
docker --version                 # Print the Docker CLI version.
docker version                   # Show both client and daemon versions.
docker info                      # Show daemon configuration, storage, plugins, and resource details.
docker help                      # List Docker commands and general help.
docker <command> --help          # Show help and options for a command, e.g. docker run --help.
docker context ls                # List Docker contexts (daemon connection configurations).
docker context show              # Print the currently selected Docker context.
```

If `docker version` cannot show server details, start Docker Desktop or the Docker Engine service.

## 2. Find and download images

```sh
docker search nginx                        # Search Docker Hub for images matching nginx.
docker pull nginx                          # Download nginx, using its default latest tag.
docker pull nginx:1.27                     # Download the specifically tagged nginx 1.27 image.
docker image ls                            # List images stored locally.
docker images                              # Legacy shorthand for listing local images.
docker image ls --digests                  # List local images including immutable registry digests.
docker image inspect nginx:latest          # Show detailed image configuration and metadata.
docker image history nginx:latest          # Show the image layers and build instructions.
```

Image references have the form `registry/namespace/name:tag`. An omitted tag defaults to `latest`; use explicit version tags for reproducible deployments.

## 3. Create images

```sh
docker build -t my-app:1.0 .                                      # Build from the current directory and tag the image.
docker build -f path/to/Dockerfile -t my-app:1.0 .                # Build using a Dockerfile at a custom path.
docker build --no-cache -t my-app:dev .                           # Build without reusing cached layers.
docker build --pull -t my-app:latest .                            # Check for a newer base image before building.
docker build --build-arg APP_VERSION=1.0 -t my-app:1.0 .          # Pass a build-time argument to the Dockerfile.
docker buildx version                                               # Print the installed Buildx version.
docker buildx ls                                                    # List Buildx builders and supported platforms.
docker buildx create --name multiarch --use                        # Create and select a builder named multiarch.
docker buildx inspect --bootstrap                                   # Show the selected builder and start it if needed.
docker buildx build --platform linux/amd64 -t my-app:local --load . # Build one platform and load the image locally.
docker buildx build --platform linux/amd64,linux/arm64 -t username/my-app:1.0 --push . # Build and push images for two CPU architectures.
```

`--load` makes a single-platform Buildx result available in the local image store. Use `--push` to publish the build directly to a registry.

## 4. Manage, tag, and publish images

```sh
docker image ls --format '{{.Repository}}:{{.Tag}}' # Print local image names and tags only.
docker image inspect my-app:1.0                    # Inspect image configuration, environment, and layers.
docker image history my-app:1.0                    # Review image layer history.
docker tag my-app:1.0 username/my-app:1.0          # Add a registry/user-qualified tag to a local image.
docker login                                       # Authenticate to the default registry (usually Docker Hub).
docker login registry.example.com                  # Authenticate to a specified image registry.
docker push username/my-app:1.0                   # Upload the tagged image to its registry.
docker logout                                      # Remove stored credentials for the default registry.
docker save -o my-app.tar my-app:1.0              # Save an image and its layers to a tar archive.
docker load -i my-app.tar                         # Load an image archive created by docker save.
docker export <container> -o container-rootfs.tar # Export a container filesystem as a tar archive.
docker import container-rootfs.tar imported:latest # Create a new image from an exported filesystem archive.
docker buildx build -t username/my-app:1.0 --push . # Build and push an image to a registry.
```

`docker save`/`load` preserve image layers and tags. `docker export`/`import` transfer a container filesystem only; they do not preserve image metadata or build history.

## 5. Delete images

These commands remove images from the **local Docker daemon**. They do not delete image tags stored on Docker Hub or another registry.

```sh
docker image ls                              # List local images before deleting.
docker image rm my-app:1.0                   # Remove a local image tag.
docker image rm nginx:1.27                   # Remove the local nginx:1.27 image tag.
docker image rm <image-id>                   # Remove a local image by its ID.
docker image rm -f my-app:1.0                # Force-remove a local image tag.
docker image prune                           # Remove dangling local images after confirmation.
docker image prune -a                        # Remove images not used by any container after confirmation.
docker image prune -a -f                     # Remove unused images without a confirmation prompt.
docker image ls -aq                          # Preview IDs of all local images.
docker image ls -aq | Sort-Object -Unique    # In PowerShell, preview unique image IDs before deletion.
docker image ls -aq | sort -u                # In a POSIX shell, preview unique image IDs before deletion.
```

To delete every local image, remove containers that use them first, then run the matching shell command:

```sh
docker image ls -aq | sort -u | xargs -r docker image rm -f # Force-remove all local images in a POSIX shell.
```

```powershell
docker image ls -aq | Sort-Object -Unique | ForEach-Object { docker image rm -f $_ } # Force-remove all local images in PowerShell.
```

Delete a published image tag or repository using Docker Hub's web interface or its registry-supported API; `docker image rm` only affects the local copy.

## 6. Create and run containers

```sh
docker run hello-world                                            # Download if needed, then run Docker's test image.
docker run --rm alpine:latest echo "Hello from a container"       # Run a command and remove its container when it exits.
docker run -it ubuntu:24.04 bash                                  # Start Ubuntu with an interactive terminal and Bash shell.
docker run -d --name web nginx:latest                             # Run nginx in the background with the name web.
docker run -d --name web -p 8080:80 nginx:latest                  # Publish host port 8080 to container port 80.
docker run -d --name web -p 127.0.0.1:8080:80 nginx:latest       # Publish port 8080 only on the host's loopback interface.
docker run -d --name web --restart unless-stopped nginx:latest    # Restart unless the container was explicitly stopped.
docker run -d --name app --env NODE_ENV=production my-app:latest  # Set one environment variable in the container.
docker run -d --name app --env-file .env my-app:latest            # Load environment variables from a file.
docker run -d --name app --cpus=1.5 --memory=512m my-app:latest   # Limit CPU to 1.5 cores and memory to 512 MiB.
docker run -d --name app --read-only --tmpfs /tmp my-app:latest   # Make the root filesystem read-only except temporary /tmp.
docker run -d --name db -v app-data:/var/lib/postgresql/data postgres:16 # Mount a named volume for persistent database storage.
```

`-d` runs in the background; `-it` allocates an interactive terminal; `--rm` removes a container after it exits; and `-p HOST_PORT:CONTAINER_PORT` publishes a port. Binding to `127.0.0.1` limits access to the local machine.

## 7. Manage containers

```sh
docker ps                                                         # List running containers.
docker ps -a                                                      # List all containers, including stopped ones.
docker ps --filter status=exited                                  # List containers that have exited.
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"    # Show selected container fields in a table.
docker start <container>                                          # Start an existing stopped container.
docker stop <container>                                           # Gracefully stop a running container.
docker restart <container>                                        # Restart a container.
docker pause <container>                                          # Suspend the container's processes.
docker unpause <container>                                        # Resume processes suspended with docker pause.
docker rename <old-name> <new-name>                               # Change a container's name.
docker update --memory 1g --cpus 2 <container>                    # Change resource limits on an existing container.
docker kill --signal SIGTERM <container>                          # Send SIGTERM directly to the container's main process.
```

## 8. Debug and inspect containers

```sh
docker logs <container>                                     # Print the container's captured stdout and stderr.
docker logs -f --tail 100 <container>                       # Follow logs, starting with the most recent 100 lines.
docker logs --since 10m <container>                         # Show logs produced in the last ten minutes.
docker inspect <container>                                  # Show detailed container configuration and runtime state.
docker inspect --format '{{.State.Status}}' <container>     # Print only the container's current state.
docker stats                                                # Stream CPU, memory, network, and I/O usage for running containers.
docker stats <container>                                    # Show resource usage for one running container.
docker top <container>                                      # List processes running inside the container.
docker port <container>                                     # List host-to-container port mappings.
docker diff <container>                                     # Show filesystem changes made since the container was created.
docker events --since 10m                                   # Show Docker daemon events from the last ten minutes.
docker exec -it <container> sh                              # Open an interactive sh shell in a running container.
docker exec -it <container> bash                            # Open an interactive Bash shell if Bash is installed.
docker exec <container> <command>                           # Run a command in a running container without opening a shell.
docker attach <container>                                    # Attach your terminal to the container's main process.
docker cp <container>:/path/in/container ./local-path       # Copy a container file or directory to the host.
docker cp ./local-file <container>:/path/in/container       # Copy a host file or directory into the container.
docker wait <container>                                     # Wait for the container to stop and print its exit code.
```

`docker exec` starts a new process in a running container. `docker attach` connects to its main process; sending input or signals can affect that process.

## 9. Delete containers

Removing a container does not normally remove its image or a named volume. Stop it first if you want a graceful shutdown.

```sh
docker container ls -a                                      # List all containers and confirm the name or ID.
docker stop <container>                                      # Gracefully stop a running container.
docker rm <container>                                        # Remove a stopped container by name or ID.
docker rm -f <container>                                     # Force-stop and remove a container.
docker rm -v <container>                                     # Remove the container and anonymous volumes; named volumes remain.
docker container prune                                       # Remove all stopped containers after confirmation.
docker container prune -f                                    # Remove all stopped containers without a confirmation prompt.
docker container ls -aq                                      # Preview IDs of every container, including stopped ones.
docker container ls -aq | xargs -r docker rm -f              # Force-remove every container in a POSIX shell; interrupts running containers.
```

In PowerShell, force-remove every local container with:

```powershell
docker container ls -aq | ForEach-Object { docker rm -f $_ } # Force-remove each local container.
```

## 10. Networks

```sh
docker network ls                                                        # List Docker networks.
docker network create app-net                                            # Create a user-defined bridge network.
docker network create --driver bridge --subnet 172.20.0.0/16 app-net     # Create a bridge network with an explicit subnet.
docker network inspect app-net                                           # Show network settings and attached containers.
docker network connect app-net <container>                               # Connect an existing container to the network.
docker network disconnect app-net <container>                            # Disconnect a container from the network.
docker network rm app-net                                                # Remove a network that has no attached containers.
docker network prune                                                     # Remove unused networks after confirmation.
```

Containers on a user-created bridge network can reach each other by container name. Prefer user-defined networks over the legacy default bridge for application communication.

## 11. Persistent data and volumes

```sh
docker volume ls                                                                # List Docker-managed volumes.
docker volume create app-data                                                   # Create a named volume called app-data.
docker volume inspect app-data                                                  # Show where and how Docker stores the volume.
docker run --rm -v "${PWD}:/workspace" -w /workspace alpine ls                 # Bind-mount the current directory and list it in Alpine.
docker run --rm --mount type=volume,src=app-data,dst=/data alpine ls /data     # Mount a named volume at /data and list its contents.
docker volume rm app-data                                                       # Remove a volume that is not in use.
docker volume prune                                                            # Remove unused volumes after confirmation.
```

Named volumes are managed by Docker and are generally preferred for persistent container data. A bind mount (`-v HOST_PATH:CONTAINER_PATH`) maps a host directory or file into a container; host-path syntax can vary by operating system. Volume removal can permanently erase application data.

## 12. Docker Compose

Run these from a directory containing `compose.yaml` or `docker-compose.yml`.

```sh
docker compose version                                          # Print the Compose plugin version.
docker compose config                                           # Render and validate the merged Compose configuration.
docker compose config --quiet                                   # Validate configuration without printing it.
docker compose pull                                             # Download images referenced by the Compose project.
docker compose build                                            # Build services that have a build configuration.
docker compose build --no-cache                                 # Build services without using cached layers.
docker compose up                                               # Create and start project services in the foreground.
docker compose up -d                                            # Start project services in the background.
docker compose up -d --build                                    # Build required images, then start services in the background.
docker compose ps                                               # Show containers and status for the Compose project.
docker compose logs                                             # Print logs from project services.
docker compose logs -f --tail 100                               # Follow service logs, starting with up to 100 recent lines.
docker compose logs -f <service>                                # Follow logs for one service.
docker compose exec <service> sh                                # Open sh in a running service container.
docker compose run --rm <service> <command>                     # Run a one-off service command and remove its container.
docker compose restart                                          # Restart all services in the project.
docker compose restart <service>                                # Restart one service.
docker compose stop                                             # Stop project containers without removing them.
docker compose start                                            # Start previously created, stopped project containers.
docker compose down                                             # Stop and remove project containers and networks.
docker compose down --remove-orphans                            # Also remove containers no longer defined in the Compose file.
docker compose down --volumes                                   # Also remove Compose-managed volumes and their data.
docker compose -f compose.yaml -f compose.prod.yaml up -d       # Merge two Compose files and start the result in the background.
docker compose --profile monitoring up -d                       # Start services enabled by the monitoring profile as well.
```

`docker compose down --volumes` deletes volume data; use it only when the data is disposable or backed up.

## 13. Docker contexts and remote daemons

```sh
docker context ls                                                        # List available daemon connection contexts.
docker context inspect default                                           # Show connection details for the default context.
docker context create staging --docker "host=ssh://user@server.example.com" # Create a context that connects to a remote daemon over SSH.
docker context use staging                                                # Select staging as the default context for future commands.
docker --context staging ps                                               # List containers on staging without changing the selected context.
docker context use default                                                # Switch the CLI back to the default context.
docker context rm staging                                                 # Remove the staging context configuration.
```

Contexts select which Docker daemon the CLI targets. Confirm the active context before creating or deleting resources.

## 14. Cleanup and disk usage

```sh
docker system df                      # Summarize disk space used by images, containers, and volumes.
docker system df -v                   # Show detailed disk usage for individual Docker resources.
docker builder prune                  # Remove unused build cache after confirmation.
docker buildx prune                   # Remove unused Buildx build cache.
docker system prune                   # Remove stopped containers, unused networks, dangling images, and build cache.
docker system prune -a                # Also remove every image not used by a container.
docker system prune -a --volumes      # Also remove unused volumes; volume data may be permanently lost.
```

Prune commands permanently remove resources. Review the confirmation prompt and back up anything important first.

## 15. Docker Swarm

```sh
docker swarm init                                                        # Initialize Swarm mode on this Docker Engine.
docker swarm init --advertise-addr <manager-ip>                          # Initialize Swarm and advertise a specific manager address.
docker swarm join-token worker                                           # Print a token for adding worker nodes.
docker swarm join-token manager                                          # Print a token for adding manager nodes.
docker swarm join --token <token> <manager-ip>:2377                      # Join this node to a Swarm using a manager-issued token.
docker node ls                                                           # List nodes (run on a manager).
docker node inspect <node>                                               # Show detailed node configuration and status.
docker node update --availability drain <node>                           # Stop scheduling tasks on a node and move tasks elsewhere.
docker service create --name web --replicas 3 -p 8080:80 nginx:latest    # Deploy a replicated nginx service with a published port.
docker service ls                                                        # List Swarm services.
docker service ps web                                                    # List tasks and node placement for the web service.
docker service logs -f web                                               # Follow logs from tasks belonging to the web service.
docker service scale web=5                                               # Set the web service to five replicas.
docker service update --image nginx:stable web                           # Update the service to use the nginx:stable image.
docker service update --rollback web                                     # Roll back the web service to its previous configuration.
docker service rm web                                                    # Remove the web service.
docker stack deploy -c compose.yaml my-stack                             # Deploy a stack from a Compose-format file to the Swarm.
docker stack ls                                                          # List deployed Swarm stacks.
docker stack services my-stack                                           # List services belonging to my-stack.
docker stack ps my-stack                                                 # List tasks belonging to my-stack.
docker stack rm my-stack                                                 # Remove a stack and its services.
docker swarm leave                                                       # Leave the Swarm as a worker or an available manager.
docker swarm leave --force                                               # Force a manager to leave its Swarm.
```

Swarm mode is built into Docker Engine. `docker stack deploy` supports a subset of Compose features. Leaving a manager can affect cluster availability.

## 16. Credentials, access, and security checks

```sh
docker login                                                              # Authenticate to the default registry.
docker logout                                                             # Remove stored credentials for the default registry.
docker scout quickview                                                   # Summarize vulnerabilities and recommendations for an image.
docker scout cves <image>                                                # List known CVEs affecting an image.
docker scout recommendations <image>                                     # Suggest image upgrades or base-image changes.
docker run --rm --read-only --cap-drop=ALL --security-opt=no-new-privileges <image> # Run with a read-only root, no Linux capabilities, and no privilege escalation.
```

Avoid putting passwords, tokens, or other secrets directly in command-line arguments, image layers, or committed `.env` files. Use a secret manager or the platform's supported secret mechanism.

## 17. Useful command patterns

```sh
docker ps -aq                                             # Print IDs of all containers, including stopped ones.
docker stop $(docker ps -q)                               # Stop all running containers (POSIX shell).
docker image ls --format '{{.Repository}}:{{.Tag}}'       # Print local image names and tags only.
docker inspect --format '{{json .NetworkSettings.Networks}}' <container> # Print a container's attached networks as JSON.
docker run --rm -e KEY=value --entrypoint sh <image> -c 'echo "$KEY"' # Override entrypoint and print an environment variable.
```

In PowerShell, pipe IDs to Docker commands with:

```powershell
docker ps -q | ForEach-Object { docker stop $_ } # Stop each running container by ID.
docker ps -aq | ForEach-Object { docker rm $_ }   # Remove each stopped container by ID.
```

## 18. Quick workflow

```sh
docker build -t my-app:dev .                                  # Build and tag the image from the current directory.
docker run -d --name my-app -p 127.0.0.1:3000:3000 my-app:dev # Run it in the background, bound to localhost port 3000.
docker ps                                                     # Check that the container is running.
docker logs -f my-app                                         # Follow the application's output.
docker stop my-app                                             # Gracefully stop the application container.
docker rm my-app                                               # Remove the stopped container; the image remains.
docker image rm my-app:dev                                     # Remove the local image tag after deleting its container.
```
