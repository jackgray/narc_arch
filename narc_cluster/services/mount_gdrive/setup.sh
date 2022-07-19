# download repository containing tool
sudo add-apt-repository ppa:alessandro-strada/ppa
# obligatory update
sudo apt-get update
# install mount tool
sudo apt-get install google-drive-ocamlfuse
# authorize it
google-drive-ocamlfuse
# make a dir as mount point
sudo mkdir /mnt/google-drive
# create access group for google drive and add executing user
sudo useradd -aG $USER googledrive
# make googledrive group owner 
sudo chown :googledrive /mnt/google-drive
# restrict access only to googledrive group 
sudo chmod  070 /mnt/googledrive/
# mount google drive
google-drive-ocamlfuse /mnt/googledrive
