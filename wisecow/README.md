# Wisecow Assignment

## Overview
This repository contains the Wisecow application and all necessary configuration to:
- Containerize the app with Docker
- Deploy it to Kubernetes (k3d/k3s/minikube/cloud)
- Expose it securely over HTTPS using Ingress and TLS
- Automate build and deployment with GitHub Actions (CI/CD)

## Architecture
- **App:** Bash script serving fortunes via cowsay (port 4499)
- **Docker:** Containerizes the app and its dependencies
- **Kubernetes:**
  - **Deployment:** Runs the app
  - **Service:** Exposes the app internally (port 80 → 4499)
  - **Ingress:** Routes HTTPS traffic to the app, terminates TLS
  - **cert-manager:** Automates TLS certificate management (self-signed for local/dev)
- **CI/CD:** GitHub Actions workflow for build, push, and deploy

## Prerequisites
- Docker
- [k3d](https://k3d.io/) (recommended for local dev)
- kubectl
- (Optional) k3s, minikube, or any Kubernetes cluster

## Local Deployment (with k3d)

### 1. Clone the Repository
```sh
git clone <repo-url>
cd <repo-root>
```

### 2. Create a k3d Cluster
```sh
k3d cluster create wisecow-cluster --api-port 6550 -p "80:80@loadbalancer" -p "443:443@loadbalancer"
export KUBECONFIG=$(k3d kubeconfig get wisecow-cluster > /tmp/k3d-wisecow.yaml && echo /tmp/k3d-wisecow.yaml)
```

### 3. Install cert-manager
```sh
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml
kubectl wait --namespace cert-manager --for=condition=Ready pods --all --timeout=120s
```

### 4. Add Local Domain
Add to your `/etc/hosts`:
```
127.0.0.1 wisecow.local
```

### 5. Deploy the App and TLS
```sh
kubectl apply -f wisecow/selfsigned-issuer.yaml
kubectl apply -f wisecow/certificate.yaml
kubectl apply -f wisecow/deployment.yaml
kubectl apply -f wisecow/service.yaml
kubectl apply -f wisecow/ingress.yaml
```

### 6. Test the App
```sh
curl -vk https://wisecow.local
```
Or open [https://wisecow.local](https://wisecow.local) in your browser (accept the self-signed cert warning).

## Ingress & TLS Details
- Uses Traefik (default in k3d/k3s) as Ingress controller
- Ingress resource is annotated with `kubernetes.io/ingress.class: traefik`
- TLS is managed by cert-manager with a self-signed ClusterIssuer for local/dev
- For production, swap to a real domain and a Let's Encrypt ClusterIssuer

## CI/CD (GitHub Actions)
- Workflow in `.github/workflows/ci-cd.yaml`:
  - Builds and pushes Docker image to Docker Hub
  - Deploys new image to Kubernetes
- Requires secrets: `DOCKER_USERNAME`, `DOCKER_PASSWORD`, `DOCKER_REGISTRY`, `KUBECONFIG`

## Portability Notes
- All manifests use standard Kubernetes resources
- Should work on any Kubernetes environment (k3d, k3s, minikube, GKE, EKS, etc.)
- For minikube, ensure Ingress controller is enabled and service type is LoadBalancer
- For production, update domain and TLS issuer as needed

## Project Structure
- `wisecow.sh` – App source
- `Dockerfile` – Container build
- `deployment.yaml`, `service.yaml`, `ingress.yaml` – Kubernetes manifests
- `selfsigned-issuer.yaml`, `certificate.yaml` – cert-manager TLS setup
- `.github/workflows/ci-cd.yaml` – CI/CD pipeline

## Contact
For any questions, please contact the repository owner.
