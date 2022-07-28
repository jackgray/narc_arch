# Operating System
FlatCar Linux
https://flatcar-linux.org/

Install fresh hard drives then run install script from another system with this drive as a target

`wget https://raw.githubusercontent.com/flatcar-linux/init/flatcar-master/bin/flatcar-install`

Install required binaries 

`sudo apt-get install bash lbzip2 zip2 mount lsblk wget grep cp dd mkfifo mkdir rm tee udevadm gpg gpg2 gawk`

`flatcar-install -d /dev/sda -i ignition.json`


# Install BuildKit
For building containers

# Install Firecracker VMs
https://github.com/cneira/firecracker-task-driver

enable KVM 
ensure tun module is loaded

# Install Min.io 