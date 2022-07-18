# these commands are currently theoretical and untested

DRIVE_NAME=$1
IP=$2
SHARE_PATH=$3
SMB_ADDR=//${IP}${SHARE_PATH}
MOUNT_PATH=/mnt/${DRIVE_NAME}


sudo mkdir -p /mnt/${DRIVE_NAME}

sudo touch /opt/.smbcredentials && sudo chmod 600 /opt/.smbcredentials

sudo echo -e "username=${SMB_USER}\npassword=${SMB_PASS}\ndomain=//${IP}/${PATH}" >> /opt/.smbcredentials

# if mount fails, check uid/gid settings
sudo echo -e "//${IP}/${SMB_PATH} ${MOUNT_PATH} cifs multiuser,vers=2.0,credentials=/opt/.smbcredentials,iocharacterset=utf8,gid=1000,uid=1000,file_mode=0777,dir_mode=0777 0 0" >> /etc/fstab

# -o flag tells system not to mount automatically on boots
sudo mount -t cifs username=${SMB_USER} //${IP}/${SMB_PATH} ${MOUNT_PATH}

# access share as another user
cifscreds add -u SMB_username $SMB_ADDR



#####################################
AUTO-EDIT FSTAB ON NEW INSTALL
#####################################

mkdir /mnt/shared
chown $USER:$USER /mnt/shared
chmod 777 /mnt/shared
mkdir /mnt/data
chown $USER:$USER /mnt/data
chmod 777 /mnt/data
#The big "X" will also not make files executable unless they were executable to begin with.Morbius1
#sudo chmod -R a+rwX /mnt/data

# edit fstab to add mounts, UUIDs of data partitions do not change
cp /etc/fstab /etc/fstab.backup
#Edit fstab first Need to change from UUID to labels, so it works on both portable & DT
str1="# Entry for /dev/sdc6 :"
str2="UUID=a55e6335-616f-4b10-9923-e963559f2b05  /mnt/data    ext3         auto,users,rw,relatime               0  2  "
str3="# Entry for /dev/sda1 :"
str4="UUID=04B05B70B05B6768                      /mnt/cdrive           ntfs-3g  ro   0  0  "
str5="# Entry for /dev/sdc2 :"
str6="UUID=44332FD360AA9657                      /mnt/shared  ntfs-3g   defaults,uid=1000,nls=utf8,windows_names   0  0  "
fname=/etc/fstab
echo $str1 >> $fname
echo $str2 >> $fname
echo $str3 >> $fname
echo $str4 >> $fname
echo $str5 >> $fname
echo $str6 >> $fname
# Verify no errors in fstab & remount with new mounts
mount -a