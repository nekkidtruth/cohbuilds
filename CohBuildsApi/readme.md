# API Development Environment Setup

We're developing on Ubuntu 18.04 with Dotnet Core 3.0.

## Installation

Install Dotnet Core 3.0

```bash
wget -q https://packages.microsoft.com/config/ubuntu/18.04/packages-microsoft-prod.deb

sudo dpkg -i packages-microsoft-prod.deb

sudo add-apt-repository universe

sudo apt-get install apt-transport-https software-properties-common

sudo apt-get update

sudo apt-get install dotnet-sdk-3.0
```

##Install Visual Studio Code
```bash
wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"

sudo apt update

sudo apt install code
```

## Test Dotnet Core Install

```bash
dotnet --version
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)