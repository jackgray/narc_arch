Follow these steps to mount an SMB network drive to a linux machine

1. Add line to /etc/fstab on linux machine 

sudo echo "//10.95.18.51/shr3 /mnt/J-Drive cifs multiuser,vers=2.0,credentials=/home/narclab/.smbcredentials

currently there is a permission denied error when trying to mount the easy way using the config files, so you probably need to type in the full address and username, but the config files are still required
