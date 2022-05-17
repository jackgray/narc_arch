import paramiko
from ssh_utilities import Connection
from narc_cluster.db.configs import fileServer


def sshConnect():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(fileServer.config['host_addr'], 22, username=fileServer.config['username'], password=fileServer.config['password'], look_for_keys=False, allow_agent=False)

    # ssh = Connection.add_hosts({"user": fileServer.config['username'], "hostname": fileServer.config['host_addr'], "password": fileServer.config['password'], "identityfile": None}, allow_agent=False)
    
    return ssh

