target_ip=$1

export IP=${target_ip}

hashi-up nomad install -ssh-target-addr $IP -ssh-target-user ubuntu --server

# nomad should be accessible now at http://${target_ip}:4646
nomad agent-info -address=http://${target_ip}:4646

# add client agents to the cluster
export SERVER_IP=${target_ip}
export AGENT_1_IP=<IP to add>
export AGENT_2_IP=<IP to add>

hashi-up nomad install --ssh-target-addr $AGENT_1_IP --ssh-target-user <username> --client --retry-join $SERVER_IP
hashi-up nomad install --ssh-target-addr $AGENT_2_IP --ssh-target-user <username> --client --retry-join $SERVER_IP

# for multi-server HA setup
export SERVER_1_IP=<IP to add>
export SERVER_2_IP=<IP to add>
export SERVER_3_IP=<IP to add>

# to install nomad servers
hashi-up nomad install --ssh-target-addr $SERVER_1_IP --ssh-target-user <username> --server --bootstrap-expect 3 --retry-join $SERVER_1_IP --retry-join $SERVER_2_IP --retry-join $SERVER_3_IP
hashi-up nomad install --ssh-target-addr $SERVER_2_IP --ssh-target-user <username> --server --bootstrap-expect 3 --retry-join $SERVER_1_IP --retry-join $SERVER_2_IP --retry-join $SERVER_3_IP
hashi-up nomad install --ssh-target-addr $SERVER_3_IP --ssh-target-user <username> --server --bootstrap-expect 3 --retry-join $SERVER_1_IP --retry-join $SERVER_2_IP --retry-join $SERVER_3_IP

# to join client agents
hashi-up nomad install --ssh-target-addr $AGENT_1_IP --ssh-target-user $target_username --client --retry-join $SERVER_1_IP --retry-join $SERVER_2_IP --retry-join $SERVER_3_IP
hashi-up nomad install --ssh-target-addr $AGENT_2_IP --ssh-target-user $target_username --client --retry-join $SERVER_1_IP --retry-join $SERVER_2_IP --retry-join $SERVER_3_IP

