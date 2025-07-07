# Wisecow Assignment

## Overview
This repository contains the Wisecow application and all necessary configuration to:
- Containerize the app with Docker
- Deploy it to Kubernetes (k3s, minikube, or cloud)
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

## File Structure
```
wisecow-app-accuknox-assignment-/
├── .github/
│   └── workflows/
│       └── ci-cd.yaml         # GitHub Actions workflow for CI/CD
├── wisecow/
│   ├── wisecow.sh             # App source (Bash script)
│   ├── Dockerfile             # Docker build file
├── k8s/
│   ├── deployment.yaml        # Kubernetes Deployment manifest
│   ├── service.yaml           # Kubernetes Service manifest
│   ├── ingress.yaml           # Kubernetes Ingress manifest (with TLS)
├── certs/
│   ├── selfsigned-issuer.yaml # cert-manager ClusterIssuer (self-signed)
│   ├── cert-issuer.yaml       # cert-manager ClusterIssuer (Let's Encrypt, for prod)
│   └── certificate.yaml       # cert-manager Certificate manifest
└── README.md                  # (This file)
```

## Prerequisites
- Docker
- Kubernetes cluster (k3s recommended for this assignment)
- kubectl
- Docker Hub account
- cert-manager and Ingress controller (Traefik is default in k3s)

## Environment-Specific Notes
- **k3s:**
  - Traefik Ingress controller is installed by default.
  - Use the public IP of your VM for external access.
  - For TLS, use the self-signed issuer for local/dev, or Let's Encrypt for production (update cert-issuer.yaml and certificate.yaml accordingly).
- **minikube:**
  - Enable Ingress: `minikube addons enable ingress`
  - Use `minikube tunnel` for LoadBalancer services.
  - Update Ingress annotation to `nginx` if using NGINX Ingress.
- **Cloud (AKS, EKS, GKE):**
  - Ensure ports 80/443 are open in your firewall/security group.

## Setup and Deployment (k3s Example)

### 1. **Install k3s on a Linux VM**
```sh
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--tls-san <PUBLIC_IP>" sh -
```
- Replace `<PUBLIC_IP>` with your VM's public IP (needed for remote access and CI/CD).

### 2. **Configure kubectl Access**
```sh
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
kubectl get nodes
```
- Edit the `server:` line in `k3s.yaml` to use your public IP for remote access.

### 3. **Install cert-manager**
```sh
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml
kubectl wait --namespace cert-manager --for=condition=Ready pods --all --timeout=120s
```

### 4. **Add Domain to /etc/hosts (Local Machine)**
- On your local machine, add:
  ```
  <PUBLIC_IP> wisecow.local
  ```
- This allows you to access the app at https://wisecow.local

### 5. **Deploy the Application and TLS**
```sh
kubectl apply -f certs/selfsigned-issuer.yaml
kubectl apply -f certs/certificate.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

### 6. **Test the Application**
```sh
curl -vk https://wisecow.local
```
Or open [https://wisecow.local](https://wisecow.local) in your browser (accept the self-signed cert warning).

## CI/CD Pipeline (GitHub Actions)
- On every push to `main`, GitHub Actions:
  - Builds and pushes a Docker image to Docker Hub, tagged with both `latest` and the commit SHA.
  - Updates the Kubernetes deployment to use the new SHA-tagged image.
- **Secrets required:**
  - `DOCKER_USERNAME`, `DOCKER_PASSWORD`, `DOCKER_REGISTRY`, `KUBECONFIG`
- **How to verify:**
  - Check the Actions tab for a successful run.
  - Check the pod image tag in your cluster matches the latest commit SHA.

## How to Verify Everything is Working
- **Pod is running:**
  ```sh
  kubectl get pods
  ```
- **Deployment uses correct image:**
  ```sh
  kubectl get deployment wisecow -o yaml | grep image:
  ```
- **App is accessible:**
  ```sh
  curl -vk https://wisecow.local
  ```
- **CI/CD is working:**
  - Push a new commit, see a new pod with a new image tag.
