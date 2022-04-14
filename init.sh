# install/update npm and required dependencies for node/typescript 
sudo apt upgrade 
curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
sudo apt install nodejs
sudo apt install build-essential
sudo apt autoremove
npm install npm@latest -g
npm update

# Configure private settings 
# create password for Pulumi 
# export PULUMI_CONFIG_PASSPHRASE='enterpassphrasehere'

# ^ or, simply remove -y flag from pulumi new command below for interactive setup 

# use local Pulumi state file 
# pulumi login --local

# create folder for cluster config files 
mkdir -p ~/narc-cluster && cd narc-cluster

# create pulumi project -- launches interactive setup tool
pulumi new kubernetes-typescript 
# ^ you may need to log into app.pulumi.com and generate an access token for project init sud

#  download node modules
npm install 