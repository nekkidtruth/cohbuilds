FROM ubuntu:18.04

WORKDIR /
# Install requirements
RUN apt-get update; \
    apt-get install -y \
        wget \
        software-properties-common \
        apt-transport-https \
        apt-utils

# Install Dotnet Core 3.0 and Visual Studio Code
RUN wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | apt-key add -; \
    wget -q https://packages.microsoft.com/config/ubuntu/18.04/packages-microsoft-prod.deb; \
    dpkg -i packages-microsoft-prod.deb; \
    apt-get update; \
    apt-get install -y dotnet-sdk-3.0

# Install Visual Studio Code
#RUN wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | apt-key add -; \
#    add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"; \
#    apt update; \
#    apt install -y code

# Install Entity Framework Tool
RUN dotnet tool install --global dotnet-ef --version 3.0.0-preview4.19216.3

# Project should be mounted at /cohbuilds
EXPOSE 5001
WORKDIR /cohbuilds
ENTRYPOINT dotnet watch run  
