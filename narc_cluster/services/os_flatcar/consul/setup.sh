mkdir -p /etc/consul.d
consul_key=$(consul keygen)
echo consul_key > /etc/consul.d/gossip.key

cd /etc/consul.d && consul tls ca create -domain  consul

# create set of certs for each consul agent
consul tls cert create -server -dc dc1 -domain consul

# distribute to nodes 
scp consul-agent-ca.pem dc1-server-consul-0.pem dc1-server-consul-0-key.pem ${NODE_USER}@${NODE_IP}:/etc/consul.d

sudo mkdir --parents /etc/consul.d
sudo touch /etc/consul.d/consul.hcl
sudo chown --recursive consul:consul /etc/consul.d
sudo chmod 640 /etc/consul.d/consul.hcl

# repeat above for server.hcl

# place consul.service in /etc/system

sudo consul validate /etc/consul.d/
sudo systemctl enable consul
sudo systemctl start consul

#############################
# alternate config (preferred)
#############################
mkdir /etc/consul.d/bootstrap /etc/consul.d/server /etc/consul.d/client

#gist: 
# {
#     "bootstrap": false,
#     "server": true,
#     "datacenter": "nyc2",
#     "data_dir": "/var/consul",
#     "encrypt": "X4SYOinf2pTAcAHRhpj7dA==",
#     "log_level": "INFO",
#     "enable_syslog": true,
#     "start_join": ["192.0.2.1", "192.0.2.3"]
# }

# download web ui files
su consul
cd ~

wget https://dl.bintray.com/mitchellh/consul/0.3.0_web_ui.zip

# store /dist folder and web ui contents in place pointed to by conf file

# on consul servers
touch /etc/init/consul.conf
echo "description "Consul server process"

start on (local-filesystems and net-device-up IFACE=eth0)
stop on runlevel [!12345]

respawn

setuid consul
setgid consul

exec consul agent -config-dir /etc/consul.d/server" \
> /etc/init/consul.conf

# same for client server 
touch /etc/init/consul.conf
echo "description 'Consul client process'

start on (local-filesystems and net-device-up IFACE=eth0)
stop on runlevel [!12345]

respawn

setuid consul
setgid consul

exec consul agent -config-dir /etc/consul.d/client" \
> /etc/init/consul.conf

# on server that contains bootstrap config:
su consul
consul agent -config-dir /etc/consul.d/bootstrap

# on the other consul servers
sudo su - 
start consul
# they will connect to the bootstrap servers

# exit consul process on bootstrap server (ctl-c), then exit consul user to return to root
exit
start consul
# makes originally bootstrapped server join the cluster with un-elevated privs

# add clients to cluster with same process
sudo su -
start consul # client should connect to consul server cluster
# check members of cluster status
consul members

# connect to web ui
# create ssh tunnel to client machine holding ui files (port 8500)
ssh -N -f -L 8500:localhost:8500 root@192.168.0.123

# access consul web interface at http://localhost:8500
# close ssh tunnel; find pid from port
ps aux | grep 8500
kill [pid]

############# AZURE SETUP #######################

source .env

# Create read-only azure service principal - used for consul auto-join (save output values for later)
az ad sp create-for-rbac --role="Reader" --scopes="/subscriptions/${SUBSCRIPTION_ID}"

git clone hashicoprt-guides/azure-consul
cd azure-consul/terraform/single-region

export AUTO_JOIN_SUBSCRIPTION_ID=
export AUTO_JOIN_CLIENT_ID=
export AUTO_JOIN_CLIENT_SECRET=
export AUTO_JOIN_TENANT_ID=

# update terraform.tfvars file

terraform init