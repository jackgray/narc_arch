# Install Vault

sudo apt update && sudo apt install gpg

wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg >/dev/null

gpg --no-default-keyring --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg --fingerprint

echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list

sudo apt update && sudo apt install vault

vault server -dev -dev-root-token-id root

export VAULT_TOKEN="root"

export VAULT_ADDR="http://127.0.0.1:8200"

git clone github.com/jackgray/narc_arch

cd narc_arch/narc_cluster/services/vault

terraform init

terraform apply