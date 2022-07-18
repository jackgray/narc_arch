datacenter = "local-1"
data_dir = "/opt/consul"
encrypt = "L8JqKSIj6hhLbDgk13fLsozLP4quK5p3Y+rgbPC455c="
verify_incoming = true
verify_outgoing = true
verify_server_hostname = true
ca_file = "/etc/consul.d/consul-agent-ca.pem"
cert_file = "/etc/consul.d/local1-server-consul-0.pem"
key_file = "/etc/consul.d/local1-server-consul-0-key.pem"

auto_encrypt {
    allow_tls = true
}

retry_join = []