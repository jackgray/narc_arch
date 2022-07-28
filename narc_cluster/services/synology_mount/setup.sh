sudo apt install sshfs


printf "Name of drive you are mounting from (you can make this up): "
read drive_name
printf "Name of shared folder (directory after volume1) to mount: "
read directory

mount_point=/mnt/${drive_name}/${directory}

# Prepare mount location
sudo mkdir -p $mount_point

# Get Synology login
echo "Enter the IP address of your server (or alias configured in your ssh config)"
read server_addr
echo "username of Synology server: "
read username
stty -echo
printf "password: "
read password
stty echo
printf "\n"

sudo sshfs ${username}@${server_addr}:/${directory} ${mount_point}

echo "Done! If you didn't get an error, you probably have a successful mount of your network drive at ${mount_point}"