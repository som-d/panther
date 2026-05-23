# Docker + Kubernetes Study Plan

**Target Level:** Mid-level DevOps (3+ YOE) | 7-14 LPA interviews
**Scope:** Docker is MEDIUM-HIGH priority (70% JDs mention it). K8s is LOW (35% — nice-to-have).
**Rule:** Only study what matters for interviews. Dont become a container expert overnight.

---

## Part 1: Docker (HIGH Priority — 1 Week)

### Day 1: Docker Fundamentals
**What is Docker?**
- Container = lightweight VM (shares host OS kernel)
- Image = read-only template (snapshot of a container)
- Container = running instance of an image

**Key concepts:**
```bash
docker pull nginx          # Download an image
docker run -d -p 80:80 nginx    # Run a container
docker ps                  # List running containers
docker stop <container>    # Stop a container
docker rm <container>      # Remove a container
docker images              # List images
docker rmi <image>         # Remove an image
```

### Day 2: Dockerfile
```dockerfile
FROM node:20-alpine        # Base image (small! alpine = 5MB)
WORKDIR /app               # Working directory
COPY package*.json ./      # Copy package files first (layer caching)
RUN npm install            # Install dependencies
COPY . .                   # Copy source code
EXPOSE 3000                # Document port
CMD ["npm", "start"]       # Default command
```

**Layer caching trick:** Copy package.json before source code. If dependencies don't change, Docker reuses the cached layer. Faster builds.

### Day 3: Docker Compose
```yaml
version: '3.8'
services:
  web:
    build: ./web
    ports:
      - "3000:3000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/mydb

  db:
    image: postgres:15
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}

volumes:
  pgdata:
```

**Compose = multi-container local development.** Not for production.

### Day 4: Multi-stage Builds
```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Production (smaller image)
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Why:** Final image is ~20MB instead of ~1GB (no build tools, no source code).

### Day 5: Docker in CI/CD
```yaml
steps:
  - script: docker build -t myapp:$(Build.BuildId) .
  - script: docker tag myapp:$(Build.BuildId) myregistry.azurecr.io/myapp:$(Build.BuildId)
  - script: docker push myregistry.azurecr.io/myapp:$(Build.BuildId)
```

### Day 6: Container Registry + Security
- Docker Hub vs Azure Container Registry (ACR)
- ACR Tasks — build images in Azure
- Image scanning — `docker scout` or Trivy
- **Never run containers as root** (use `USER node` in Dockerfile)

### Day 7: Practice
- Create Dockerfile for a Node.js app
- Build and run locally
- Push to ACR
- Multi-stage build optimization

---

## Part 2: Kubernetes Basics (LOW Priority — 3 Days Only)

### Day 8: K8s Concepts (Just Know These)
- **Cluster:** Set of machines (nodes) running containers
- **Node:** Worker machine (VM)
- **Pod:** Smallest deployable unit (1+ containers)
- **Deployment:** Declarative update for Pods
- **Service:** Stable network endpoint to access Pods
- **Namespace:** Virtual cluster within a cluster

### Day 9: Key Objects
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myregistry.azurecr.io/myapp:latest
        ports:
        - containerPort: 3000
---
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 3000
```

### Day 10: AKS (Azure Kubernetes Service)
- AKS = Managed Kubernetes on Azure
- Node pools: system (core services) vs user (your apps)
- `az aks create` — create cluster
- `az aks get-credentials` — connect kubectl

**Only need to know:**
- What AKS is and why use it (managed control plane)
- How Terraform creates AKS clusters
- Deploying with kubectl apply

**Dont bother with:**
- Helm charts (not asked at this level)
- Service mesh (Istio/Linkerd)
- K8s operators
- Custom controllers

---

## Interview Questions

### Docker
1. "What's the difference between an image and a container?"
2. "How do Docker layers work?"
3. "What is a multi-stage build and why use it?"
4. "How do you optimize Docker image size?"
5. "Explain Docker Compose vs Docker Swarm"
6. "How do you handle secrets in Docker?" (Answer: dont use ENV for secrets, use Docker secrets or volume mount)

### Kubernetes
1. "What is a Pod?" (Answer: smallest deployable unit, 1+ containers sharing network/storage)
2. "What is a Deployment vs a StatefulSet?"
3. "How do you expose an application in K8s?" (Service types)
4. "What is a kubeconfig file?"
5. "How does AKS differ from self-managed Kubernetes?"

---

## Key Docker Commands Reference

```bash
docker build -t myapp:1.0 .          # Build image
docker run -d -p 8080:80 myapp:1.0  # Run container
docker exec -it <id> sh              # Shell into container
docker logs <id>                     # Check logs
docker stats                         # Live resource usage
docker system prune                  # Clean unused resources
docker network ls                    # List networks
docker volume ls                     # List volumes
```

---

## Key K8s Commands Reference

```bash
kubectl get nodes                    # List nodes
kubectl get pods                     # List pods
kubectl get deployments              # List deployments
kubectl get services                 # List services
kubectl logs <pod-name>              # Check pod logs
kubectl describe pod <pod-name>      # Detailed pod info
kubectl apply -f deployment.yaml     # Create/update resources
kubectl delete -f deployment.yaml    # Delete resources
kubectl exec -it <pod> -- sh         # Shell into pod
```

---

*Last updated: 21 May 2026 | Focus on Docker (1 week), K8s basics (3 days max)*
