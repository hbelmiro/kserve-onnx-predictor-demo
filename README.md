# kserve-onnx-predictor-demo

This repository provides a demo for deploying a custom predictor to serve ONNX models using KServe, designed to run
seamlessly on macOS and a local Kind cluster. It addresses challenges like NVIDIA Triton’s incompatibility with Macs by
using a lightweight, CPU-based custom predictor, making it a practical starting point for ONNX model serving in
Kubernetes.

## This is not supposed to be needed in production

For a production environment, https://kserve.github.io/website/master/modelserving/v1beta1/onnx/ can be used.

## Why This Exists

Serving ONNX models with KServe can be complex on environments not supported by NVIDIA Triton, especially on macOS with
ARM64 architecture. This demo:

- Offers a **custom predictor** built with Python and ONNX Runtime, ensuring compatibility with macOS and CPU
  environments.
- Demonstrates deployment on **Kind** (Kubernetes in a container engine) with KServe, simplifying local testing and
  scaling.
- Provides a reproducible setup for developers to experiment with ONNX model serving on their Macs.

## What This Does

- **Model**: An example ONNX model (in this case, for fraud detection) with 5 input features, served via a custom
  predictor.
- **Predictor**: A Python script (`predictor.py`) leveraging KServe’s API and ONNX Runtime to load and serve ONNX
  models.
- **Deployment**: Instructions for running locally on macOS or deploying to Kind with KServe, including Kubernetes
  manifests.

## Prerequisites

- **Container Engine**: A container engine, like [Podman](https://podman.io), for building the container image and
  running Kind.
- **[Kind](https://kind.sigs.k8s.io)**: To create a local Kubernetes cluster.
- **kubectl**: To interact with the cluster.
- **Python 3.11+**: For local execution.
- **[uv](https://docs.astral.sh/uv/)**: For dependency management (optional but recommended).

## Running Locally on macOS

### Start the Server: Run the predictor locally:

```shell
python predictor.py
```

This starts a server on `http://0.0.0.0:8080`.

### Test the Endpoint

In a new terminal, send a sample request:

```shell
curl -i -X POST http://0.0.0.0:8080/v1/models/onnx-model:predict -H "Content-Type: application/json" -d '{"
instances": [[50.0, 5.0, 0.0, 0.0, 1.0]]}'
```

Expected output:

```shell
HTTP/1.1 200 OK
date: Sat, 05 Apr 2025 14:42:34 GMT
server: uvicorn
content-length: 38
content-type: application/json

{"predictions":[[0.9998821020126343]]}
```

## Deploying to Kind with KServe

### Install KServe on Kind

Set up KServe in your Kind cluster by following the official KServe
instructions: https://kserve.github.io/website/master/get_started/#install-the-kserve-quickstart-environment

### Build and Push the Image

Build the container image using a container engine, like [Podman](https://podman.io), and push it to a registry
(e.g., [Quay.io](https://quay.io)):

```shell
podman build -t quay.io/<your-username>/kserve-onnx-predictor-demo:latest -f Containerfile .
podman push quay.io/<your-username>/kserve-onnx-predictor-demo:latest
```

Replace `<your-username>` with your Quay.io username.

### Update the Manifests with your new image

Update [inferenceservice.yaml](manifests/inferenceservice.yaml) setting the image you've created in the previous step in
`spec.predictor.containers[0].image`.

### Deploy the Manifests

Apply the Kubernetes manifests from the `manifests` directory:

```shell
kubectl apply -k manifests
```

This deploys the `InferenceService` in the `onnx-model` namespace.

### Port-Forward to the Pod

KServe services lack selectors, so port-forward to the pod:

```shell
kubectl get pods -n onnx-model -l serving.kserve.io/inferenceservice=onnx-model -o jsonpath="{.items[0].metadata.name}" | xargs -I {} kubectl port-forward -n onnx-model pod/{} 8080:8080
```

### Run a Test Request

With the port-forward active, test the deployed model:

```shell
curl -i -X POST http://localhost:8080/v1/models/onnx-model:predict -H "Content-Type: application/json" -d '{"instances": [[50.0, 5.0, 0.0, 0.0, 1.0]]}'
```

Expected output:

```
HTTP/1.1 200 OK
date: Mon, 07 Apr 2025 21:34:03 GMT
server: uvicorn
content-length: 38
content-type: application/json

{"predictions":[[0.9998821020126343]]}
```

### Undeploying everything

Run the following command to undeploy this demo:

```shell
kubectl delete -k manifests
```
