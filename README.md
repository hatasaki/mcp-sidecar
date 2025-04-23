# MCP Sidecar Pattern
MCP sidecar pattern on Kubernetes

Your can run MCP server only support stdio mode separetely from your app!

## MCP Sidecar concept
![sidecar image](/img/mcp_sidecar.png)

## Content
### Dockerfile-github-mcp-server
Sample Dockerfile to build GitHub MCP Server container(to add some tools to create FIFO pipe in GitHub MCP Server)

### Dockerfile-client-app
Dockerfile for Sample Apps

### mcp-sidecar-deploy.yaml
Kubernetes manifest to run a pod of AI app and MCP server sidecar

### app.py
Sample python app to get your GitHub Repo list via MCP Server

### mcp-proxy.py
Local proxy to bridge stdin/stdout pipe between app container and MCP Server sidecar container

## How to run the sample app
1. Build your app container with Dockerfile-client-app
    - cd ~
    - git clone https://github.com/hatasaki/mcp-sidecar.git
    - cd mcp-sidecar
    - docker build --tag `your-app-container-image` -f Dockerfile-client-app .
    - docker push `your-app-container-image`
2. Build your GitHub MCP Server container with Dockerfile-github-mcp-server
`This is optional, only required for a MCP server container image without shell or mkfifo such as GitHub MCP Server in this sample`
    - cd ~
    - git clone https://github.com/github/github-mcp-server.git
    - cd github-mcp-server
    - cp ../mcp-sidecar/Dockerfile-github-mcp-server .
    - docker build --tag `your-built-github-mcp-server-image>` -f Dockerfile-github-mcp-server .
    - docker push `your-built-github-mcp-server-image>`
3. Run app on your Kubernetes
    - cd ../mcp-sidecar
    - kubectl create ns mcp
    - kubectl create secret generic github-token --from-literal=token=`your GitHub PAT`
    - kubectl apply -f MCP-sidecar-deploy.yaml
4. Test your app
    - kubectl get pod -n mcp
    - kubectl exec github-mcp-sidecar-`your-pod-name` -it -- /bin/bash
    - python app.py
Then, you can see list of your GitHub repos detail

## Contributing
This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.