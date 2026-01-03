
minikube start
minikube status
kubectl config use-context minikube
# Enable metrics-server addon
minikube addons enable metrics-server

# Verify metrics-server is running
kubectl get pods -n kube-system | grep metrics-server

# Verify metrics are available (may take 1-2 minutes)
kubectl top nodes

# pull the image
minikube ssh -- docker pull ghcr.io/yandex-practicum/scaletestapp:latest

# Apply the deployment
kubectl apply -f scaletestapp-deployment.yaml

# Apply the service
kubectl apply -f scaletestapp-service.yaml

# Check deployment status
kubectl get deployments
kubectl get pods

# Get the service URL
minikube service scaletestapp-service --url

# This will output something like: http://192.168.49.2:30000
# Test the endpoints using curl:
curl $(minikube service scaletestapp-service --url)/
curl $(minikube service scaletestapp-service --url)/metrics

# Or open in browser (Windows PowerShell):
minikube service scaletestapp-service

# Apply the HPA manifest
kubectl apply -f scaletestapp-hpa.yaml

# Check HPA status
kubectl get hpa

# Watch HPA in real-time
kubectl get hpa scaletestapp-hpa -w

# Get detailed HPA information
kubectl describe hpa scaletestapp-hpa

locust