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