docker buildx build --platform linux/amd64 -t fe .
docker tag fe:latest ghcr.io/haslhofer/fe:v1
docker push ghcr.io/haslhofer/fe:v1

Create app services plan
Add webapp with image ghcr.io/ghcr.io/haslhofer/fe:v1