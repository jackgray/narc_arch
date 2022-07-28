
# Download config compiler
git clone --branch v0.8.0 https://github.com/flatcar-linux/container-linux-config-transpiler
cd container-linux-config-transpiler
make

# Download nomad/consul flatcar configs 
git clone https://github.com/jackgray/narc-flatcar-install
cd ../nomad-on-flatcar

# Generate password hash for users
core_pw=$(mkpasswd --method=SHA-512 --rounds=4096)
shareduser_pw=$(mkpasswd --method=SHA-512 --rounds=4096)

# Generate ignition files from config.yaml
printf "Provide a name for the resource group"
read RESOURCE_GROUP
printf "Provide a name for the datacenter"
read DATACENTER
printf "Provide IP address of "
read BOOTSTRAP_IP
export $RESOURCE_GROUP
export $DATACENTER=datacenter-name
export $BOOTSTRAP_IP
export SSH_PUBKEY=$(ssh-keygen -t rsa -f ./flatcar-key)
make

# # log in to azure
# az login

# # deploy on azure
# make deploy

# Modify config.yaml to include appropriate ssh key

# Download install script (for most up to date)
sudo echo $(wget https://flatcar-linux.org/docs/latest/installing/bare-metal/installing-to-disk/) > flatcar_install.sh

# or use the provided script
flatcar_install -v -d /dev/nvme0n1 -i ignition.json -C stable 