# gather ips of server nodes and client nodes

# install nomad binary on all the nodes
# allow ports on firewall: 4646, 4647, 4648 /tcp and 4648/udp

# install cfssl
sudo apt-get install go -y;git clone https://github.com/cloudflare/cfssl.git;
cd cfssl;
git checkout tags/v1.5.0;
make;sudo su - ;
cat > /etc/profile.d/cfssl.sh <<EOF
export CFSSL_HOME=/home/opc/cfssl;
export PATH=\${PATH}:\${CFSSL_HOME}/bin;
EOFsudo su - opc;
source /etc/profile;# generate cert and private key.
cfssl print-defaults csr | cfssl gencert -initca - | cfssljson -bare nomad-ca;# create cfssl configuration.
cat <<EOF > cfssl.json
{
  "signing": {
    "default": {
      "expiry": "87600h",
      "usages": ["signing", "key encipherment", "server auth", "client auth"]
    }
  }
}
EOF

# generate nomad server cert
echo '{}' | cfssl gencert -ca=nomad-ca.pem -ca-key=nomad-ca-key.pem -config=cfssl.json \
    -hostname="server.global.nomad,localhost,127.0.0.1" - | cfssljson -bare server# Generate a certificate for the Nomad client.
echo '{}' | cfssl gencert -ca=nomad-ca.pem -ca-key=nomad-ca-key.pem -config=cfssl.json \
    -hostname="client.global.nomad,localhost,127.0.0.1" - | cfssljson -bare client# Generate a certificate for the CLI.
echo '{}' | cfssl gencert -ca=nomad-ca.pem -ca-key=nomad-ca-key.pem -profile=client \
    - | cfssljson -bare cli

# add nomad directories to all nodes
sudo mkdir -p /etc/nomad.d /export/nomad-data;
sudo chown -R nomad:nomad /etc/nomad.d /export/nomad-data;
sudo chmod 777 /etc/nomad.d /export/nomad-data

scp nomad-ca.pem nomad-server{n}:/etc/nomad.d;
scp server.pem nomad-server-{n}:/etc/nomad.d
scp server-key.pem nomad-server-{n}:/etc/nomad.d

# do for client nodes:
scp nomad-ca.pem nomad-client-{n}:/etc/nomad.d
scp client.pem nomad-client-{n}:/etc/nomad.d
scp client-key.pem nomad-client-{n}:/etc/nomad.d

# copy cli keys to all nodes
scp cli.pem nomad-{client/server}-{n}:/etc/nomad.d
scp cli-key.pem nomad-{client/server}-{n}:/etc/nomad.d

# create nomad server config
sudo su -
cat <<EOF > /etc/nomad.d/nomad.hcl
log_level = "INFO"
data_dir = "/export/nomad-data"
server {
  enabled = true
  bootstrap_expect = 3
}
tls {
  http = true
  rpc  = true  ca_file   = "/etc/nomad.d/nomad-ca.pem"
  cert_file = "/etc/nomad.d/server.pem"
  key_file  = "/etc/nomad.d/server-key.pem"  verify_server_hostname = true
  verify_https_client    = true
}
EOF

# create nomad client config
sudo su -;
echo "" > /etc/nomad.d/nomad.hcl;
cat <<EOF > /etc/nomad.d/nomad.hcl
log_level = "INFO"
data_dir = "/export/nomad-data"
client {
  enabled = true
  servers = ["10.0.0.3:4647","10.0.0.4:4647","10.0.0.5:4647"]
}
ports {
  http = 4646
}
tls {
  http = true
  rpc  = true  ca_file   = "/etc/nomad.d/nomad-ca.pem"
  cert_file = "/etc/nomad.d/client.pem"
  key_file  = "/etc/nomad.d/client-key.pem"  verify_server_hostname = true
  verify_https_client    = true
}
EOF

# create system service to run nomad agents
sudo su -;
cat <<EOF > /etc/systemd/system/nomad.service

[Unit]
Description=Nomad
Documentation=https://www.nomadproject.io/docs
Wants=network-online.target
After=network-online.target

[Service]
ExecReload=/bin/kill -HUP $MAINPID
ExecStart=/usr/bin/nomad agent -config /etc/nomad.d
KillMode=process
KillSignal=SIGINT
LimitNOFILE=infinity
LimitNPROC=infinity
Restart=on-failure
RestartSec=2
StartLimitBurst=0
StartLimitIntervalSec=10
TasksMax=infinity

[Install]
WantedBy=multi-user.target
EOF

# run agents
sudo systemctl enable nomad
sudo systemctl start nomad
sudo systemctl status nomad

# set env
sudo su -
cat <<EOF > /etc/profile.d/nomad-cli.sh
export NOMAD_ADDR=https://localhost:4646;
export NOMAD_CACERT=/etc/nomad.d/nomad-ca.pem;
export NOMAD_CLIENT_CERT=/etc/nomad.d/cli.pem;
export NOMAD_CLIENT_KEY=/etc/nomad.d/cli-key.pem;
EOF

# show node status
nomad node status

# check dns with consul get endpoints of nomad servers
dig @127.0.0.1 -p 8600 nomad.servers.consul

# or using nslookup
nslookup nomad.service.consul 127.0.0.1 -port=8600

# ensure docker is installed, then init nomad job
nomad job init
nomad job run example.nomad

# forward DNS for consul discovery
# install bind and bind-utils
sudo apt-get install bind bind-utils -y

#open ports  53/tcp 53/udp

# configure named on master
sudo su -;
echo "" > /etc/named.conf;
cat <<EOF > /etc/named.conf
options {
        listen-on port 53 { 127.0.0.1; 10.0.0.3; };
        # listen-on-v6 port 53 { ::1; };
        directory "/var/named";
        dump-file "/var/named/data/cache_dump.db";
        statistics-file "/var/named/data/named_stats.txt";
        memstatistics-file "/var/named/data/named_mem_stats.txt";
        allow-query { any; };
        allow-transfer { localhost; 172.31.27.18; };
        recursion yes;
        dnssec-enable yes;
        dnssec-validation yes;
        dnssec-lookaside auto;
        /* Path to ISC DLV key */
        bindkeys-file "/etc/named.iscdlv.key";
        managed-keys-directory "/var/named/dynamic";
};
logging {
        channel default_debug {
                file "data/named.run";
                severity dynamic;
        };
};
zone "nomad.cluster" IN {
        type master;
        file "nomad.cluster.zone";
        allow-update { none; };
};
zone "0.10.in-addr.arpa" IN {
        type master;
        file "0.10.zone";
        allow-update { none; };
};
zone "consul" IN {
        type forward;
        forward only;
        forwarders { 127.0.0.1 port 8600; };
};
controls {
        inet 127.0.0.1 allow { localhost; }
        keys { rndc-key; };
};
key "rndc-key" {
        algorithm hmac-md5;
        secret "DWsZoZ8xRALstyi7w5WWzw==";
};
EOF


# create RNDC key and update config above with generated key
rdnc-confgen -a -r /dev/urandom

# add
key "rndc-key" {
    algorithm hmac-md5
    secret [output from above]
}

# create zone files 
cat <<EOF > /var/named/nomad.cluster.zone
\$TTL 86400
@ IN SOA nomad-server-0.nomad.cluster. root.nomad.cluster. (
        2 ;Serial
        3600 ;Refresh
        1800 ;Retry
        604800 ;Expire
        86400 ;Minimum TTL
)
; Specify our two nameservers
        IN NS nomad-server-0.nomad.cluster.
        IN NS nomad-server-1.nomad.cluster.
; Resolve nameserver hostnames to IP, replace with your two droplet IP addresses.
@ IN A 127.0.0.1
 
nomad-server-0   IN A 10.0.0.3
nomad-server-1   IN A 10.0.0.4
nomad-server-2   IN A 10.0.0.5
nomad-client-0   IN A 10.0.0.6
nomad-client-1   IN A 10.0.0.7
EOF
cat <<EOF > /var/named/0.10.zone
@ IN SOA nomad-server-0.nomad.cluster. root.nomad.cluster. (
        1 ;Serial
        3600 ;Refresh
        1800 ;Retry
        604800 ;Expire
        86400 ;Minimum TTL
)
; Specify our two nameservers
        IN NS nomad-server-0.
        IN NS nomad-server-1.
 
; Define ip -> host.
0.3  IN PTR nomad-server-0.
0.4  IN PTR nomad-server-1.
0.5  IN PTR nomad-server-2.
0.6  IN PTR nomad-client-0.
0.7  IN PTR nomad-client-1.
EOF

# create named config on client
sudo su -;
echo "" > /etc/named.conf;
cat <<EOF > /etc/named.conf
options {
        listen-on port 53 { 127.0.0.1; 10.0.0.4; };
        #listen-on-v6 port 53 { ::1; };
        directory "/var/named";
        dump-file "/var/named/data/cache_dump.db";
        statistics-file "/var/named/data/named_stats.txt";
        memstatistics-file "/var/named/data/named_mem_stats.txt";
        allow-query { any; };
        recursion yes;
        dnssec-enable yes;
        dnssec-validation yes;
        dnssec-lookaside auto;
        /* Path to ISC DLV key */
        bindkeys-file "/etc/named.iscdlv.key";
        managed-keys-directory "/var/named/dynamic";
};
 
logging {
        channel default_debug {
                file "data/named.run";
                severity dynamic;
        };
};n
zone "nomad.cluster" IN {
        type slave;
        masters { 10.0.0.3; };
        file "nomad.cluster.zone";
};
zone "0.10.in-addr.arpa" IN {
        type slave;
        masters { 10.0.0.3; };
        file "0.10.zone";
};
zone "consul" IN {
        type forward;
        forward only;
        forwarders { 127.0.0.1 port 8600; };             
};
EOF

# start name server
# check named first
named-checkzone nomad.cluster /var/named/nomad.cluster.zone
named-checkzone 0.10.in-addr.arpa /var/named/0.10.zone

# add DNS in network script /etc/sysconfig/network-scripts/ifcfg-ens3
DNS1=10.0.0.3
DNS2=10.0.0.4

# restart network
sudo systemctl restart network

# check consul dns interface
nslookup nomad.service.consul

# bind should forward dns to consul service discovery
# all apps on nomad should be able access each other with service name registered as a DNS entry in consul service discovery