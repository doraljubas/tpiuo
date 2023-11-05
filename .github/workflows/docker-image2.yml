name: Docker Image Consumer CI

on:
  push:
    branches: lab1
    paths:
      - 'consumer/consumer.py'
  pull_request:
    branches: lab1
    paths:
      - 'consumer/consumer.py'

jobs:
  editorconfig:
    runs-on: ubuntu-latest
    steps:
    - name: EditorConfig-Action
      uses: zbeekman/EditorConfig-Action@v1.1.1

  linter:
    runs-on: ubuntu-latest
    steps:
    - name: Super-Linter
      uses: super-linter/super-linter@v5.6.1

  build-and-deploy:
    runs-on: ubuntu-latest
    needs: [editorconfig,linter]
    
    steps:
    - name: AzureLogin
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}

    - name: AzureContainerRegistryLogin
      run: az acr login --name fervjestinaregistry.azurecr.io

    - name: DockerImageBuild
      run: docker build -t fervjestinaregistry.azurecr.io/consumer:latest ./consumer

    - name: PushDockerImageToACR
      run: docker push fervjestinaregistry.azurecr.io/consumer:latest
      
    - name: DeployAzureContainerApps
      uses: azure/container-apps-build-and-deploy@v1
      with:
          resourceGroup: fervjestina
          containerAppName: consumer
          image: fervjestinaregistry.azurecr.io/consumer:latest
          namespace: default
      
    
